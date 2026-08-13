# Persistence Layout

Default root: `~/.limitless/learn-anything/<slug>/`

```
learner.md           # living capability + progress state
recon.md             # latest pedagogy recon for active emission
progression-map.md   # all tiers: titles + exit goals; mark which is fully written
tier-1.md            # fully written active/completed tiers
tier-2.md            # …
capstone-tN.md       # optional instantiated capstone attempt sheet
reports/             # dated progress reports
sessions/            # optional raw formative transcripts
```

## learner.md minimum fields

- topic, slug, goal
- active_tier, status
- lessons_completed[]
- lesson_assessments{} — formative notes per lesson
- capstone / capstone_result
- strengths[], issues[]
- user_feedback
- search_backed: true|false
- updated: ISO date

Never require the user's git repo to store these unless they explicitly ask for project-local curricula.
