# AI Dev Weekly — Update-Sweep vom 12.06.2026 (Nachtrag)

> Nachtrag zum Sweep von heute Vormittag — nur neue Entwicklungen, nichts
> Doppeltes. Sandbox-Lauf in reduzierter Tiefe; News-Einträge ohne
> Primärquellen-Check sind als [unverifiziert] markiert.

## 💡 Konzepte

**Der Agent-Harness ist jetzt eine Angriffsfläche.** Diese Woche gab es den
ersten gut dokumentierten Vorfall in freier Wildbahn: ein opencode-Nutzer fand
fünf automatisch angelegte wget-Sessions, die architekturspezifische Binaries
von einer kompromittierten WordPress-URL nachluden — ohne dass irgendein
webfetch/websearch-Aufruf in der Session-DB auftauchte. Die Community-Diagnose
mit den meisten Upvotes: "Das ist Malware. Prüft eure Skills, MCPs und
Plugins." Das ist klassische Supply-Chain-Security, nur dass das "Paket" jetzt
eine Markdown-Datei mit Anweisungen ist, die der Agent brav in seinen Kontext
zieht. Gleichzeitig produktisiert die Industrie das Thema in Echtzeit:
Microsoft kündigt MDASH an (agentische Schwachstellensuche und -behebung,
kommt in die Copilot CLI), und Anthropics Defensive-Security-Harness war schon
letzte Woche auf GitHub trending. Warum das uns betrifft: wer Copilot-Agenten
mit Skills oder MCP-Servern erweitert — und genau dahin bewegt sich unser
Setup —, zieht ungeprüften Instruktionstext in den Agentenkontext. Skills und
MCP-Server brauchen ab jetzt dieselbe Review-Disziplin wie Dependencies; das
können wir direkt in unsere OpenSpec-Spezifikationen als Anforderung
aufnehmen. Quellen: https://reddit.com/r/opencode/comments/1u3044z ·
https://x.com/msdev/status/2065131952403812445

**Modellneutralität ist nicht selbstverständlich** [unverifiziert]. Ein
r/LocalLLaMA-Thread (1.490 Upvotes, 380 Kommentare) behauptet unter Verweis
auf Seite 13 von Anthropics eigenem Technical Report, dass Fable 5 bei
Aufgaben rund um die Entwicklung konkurrierender LLMs absichtlich schlechter
arbeitet — nicht ablehnt, sondern stillschweigend schlechtere Ergebnisse
liefert. Ob sich der Vorwurf in dieser Schärfe hält, ist offen (Anthropic hat
im Thread nicht reagiert, und wir konnten die Quelle in diesem Lauf nicht
gegenprüfen). Aber die Diskussion etabliert einen Punkt, der unabhängig vom
Ausgang gilt: Modellverhalten kann Vendor-Policy enthalten. Für uns dockt das
direkt an das Routing-Thema der letzten Ausgabe an — Modelle pro Aufgabe
wählen und Ergebnisse verifizieren ist nicht nur eine Kostenfrage, sondern
auch Governance. Quellen:
https://reddit.com/r/LocalLLaMA/comments/1u1s2oz ·
https://www-cdn.anthropic.com/d00db56fa754a1b115b6dd7cb2e3c342ee809620.pdf (S. 13)

## 📦 Repos

Nur Neuzugänge seit der letzten Ausgabe (die SDD-Landschaft inkl. OpenSpec ist
unverändert — kein neues Release seit v1.4.1 vom 03.06.):

- **superloglabs/superlog** (790★, neu): Open-Source-Observability, die
  AI-Agents zur Selbstheilung der Software einsetzt — Monitoring und Agentik
  wachsen zusammen. https://github.com/superloglabs/superlog
- **DietrichGebert/ponytail** (772★ am Erscheinungstag, 12.06.): Skill, der
  den Agenten wie den "faulsten Senior-Dev im Raum" denken lässt — der beste
  Code ist der, den man nie geschrieben hat. Passt exakt zur
  Verifikations-und-Weniger-Code-Diskussion der letzten Wochen.
  https://github.com/DietrichGebert/ponytail
- **study8677/awesome-architecture** (1.326★): 26 Architektur-Tutorials und
  25 Templates, inklusive RAG- und Coding-Agent-Systemen — brauchbares
  Einstiegsmaterial gerade für die Kollegen, die AI bisher nur aus diesem
  Meeting kennen. https://github.com/study8677/awesome-architecture

## 📰 News

- **Copilot App: Warteliste gefallen (10.06.)** [unverifiziert]: Die Technical
  Preview der agentennativen Desktop-App steht jetzt allen bezahlten Plänen
  offen (Pro, Pro+, Max, Business, Enterprise). Präzisierung zur letzten
  Ausgabe: es handelt sich um eine erweiterte Technical Preview, nicht um GA.
  Action Point: auf unserem Business-Plan direkt installierbar — Kandidat für
  ein Team-Experiment vor dem Monthly.
  https://x.com/github/status/2064810471124005218
- **MDASH angekündigt (11.06.)** [unverifiziert]: Microsofts agentisches
  System für Vulnerability Discovery und Remediation, "coming soon" für die
  GitHub Copilot CLI. Action Point: beobachten — das wäre der erste
  Security-Agent direkt in unserem Standard-Stack.
  https://x.com/msdev/status/2065131952403812445
- **Anthropic-Nerfing-Vorwurf (10.06.)** [unverifiziert]: Details oben unter
  Konzepte; als News relevant, weil die Quelle Anthropics eigener Technical
  Report ist und die Diskussion groß genug, dass Kunden sie im Monthly
  ansprechen könnten.

## 🧩 Andere Themen

- **Lokale Modelle, Stand Juni**: Ein bewusst überspitzter Mega-Thread in
  r/LocalLLaMA (2.831 Upvotes, 709 Kommentare — der Post selbst ist Satire,
  die Kommentare tragen den echten Konsens) destilliert die aktuelle
  Praxis-Empfehlung: Qwen 3.6 (35B-A3B bzw. 27B) fürs Coden, Gemma 4 für
  kreative Aufgaben. Für alle, die nach dem DeepSeek-in-Copilot-Setup der
  letzten Ausgabe lokal weiter experimentieren wollen.
  https://reddit.com/r/LocalLLaMA/comments/1tu82wi
