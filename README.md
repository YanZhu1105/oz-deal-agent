# Oz Deal Agent

An open-source, local-first OzBargain deal companion for an existing AI agent such as Codex. It collects the recent public RSS feed, lets your agent classify and summarise relevant deals, and remembers your settings and feedback locally. It does not require a separate AI API key: the host agent uses its own account and usage allowance.

**Early prototype.** Manual collection, analysis and feedback are implemented. Automatic collection and daily push depend on a scheduler you enable; neither is installed automatically. The feed is a rolling snapshot and can miss posts. This project is not affiliated with or endorsed by OzBargain.

## Use with Codex

1. Download or clone this repository and open its folder as a Codex project. Python 3.9 or newer is required. The included skill is in `.agents/skills/oz-deal-agent`.
2. Ask Codex: `Use $oz-deal-agent to set up my deal preferences.` Choose from all 17 interest categories, set the minimum AUD benefit, the maximum time to complete the offer requirements, and whether a higher-benefit exception applies to other categories. Task duration and payout wait are recorded separately.
3. Ask for today's deals. The agent collects the feed, analyses candidates and presents a grouped digest with original links. Tell it which deals were useful, irrelevant or wrong, and why; general feedback can also be saved.
4. If supported by your Codex account, ask it to schedule a daily run in the same chat. Ask separately about scheduling the RSS collector every 15 minutes. A local schedule needs your machine to be on; desktop AI jobs may also require the app running. Scheduling availability and usage limits depend on the platform and account. No guarantee is made about free-plan availability.

The first run sees only posts still in the feed. For reliable coverage, the collector must run frequently and persist its database, and even then network errors, site restrictions, edits or posts outside the deal feed can cause omissions. RSS feeds have had a limited amount of post text since [OzBargain's 2025 change](https://www.ozbargain.com.au/node/295181). Run `python3 .agents/skills/oz-deal-agent/scripts/agent.py watch` to collect every 15 minutes while that process is running, or schedule the `collect` command using your operating system. The collector fetches RSS once per invocation; the agent may fetch individual relevant original posts. Avoid aggressive requests and do not bypass site access controls; see [OzBargain's RSS discussion](https://www.ozbargain.com.au/node/676479).

The standalone skill format may also be usable by other compatible agents, including Claude Code, but that integration has not yet been tested. This repository does not provision or send email, Telegram or other external messages.

## State and privacy

Preferences, feed entries, analysis and feedback are stored in SQLite under `~/.local/share/oz-deal-agent/`. Set `OZ_DEAL_DATA` to choose another directory. Requests go to OzBargain; the chosen AI host handles the text according to its own terms. Never enter passwords, banking details or identity documents into the profile. The database contains personal preferences: don't commit it to a public repository. Outputs link to original posts; they are not a license to republish third-party content.

Every feedback entry, including general feedback, is appended locally and can be reviewed later. The agent uses feedback to adjust future recommendations; this does not train the model. Deals can have multiple categories and are deduplicated. Unknown amounts or task durations are separated for review when relevant and never treated as qualifying. Savings, eligibility and expiry can be wrong or change: check the original offer and merchant conditions.

## Commands

The script is `.agents/skills/oz-deal-agent/scripts/agent.py`; run `python3 <script> --help` for all commands. `collect` and `post` make network requests. To inspect data without changing your main state, set `OZ_DEAL_DATA` to a temporary directory. No API tokens or dependencies are required by the script.
