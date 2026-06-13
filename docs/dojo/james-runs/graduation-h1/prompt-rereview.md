# Graduation H1 re-review prompt

Sent to the same resumed James subagent.

```text
Resume the same James review thread for the updated document. Use prior issue list as process memory only. Evidence is still limited to the current allowed scope.

Project root:
/home/pyro/projects/private/limitless/docs/dojo/james-runs/fixtures/holdout-h1

Target document:
docs/strategy.md

Allowed context:
- docs/strategy.md only

Document intent:
strategy document

Review question:
Can a future agent understand and act on this document using only the allowed scope?

Output exactly this shape:

Score: X/10
Passed: yes/no

Issues:
1. [Issue.] Fixable now: yes/no. [Short reason.]
2. ...

Scope notes:
- [Say what context you used and what you refused to use.]

No severity buckets. No high/medium/low labels. Do not rewrite the document. This is raw re-review data for the main agent.
```
