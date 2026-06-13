# Graduation H2 re-review prompt

Sent to the same resumed James subagent.

```text
Resume the same James thread for the updated PRD. Use prior issue list as process memory only. Evidence is still limited to the current allowed scope.

Project root:
/home/pyro/projects/private/limitless/docs/dojo/james-runs/fixtures/holdout-h2

Target document:
PRD.md

Allowed context:
- PRD.md only

Document intent:
PRD

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
