# Oz Deal Agent

Find Australian deals that fit your interests, minimum benefit and preferred time commitment. Oz Deal Agent is an open-source skill for Codex that monitors OzBargain, checks potential matches against the merchant's current terms, and lets you refine recommendations through conversation.

[中文说明](README.zh-CN.md) · [Report a bug or request a feature](https://github.com/YanZhu1105/oz-deal-agent/issues/new/choose) · [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md)

> **Early prototype:** Use it in a local Codex session first. Automatic collection, scheduled AI runs and notifications require separate setup and a host that supports them. The project does not provide a hosted service, email or Telegram delivery. A deal, its eligibility and its terms can change: check the linked offer before acting. This project is independent and is not affiliated with OzBargain.

## What it does

- Asks five setup questions: interests, minimum AUD benefit, maximum time to complete the requirements, an optional high-value override and digest frequency.
- Covers 17 selectable topics, from banking, credit cards and cashback to groceries, travel and technology. Deals can belong to multiple topics.
- Screens RSS titles and summaries first, then checks promising OzBargain posts and official merchant terms. For every offer, summarises verified reward and costs, claim steps, eligible and excluded customers, deadlines and payout. Credit-card details also cover prior-card exclusions, interest-free repayment and automatic-payment options where verified.
- Keeps preferences, feedback, collected deals and delivered IDs in a local SQLite database. Previously delivered IDs are excluded from later reports.
- On the first run, can backfill the site's publicly paginated list of deals marked active, then continue collecting new RSS entries.

The collector uses Python's standard library and makes no model API calls. Your AI host performs analysis with its own available usage allowance. A paid API key is not required by this project; access, usage limits, scheduling and notifications depend on your AI provider and account.

## Get started

### Requirements

- Codex with local skills, file and network access. Availability and usage limits depend on your account and platform.
- Git and Python **3.9 or newer**. On Windows, Python may need the IANA time zone database: `python -m pip install tzdata`. The project has not yet been tested on Windows.
- A computer that can reach OzBargain and the relevant merchant websites.

### Install and run

1. Clone the repository and enter it:

   ```bash
   git clone https://github.com/YanZhu1105/oz-deal-agent.git
   cd oz-deal-agent
   ```

2. Open this folder as a Codex project. Codex discovers the project skill in `.agents/skills/oz-deal-agent`. If it does not appear, restart Codex or select the project again. You do not need to install a separate AI API key.

3. In Codex, ask:

   > Use `$oz-deal-agent` to set up my deal preferences and find my first deals.

   The agent will show the categories, ask the five questions and save your answers. First-run backfill can involve many pages and may take several minutes. It screens listings in batches; official verification of promising deals takes additional time.

4. Tell the agent what was useful, irrelevant or wrong. Feedback is appended locally and can inform later recommendations. You can ask to change your categories or thresholds at any time.

The skill uses the [Agent Skills](https://agentskills.io/) folder format; compatibility with other hosts, including Claude Code, has **not** been tested. Downloading the repository does not automatically configure an AI host, install a scheduler or send notifications.

## Scheduling and notifications

Selecting a frequency saves a preference; it **does not** turn on a schedule. If your Codex host supports scheduled tasks, ask it to schedule the digest in your existing chat at your chosen time. Check the scheduled task was actually created and your account has enough usage. Local jobs need the computer on; local Codex scheduled tasks may also require the app to remain running.

New-deal RSS is a rolling snapshot. Fetching it only once a day can miss entries, so collection should run more frequently than the digest. To collect every 15 minutes while a terminal process remains open:

```bash
python3 .agents/skills/oz-deal-agent/scripts/agent.py watch
```

On Windows use `python` if `python3` is unavailable. Alternatively, configure your operating system's scheduler to run the `collect` command. This collector uses no AI, and it does not send a digest. Stop the terminal process with `Ctrl+C`. When the computer sleeps, stops, loses network access or is rate-limited, deals can be missed.

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

## License

[MIT](LICENSE).
