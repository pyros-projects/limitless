# Strategy

## Product Boundary

Navigator is an internal planning tool for agents that need to turn planning
documents into reviewable work contracts. It keeps the plan, contract clauses,
review notes, and next implementation actions in one place.

## Direction

Navigator should become the place where planning documents turn into reviewable
work contracts.

In this document, a "reviewable work contract" means a short set of obligations
that a future agent can verify against concrete evidence before claiming the
work is done.

## Bet

Agents forget details unless the next action is forced to consult them.

## First Users

The first users are implementation agents receiving a planning document from a
previous session. The job is to know what must be built, what evidence proves it
was built, and which decisions still require the human.

## Near-Term Priorities

1. Define the contract clause shape: obligation, acceptance evidence, authority
   boundary, and unresolved human questions.
2. Convert one planning document into that contract shape.
3. Run a fresh review pass to check whether another agent can act from the
   contract without hidden context.

## Success Measures

Navigator is working when:

1. A future agent can identify the next implementation action from the contract.
2. Each obligation has a matching acceptance evidence slot.
3. Missing human decisions are explicit instead of hidden in prose.
4. A reviewer can reject a completion claim by pointing to an unmet obligation.
