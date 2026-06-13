# Trigger eval prompt

This prompt was sent twice to fresh routing judges.

```text
You are a skill-routing judge. Below is the list of installed skills
(name: description). For each user prompt, answer with the single skill name
you would invoke, or "none". Output one line per prompt: "<n>: <skill-name>".
No explanations.

SKILLS:
agent-browser: Browser automation CLI for AI agents.
article-pack: This skill should be used when the user wants to create publishable content such as articles, blog posts, social media kits, slide decks, newsletters, or podcast transcripts.
ast-grep: Guide for writing ast-grep rules to perform structural code search and analysis.
canvas-design: Create beautiful visual art in .png and .pdf documents using design philosophy.
codies-research: This skill should be used when the user needs live research, source verification, fact-checking, current comparisons, or updates to an existing research note.
doc: Use when the task involves reading, creating, or editing `.docx` documents.
dojo: This skill should be used when the user wants to create, improve, test, or evaluate a Claude Code skill.
failure-postcards: Use when a feature, flow, or product idea sounds fine in the abstract but needs emotionally concrete pressure-testing before or during design.
find-skills: Helps users discover and install agent skills.
ghost-user: Use when something seems obvious to the builders and you want a cold first-contact pass from a first-time user with zero context or author knowledge.
hivemind: This skill should be used when the user wants to know what the collective brain is saying, building, or publishing about a topic.
humanizer: Remove signs of AI-generated writing from text.
imagegen: Generate or edit raster images when the task benefits from AI-created bitmap visuals.
james: This skill should be used after the agent writes or materially edits a concept, PRD, plan, spec, design document, strategy document, or similar planning artifact, and whenever the user says invoke James, run James, James this, or James-review. It reviews whether the document is self-contained inside project-owned scope, fixes what can be fixed, then re-reviews until pass. Not for code review, article editing, or writing the initial document.
last30days: Research what people actually say about any topic in the last 30 days.
local-mythology: Use when a project has good instincts but weak self-definition.
memory-boot: This skill should be used at session start, when entering a new project, or when the user says load memory or boot.
memory-capture: This skill should be used when the agent needs to save something to memory.
memory-close-session: This skill should be used at end of session, when wrapping up work.
memory-help: Use when the user tells you to check out your memories.
memory-promote: This skill should be used when the agent needs to evaluate or promote memory records through the trust pipeline.
naming-as-design: Use when a product, workflow, or system uses muddy, overlapping, or conflicting names.
openai-docs: Use when the user asks how to build with OpenAI products or APIs.
pdf: Use when tasks involve reading, creating, or reviewing PDF files.
plugin-creator: Create and scaffold plugin directories for Codex.
pp-suno: The correct, offline-first Suno CLI.
searxng: This skill should be used when the agent needs to perform web searches, look up current information online, or gather search results from the internet.
skill-creator: Guide for creating effective skills.
skill-installer: Install Codex skills into $CODEX_HOME/skills from a curated list or a GitHub repo path.
suno-pack: This skill should be used when the user wants to create music with Suno or execute an existing suno-pack.
surface-first-development: This skill should be used when the user wants to build, prototype, or reshape an app, tool, CLI, API, automation, or feature by starting from the interaction surface first.
taste-distiller: Use when someone likes a product, interface, writing style, or codebase but cannot yet explain the hidden rules behind why it feels right.
the-courage-to-delete: Use when a product, feature set, or roadmap feels crowded, diluted, or overcommitted.
vibe-checker: Use when a product, prototype, or workflow is usable enough but may feel tonally inconsistent or emotionally flat.

PROMPTS:
1. I wrote a PRD.md; James this before we ship.
2. Can you run James on docs/concept.md?
3. After that plan you wrote, ask James if it stands alone.
4. Invoke James on post-release-ideas.md; it can use older project docs.
5. James-review the design doc for hidden context.
6. I edited the strategy doc, please do the James loop.
7. $limitless:dojo build a new skill for reviewing docs.
8. I have an idea for an app that tracks launch readiness; show me what it would look like.
9. Write a PRD for my launch board idea.
10. Turn these notes into a Substack post.
11. What are people on Twitter saying about Fable5 today?
12. Look up the latest OpenAI API docs for Responses.
13. Make this article sound less AI-generated.
14. Review this code diff for bugs and regressions.
```
