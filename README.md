# Oz Deal Agent

Find Australian deals that fit your interests, minimum benefit and preferred time commitment. Oz Deal Agent is an open-source skill for Codex and Claude Code that monitors OzBargain, checks potential matches against the merchant's current terms, and lets you refine recommendations through conversation.

[中文说明](README.zh-CN.md) · [Report a bug or request a feature](https://github.com/YanZhu1105/oz-deal-agent/issues/new/choose) · [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) · [Disclaimer](DISCLAIMER.md)

> **Early prototype:** Use it in a local Codex session first. Onboarding can set up automatic collection and scheduled AI digests where your host supports them. A macOS collector installer is included; availability of host schedules and notifications varies. The project does not provide a hosted service, email or Telegram delivery. A deal, its eligibility and its terms can change: check the linked offer before acting. This project is independent and is not affiliated with OzBargain.

## What it does

- Asks five setup questions: interests, minimum AUD benefit, maximum time to complete the requirements, an optional high-value override and digest frequency.
- Covers 17 selectable topics, from banking, credit cards and cashback to groceries, travel and technology. Deals can belong to multiple topics.
- Screens RSS titles and summaries first, then checks promising OzBargain posts and official merchant terms. For every offer, summarises verified reward and costs, claim steps, eligible and excluded customers, deadlines and payout. Credit-card details also cover prior-card exclusions, interest-free repayment and automatic-payment options where verified.
- Keeps preferences, feedback, collected deals and delivered IDs in a local SQLite database. Previously delivered IDs are excluded from later reports.
- On the first run, can backfill the site's publicly paginated list of deals marked active, then continue collecting new RSS entries.

The collector uses Python's standard library and makes no model API calls. Your AI host performs analysis with its own available usage allowance. A paid API key is not required by this project; access, usage limits, scheduling and notifications depend on your AI provider and account.

## Get started

### Requirements

- Codex or Claude Code with local skills, file and network access. Availability and usage limits depend on your account and platform.
- Git and Python **3.9 or newer**. On Windows, Python may need the IANA time zone database: `python -m pip install tzdata`. The project has not yet been tested on Windows.
- A computer that can reach OzBargain and the relevant merchant websites.

### Install and run

1. Clone the repository and enter it:

   ```bash
   git clone https://github.com/YanZhu1105/oz-deal-agent.git
   cd oz-deal-agent
   ```

2. Open this folder as a project. Codex discovers `.agents/skills/oz-deal-agent`; Claude Code discovers `.claude/skills/oz-deal-agent`. If the skill does not appear, restart the host or select the project again. You do not need to install a separate AI API key for this project.

3. In Codex, ask (in Claude Code, use `/oz-deal-agent`):

   > Use `$oz-deal-agent` to set up my deal preferences and find my first deals.

   The agent will show the categories, ask the five questions and save your answers. First-run backfill can involve many pages and may take several minutes. It screens listings in batches; official verification of promising deals takes additional time.

4. Tell the agent what was useful, irrelevant or wrong. Feedback is appended locally and can inform later recommendations. You can ask to change your categories or thresholds at any time.

The skill uses the [Agent Skills](https://agentskills.io/) format. Claude Code project discovery follows its documented layout but has not yet been verified end-to-end in this project. For Grok Bot, see the [experimental prompt adapter](adapters/grok-bot/README.md): its cloud routines do not automatically share the local database. Downloading alone does not create a schedule.

## Scheduling and notifications

After you answer the final question about frequency, the agent should discover the current host’s capabilities and attempt to set up both an RSS collector and an AI digest schedule. It should report what actually succeeded, without requiring you to select an implementation. If scheduling is not available or fails, it should clearly say so and invite you to return to the conversation for a manual check. It must not claim automatic push is enabled until the actual scheduled task exists. AI runs consume your host's usage allowance. The macOS collector itself does not call AI.

For Codex Desktop, the agent can use its scheduled-task capability if available. Claude Desktop supports persistent local scheduled tasks, while Claude Code `/loop` is session-scoped; a cloud task cannot access your local SQLite database. Grok Bot uses cloud routines and needs a separately verified durable private store. See [Claude scheduling](https://code.claude.com/docs/en/scheduled-tasks) and [Grok routines](https://docs.x.ai/grok-bot/skills-routines-and-automations).

### macOS RSS collector

The agent can install and check the per-user collector, which runs every 15 minutes:

```bash
python3 .agents/skills/oz-deal-agent/scripts/schedule_collector.py install
python3 .agents/skills/oz-deal-agent/scripts/schedule_collector.py status
```

The installer creates a launchd job and copies the collector into your local state directory. Run `agent.py status` and check the collector logs to confirm a successful fetch; a loaded job alone is not proof. Re-run `install` after updating the project to refresh the collector. To stop and remove the job while preserving your data:

```bash
python3 .agents/skills/oz-deal-agent/scripts/schedule_collector.py uninstall
```

The collector requires your Mac to be on and a logged-in user session. It can miss posts during sleep, outages or rate limits. The scheduler installer currently supports macOS only. On other systems, use a local scheduler for `collect`, or run `python3 .agents/skills/oz-deal-agent/scripts/agent.py watch` in a terminal for collection every 15 minutes while it remains open. These commands collect only; they do not send an AI digest. Re-run the installer when you change `OZ_DEAL_DATA` for a different user.

## How matching works

A normal match must be in a selected topic, meet the minimum estimated **net** benefit in AUD, and fit the maximum task duration. If enabled, the separate high-value threshold bypasses the topic and duration limits. Task duration means the time needed to fulfil the conditions; it is separate from the time waiting for a reward to arrive. Prices, spend requirements and unsupported retail-price claims are not automatically counted as savings.

The agent screens summaries before opening candidates. It should compare the original post with current official merchant terms, including hidden or expandable footnotes. An unverified official offer is not a confirmed match. If a required amount or duration is unknown, it is flagged for review rather than silently presented as qualifying. Potential matches and values may be missed or misclassified; the system cannot determine your eligibility without the relevant facts.

First-run backfill relies on public listing pages, which include the site's current assessment of deal status, not a guarantee that an offer is live. The public pagination has limits and can shift during collection; long-running offers and posts outside the feed or listing can be missed. The RSS contains only a limited teaser ([OzBargain announcement](https://www.ozbargain.com.au/node/295181)). Avoid aggressive requests and do not bypass access controls ([site discussion](https://www.ozbargain.com.au/node/676479)).

## Data and privacy

Local data is stored at `~/.local/share/oz-deal-agent/deals.sqlite3`. Set `OZ_DEAL_DATA` to a separate directory to isolate another user or a test run. For example, on macOS/Linux:

```bash
OZ_DEAL_DATA="$PWD/test-data" python3 .agents/skills/oz-deal-agent/scripts/agent.py status
```

Use the same directory in that user's scheduled jobs. The database contains browsing preferences and feedback: keep it private, back it up if needed and never commit it. To reset the project, stop collectors and delete or move this directory; that also removes preferences and delivery history. Requests go to OzBargain and relevant merchants, and the selected AI host processes the content under its own terms. Do not enter passwords, banking details or identity documents into the profile.

Every feedback entry is appended locally. This is preference-based adjustment by the agent, not model training. Delivered IDs are recorded after the host confirms delivery; exactly-once delivery depends on that host. Clearing the database loses the history. The repository license does not grant permission to republish third-party content; link to the original deal and merchant.

## Development

```bash
python3 -m unittest discover -s tests -v
python3 .agents/skills/oz-deal-agent/scripts/agent.py --help
```

`collect`, `watch`, `bootstrap` and `post` make network requests. Use a separate `OZ_DEAL_DATA` when testing. See [CONTRIBUTING.md](CONTRIBUTING.md) for changes and [SECURITY.md](SECURITY.md) for private vulnerability reporting.

## Disclaimer and license

Results are based on public online information and can be wrong or outdated. The author and contributors disclaim liability for losses to the fullest extent permitted by law; independently verify each offer. See the full [disclaimer](DISCLAIMER.md). Software: [MIT](LICENSE).

Running `report` also appends verified matching deals to `~/.local/share/oz-deal-agent/qualifying-deals.csv`. Open it in Excel, Numbers or another spreadsheet app and edit the Status and Notes columns. Existing rows are preserved rather than overwritten; check current terms before acting, because saved rows do not update automatically.
