# Sample Failure Postcards

Three examples showing different artifact types for the same product: a team wiki tool.

---

## Postcard 1: Support Ticket

> **Subject:** Can't find my own page
>
> I created a page yesterday called "Q2 Planning." I can see it in the sidebar under my team's space. But when I search for it, nothing comes up. I tried "Q2", "planning", even the exact title. Zero results.
>
> My coworker said it might be because the page is in draft mode. But I published it. At least I think I did — there is no visible difference between draft and published.

- **What this reveals:** Search does not index reliably, and publish state is invisible to the author.
- **Broken assumption:** The team assumed search "just works" and that authors would know their page was live.
- **What to change:** Add a visible publish badge, and make search index immediately on save (not just on publish).

---

## Postcard 2: One-Star Review

> One star. I spent 20 minutes writing a page and then accidentally navigated away. No warning. No draft saved. Just gone. The "auto-save" feature listed on the homepage apparently only works if you have been on the page for more than 60 seconds, which I learned from a forum post, not the product.

- **What this reveals:** Auto-save has a silent minimum threshold that users cannot see or predict.
- **Broken assumption:** The team assumed 60 seconds was long enough that "everyone would trigger auto-save." Real writing involves switching tabs, checking references, and coming back.
- **What to change:** Save on every keystroke or pause, with no minimum threshold. Show the last-saved timestamp visibly.

---

## Postcard 3: Postmortem Fragment

> **Incident:** 3 users in the pilot reported "lost pages" in the same week. Investigation showed pages were not lost — they were created inside a personal space that the user later archived without realizing it contained active work.
>
> **Root cause:** Archiving a space silently archives all child pages. No confirmation lists the affected pages. Users archived the container without understanding the blast radius.

- **What this reveals:** Destructive actions on containers do not surface the consequences to child content.
- **Broken assumption:** Users understand the nesting model well enough to predict cascade effects.
- **What to change:** Show a summary of affected pages before any archive or delete action on a space.
