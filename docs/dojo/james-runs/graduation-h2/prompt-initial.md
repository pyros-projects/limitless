# Graduation H2 initial prompt

Sent to resumed James subagent `019ec0a6-fc06-7fd2-8a4d-bfdda1497cf2`.

```text
Resume as James for a new scoped document review. You may use prior issue list and calibration as process memory only. Prior document facts are not evidence for this review unless present in the allowed scope.

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

No severity buckets. No high/medium/low labels. Do not rewrite the document. This is raw review data for the main agent.
```
