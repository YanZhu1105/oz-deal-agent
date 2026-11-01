# Contributing

Issues and pull requests are welcome. For a bug report, include the operating system, Python version, command or Codex prompt, expected and actual behaviour, and a minimal redacted reproduction. Do not include account numbers, identity documents, API keys, local databases or private feedback.

1. Fork the repository and create a branch.
2. Make a focused change; avoid sending unnecessary requests to OzBargain or merchants during tests.
3. Run `python3 -m unittest discover -s tests -v` and describe the results in the pull request.
4. Update the README or skill instructions when behaviour or installation changes.

The collector uses the Python standard library; tests use temporary databases and should not need network access. Manual live-source checks may be useful for source changes but must respect site access rules. Do not mark an unverified or expired offer as confirmed, and preserve user preferences, feedback and delivery history during migrations.

For a sensitive vulnerability, use the private reporting process in [SECURITY.md](SECURITY.md), not a public issue.
