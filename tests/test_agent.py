"""Tests of screening, delivery history and feedback; no network required."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from types import SimpleNamespace

SCRIPT = Path(__file__).resolve().parents[1] / '.agents/skills/oz-deal-agent/scripts/agent.py'
spec = importlib.util.spec_from_file_location('oz_deal_agent', SCRIPT)
agent = importlib.util.module_from_spec(spec)
spec.loader.exec_module(agent)


class AgentTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.previous_data = agent.DATA
        agent.DATA = Path(self.tmp.name)
        self.addCleanup(setattr, agent, 'DATA', self.previous_data)
        self.conn = agent.connect()
        self.addCleanup(self.conn.close)
        self.call(agent.setup, categories='Cashback', minimum=100, global_minimum=300,
                  max_days=90, frequency_days=1, notes='')

    def call(self, func, **args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            func(self.conn, SimpleNamespace(**args))
        return json.loads(output.getvalue())

    def deal(self, id, amount, days, categories, verification='active'):
        analysis = {'categories': categories, 'status': 'known', 'benefit_aud': amount,
                    'task_days': days, 'verification': {'status': verification}}
        self.conn.execute('INSERT INTO deals VALUES (?,?,?,?,?,?,?,?,?)',
                          (id, 'Test', 'https://www.ozbargain.com.au/node/'+id,
                           agent.iso(), '', '[]', '{}', agent.iso(), json.dumps(analysis)))
        self.conn.commit()

    def test_schedule_time_and_timezone_are_saved_together(self):
        profile = self.call(agent.setup, categories='Cashback', minimum=100,
                            global_minimum=300, max_days=90, frequency_days=3,
                            delivery_time='09:00', timezone='Australia/Melbourne', notes='')
        self.assertEqual((profile['frequency_days'], profile['delivery_time'], profile['timezone']),
                         (3, '09:00', 'Australia/Melbourne'))
        with self.assertRaises(ValueError):
            self.call(agent.setup, categories='Cashback', minimum=100,
                      global_minimum=300, max_days=90, frequency_days=3,
                      delivery_time='25:00', timezone='Australia/Melbourne', notes='')

    def test_threshold_duration_override_and_verification(self):
        self.deal('1', 150, 90, ['Cashback', 'Mobile & internet'])
        self.deal('2', 299, 91, ['Cashback'])
        self.deal('3', 300, 365, ['Automotive'])
        self.deal('4', 300, 0, ['Cashback'], 'unverified')
        self.deal('5', 400, 0, ['Cashback'], 'expired')
        result = self.call(agent.report, hours=None)
        self.assertEqual({d['id'] for d in result['matches']}, {'1', '3'})
        self.assertEqual([d['id'] for d in result['needs_review']], ['4'])

    def test_verified_offer_requires_source_and_evidence(self):
        self.deal('1', 150, 0, ['Cashback'], 'unverified')
        record = {'id': '1', 'categories': ['Cashback'], 'status': 'known',
                  'benefit_aud': 150, 'task_days': 0, 'evidence': 'post',
                  'verification': {'status': 'active'}}
        previous_stdin = agent.sys.stdin
        try:
            agent.sys.stdin = io.StringIO(json.dumps([record]))
            with self.assertRaises(ValueError):
                self.call(agent.analyse)
        finally:
            agent.sys.stdin = previous_stdin

    def test_delivery_history_is_idempotent_and_per_person(self):
        self.deal('1', 150, 0, ['Cashback'])
        self.call(agent.mark_delivered, ids=['1', '1'])
        self.call(agent.mark_delivered, ids=['1'])
        self.assertFalse(self.call(agent.report, hours=None)['matches'])
        self.assertEqual(self.conn.execute('SELECT count(*) FROM deliveries').fetchone()[0], 1)
        with tempfile.TemporaryDirectory() as other:
            agent.DATA = Path(other)
            other_conn = agent.connect()
            try:
                self.assertEqual(other_conn.execute('SELECT count(*) FROM deliveries').fetchone()[0], 0)
            finally:
                other_conn.close()

    def test_feedback_appends_and_legacy_verification_is_not_assumed(self):
        self.deal('1', 150, 0, ['Cashback'], 'unverified')
        self.call(agent.feedback, id='1', rating='wrong', note='Wrong eligibility')
        self.call(agent.feedback, id='1', rating='useful', note='Useful category')
        self.call(agent.feedback, id='general', rating='useful', note='Explain fees')
        self.assertEqual(self.conn.execute('SELECT count(*) FROM feedback_events').fetchone()[0], 3)
        result = self.call(agent.report, hours=None)
        self.assertFalse(result['matches'])
        self.assertEqual(result['needs_review'][0]['id'], '1')


if __name__ == '__main__':
    unittest.main()
