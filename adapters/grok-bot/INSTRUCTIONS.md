# Oz Deal Agent for Grok Bot — experimental prompt adapter

Grok Bot uses native cloud skills and routines. This adapter is a prompt, not an installable copy of the repository's local Python skill: cloud routines cannot automatically use a database on your computer. Its ability to persist structured files and verify sources across runs depends on the Bot's available tools and has not been tested by this project.

1. Create a private Bot and send the text in [PROMPT.md](PROMPT.md). Complete its five onboarding questions.
2. Ask the Bot to save the method as a skill and test it once before scheduling.
3. Ask it to create a routine at the chosen cadence and local time. Inspect the saved schedule and use **Test** if available. Enable its app notifications separately if desired.
4. Before relying on deduplication or feedback, verify that the Bot can store and read a durable, private list of prior deal IDs, preferences and feedback across independent routine runs. If it cannot, it must disclose that and should not claim reliable deduplication. Do not upload bank credentials or identity documents.

A Grok Bot routine runs in the cloud, so it does not need your computer on, but schedules, tool access, account availability, notifications and usage are controlled by Grok Bot. A routine that fetches RSS only at digest time may miss posts; a separate collector and durable store are needed for frequent collection, and no such cloud integration is provided here. Do not use one user's state for another user. See the official [skills and routines guide](https://docs.x.ai/grok-bot/skills-routines-and-automations).
