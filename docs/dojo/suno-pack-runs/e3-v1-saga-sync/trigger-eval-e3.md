You are a skill-routing judge. Below is the list of installed skills
(name: description). For each user prompt, answer with the single skill
name you would invoke, or "none". Output one line per prompt:
"<n>: <skill-name>". No explanations.

SKILLS: identical to the list in /tmp/dojo-suno/trigger-eval-prompt.md (Read that file first for the full list), with ONE replacement — the limitless:suno-pack entry now reads:

- limitless:suno-pack: This skill should be used when the user wants to create music with Suno (AI music generation) — a song, track, beat, anthem, jingle, or instrumental — or wants to execute an existing suno-pack for real via the suno-pp-cli integration. Produces a complete track package (concept document, per-model-version style and lyrics prompts, instrumental variants, a cover/re-render workflow file, and runnable per-prompt scripts), and can render packs into actual tracks, run cover pipelines, check the local Suno library, and run one-roll experiment lanes. Supports version selection via arguments like "--versions 5.5 4.5" and experiment mode via "--mode experimental". Responds to "suno-pack", "make a track in Suno", "write me a song", "Suno prompt", "lyrics for Suno", "instrumental version", "render the pack", "generate it for real", "make it real", "run the cover pipeline", "how are my Suno tracks doing", "suno experiment", "surprise me with a Suno experiment", "sync the journal", "sync my suno pack", "rebuild the experiment saga", or any request to turn an idea, mood, or theme into Suno-ready prompts or finished Suno tracks.

Additionally these skills are installed (they were in the original list; repeated here for emphasis):
- codies-memory:memory-close-session: Used at end of session, when wrapping up work, or when the user says 'close session', 'end session', 'session summary', 'sign off'.
- codies-memory:memory-capture: Used when the agent needs to save something to memory — observations, lessons, decisions, reflections, dreams. Responds to 'remember this', 'capture', 'save to memory', 'I learned'.
- codies-memory:memory-promote: Used when the agent needs to evaluate or promote memory records through the trust pipeline. Responds to 'promote', 'evaluate inbox', 'elevate trust', or when inbox items need triage.

PROMPTS:
1. sync the journal for my pack
2. rebuild the experiment saga from my library
3. sync my suno pack with what I rolled in the web UI
4. update the journal from my suno likes
5. wrap up this session and save what we did
6. sync my research notes with the latest sources
7. check if there's anything in memory that needs attention
8. write a journal entry about what I learned today
