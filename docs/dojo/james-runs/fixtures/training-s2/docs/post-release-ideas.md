# LedgerKit Post-Release Ideas

This note collects non-committed follow-up ideas after LedgerKit v0.2.0 shipped
the Event Ledger, Acceptance Card, and Outcome Queue surfaces. It is an ideas
note, not implementation approval.

## Ideas

1. **Acceptance Card to Outcome Queue trace link.**
   - Proposal: when an Acceptance Card creates an Outcome Queue item, preserve
     a link between them so the Event Ledger can show why the follow-up exists.
   - Implementation readiness: needs a field name and backfill rule before
     implementation.
2. **Weekly Outcome Queue cleanup.**
   - Proposal: add a recurring review pass for stale Outcome Queue entries so
     follow-up ideas are closed, deferred, or promoted deliberately.
   - Implementation readiness: blocked until the cleanup mode and stale-entry
     threshold are decided.
3. **"Why accepted" field for Acceptance Cards.**
   - Proposal: capture the reason a task was accepted, not only that the
     checklist passed.
   - Implementation readiness: needs a required-versus-optional field decision
     before implementation.

## Open questions

- Should cleanup be manual or automatic?
- What age or condition makes an Outcome Queue entry stale enough for cleanup?
- Should Outcome Queue entries inherit labels from the originating Acceptance
  Card?
- Should "why accepted" be required or optional on Acceptance Cards?
