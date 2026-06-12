You are a skill-routing judge for an agent harness. Below is the list of installed skills with their trigger descriptions (a relevant subset of the full install; other skills exist for documents/slides/code-review but none of them touch research/social/music/web). For EACH numbered user prompt, output exactly one line: `<number>. <skill-name>` choosing the single skill the router should invoke, or `none` if no listed skill should trigger. No explanations.

INSTALLED SKILLS:

- hivemind: This skill should be used when the user wants to know what the collective brain — social media (X/Twitter and Reddit), GitHub, the web, or research papers — is saying, building, or publishing about a topic — trends, sentiment, hot takes, trending repos, paper-vs-practitioner checks. Also runs recurring sweeps saved as configs. Responds to "ask the hivemind", "what's the hot shit in", "what does social media say", "what does reddit/twitter/X think", "what are people saying about", "check the socials", "--radar", "trending repos and what is X saying about them", "which repos get the most mentions", "what does the research say — and do practitioners agree", "repeat <slug>", "wiederhole den Sweep", "freeze this process", "frier den Prozess ein", or any question whose best answer lives in threads, comments, replies, repos, and preprints rather than articles. NOT for single-item lookups ("find me a paper on X", "search the web for Y") — use search/research skills. Read-only research — never posts.

- searxng: This skill should be used when the agent needs to perform web searches, look up current information online, or gather search results from the internet. Provides privacy-respecting web search through a self-hosted SearXNG instance with structured JSON output. Responds to "search the web for", "look this up online", "find recent articles about", "what does Google say about", "web search", or any task requiring live internet search results.

- codies-research: This skill should be used when the user needs live research, source verification, fact-checking, current comparisons, or updates to an existing research note. Responds to "look this up", "what's the latest on X", "compare X vs Y", "is this actually true", "fact check this", "update my research notes", or any question requiring evidence-grounded answers with strong next-step branching for deeper investigation.

- article-pack: This skill should be used when the user wants to create publishable content such as articles, blog posts, social media kits, slide decks, newsletters, or podcast transcripts. Responds to "article-pack", "write me an article", "Substack post", "turn my notes into a blog post", or any request to research a topic and produce publishable material from it.

- suno-pack: This skill should be used when the user wants to create music with Suno — a song, track, beat, anthem, jingle, or instrumental — or execute an existing suno-pack via CLI integration. Responds to "suno-pack", "make a track in Suno", "write me a song", "lyrics for Suno", "render the pack", "how are my Suno tracks doing".

- dojo: This skill should be used when the user wants to create, improve, test, or evaluate a Claude Code skill. Responds to "dojo", "new skill", "test this skill", "skill evals", "why isn't my skill triggering".

- surface-first-development: This skill should be used when the user wants to build, prototype, or reshape an app, tool, CLI, API, automation, or feature by starting from the interaction surface first. Responds to "let's build", "prototype this", "what would the UX be", "click dummy", or any request where the user describes what something should do without specifying architecture.

- deep-research: Deep research harness — fan-out web searches, fetch sources, adversarially verify claims, synthesize a cited report. When the user wants a deep, multi-source, fact-checked research report on any topic.

- wd-research: Use when the user needs live research, source verification, current comparisons, updates to an existing research note, or evidence-grounded next directions for deeper investigation (white duck work context).

- wd-local-websearch: Search the web using SearXNG, a self-hosted privacy-respecting metasearch engine (white duck work context). Use as primary search tool.

USER PROMPTS:

1. ask the hivemind: what's the deal with MCP elicitation?
2. what's the hot shit in local image models right now?
3. repeat ai-dev-weekly
4. wiederhole den Sweep von letzter Woche
5. good sweep — freeze this process, I want it monthly
6. what are the trending GitHub repos in agent tooling and what is X saying about them?
7. which repos get the most mentions on r/LocalLLaMA this month?
8. what does the research say about context compression — and do practitioners on reddit agree?
9. review this repo for security issues
10. find me a paper on retrieval-augmented generation
11. search the web for the OpenAlex API rate limits
12. is it actually true that Suno v5.5 handles glitch-hop better?
13. write me an article about agent memory systems
14. what would the UX of a weekly research digest app look like?
15. I want a deep, fact-checked research report on EU AI Act enforcement
