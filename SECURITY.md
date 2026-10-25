# Security policy

Security fixes target the `master` branch and the next release. Older deck
snapshots are not maintained independently. Use the latest published release and
an Anki client that is supported by its own maintainers.

## Reporting a vulnerability

Use GitHub's **Security → Report a vulnerability** feature when it is available
for this repository. If private reporting is unavailable, open an issue titled
“Private security contact requested”, without exploit details, credentials or
personal data, so the maintainer can arrange a private channel. Do not attach a
personal Anki collection or review history to a public report.

A useful private report identifies the affected version, operating system and
Python/Anki versions, provides a minimal reproduction, and explains the impact.
Use a disposable collection and non-sensitive sample data. There is no promised
response deadline or bug bounty.

This repository contains editable geography data and deck build/export tooling.
Problems in Anki itself should also be reported through the Anki project's own
reporting process. Geographical errors and translation corrections belong in
ordinary content issues rather than security reports.
