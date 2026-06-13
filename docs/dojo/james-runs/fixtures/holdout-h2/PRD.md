# PRD: Launch Board

## Problem

Teams need a launch board that shows whether a release is ready.

## Product Boundary

Launch Board is a release-readiness dashboard. It should collect the status,
approval state, blockers, and notification state for one software launch at a
time.

This PRD is review-ready but not implementation-ready. The required human
decisions below must be answered before implementation starts.

## Required Human Decisions

1. Target customer and first user roles: who uses this first?
   Answer: Decision pending.
2. Launch status model: which statuses exist, and what evidence moves a launch
   between them?
   Answer: Decision pending.
3. Approval authority: which role can approve a launch, and what must be true
   before approval is allowed?
   Answer: Decision pending.
4. Blocker policy: what counts as blocked, who can mark it blocked, and which
   events trigger notifications?
   Answer: Decision pending.
5. Pricing: is pricing in scope for the first version, out of scope, or a
   business decision required before release?
   Answer: Decision pending.
6. Launch policy: what readiness policy must the board enforce?
   Answer: Decision pending.

## First-Version Users

Pending human decision. Do not infer target customer, buyer, or role model from
this draft.

## Features

The first version should support these feature areas after the decisions above
are answered:

1. Show the selected launch status for a release.
2. Show whether the release has been approved.
3. Show blocker state and blocker reason.
4. Notify the selected recipients when the human-defined blocker trigger occurs.

## Non-Goals Until Decided

1. Pricing and billing behavior.
2. Multi-launch portfolio reporting.
3. Automatic launch approval.
4. External integrations beyond the notification channel selected by the human.

## Acceptance

The PRD becomes implementation-ready when:

1. Every required human decision has a concrete answer in this document.
2. A future agent can name the first user role, status values, approval
   authority, blocker trigger, notification recipients, pricing scope, and
   launch policy from this document.
3. Each first-version feature has at least one observable acceptance check.
4. James re-reviews the filled-in PRD and passes it.
