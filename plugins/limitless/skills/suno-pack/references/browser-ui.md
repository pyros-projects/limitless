# Browser Route — Claude in Chrome on the User's Own Session

For Claude only, when the Claude in Chrome tools (`mcp__claude-in-chrome__*`)
are available. They drive the user's real, logged-in Chrome. Verified
2026-10-03: a v6 generation with Variety Off, Personalize Off, Weirdness 35,
Style Influence 75, Duration 3:00 — no captcha challenge, durations 179.6 s
and 179.96 s, stored tags byte-identical to the sent style.

## When to take it

- `suno doctor` reports `captcha_preflight: required: true` (or a CLI call
  returned `captcha_required`) and the user approved the render.
- The request is about a control the CLI cannot set: Variety above Off,
  Personalize / My Taste, a Duration the user asked for, Lyrics Mode
  Mumble, Remaster strength, Max Mode or Variety on a cover,
  image/video/MIDI/playlist inputs. (Variety Off itself needs no browser:
  CLI renders keep the style as sent — observed 2026-10-03.)
- Otherwise prefer the CLI route — it is faster and leaves receipts.

**Never** use a CDP-launched automation browser (agent-browser, Playwright,
Chrome for Testing) for generation: it reports `navigator.webdriver = true`
and Suno's Turnstile loops forever (observed 2026-10-03). Never add stealth
flags or spoof automation markers to get past it. Never click a captcha:
if Turnstile shows "Verify you are human", ask the user to click it and
wait.

## Agents without Claude in Chrome

Use the paste route: tell the user to open suno.com/create → Advanced and
paste the prompt file top to bottom, with the exact settings below. After
they render, saga sync picks the clips up from the library.

## Procedure

1. `tabs_context_mcp` (create the group if empty) → navigate the group's
   tab to `https://suno.com/create`; wait ~4 s. If a cookie banner shows,
   choose the most privacy-preserving option (Reject All).
2. Confirm the session: the sidebar shows the user's handle and the credit
   chip (e.g. `2.7k`). Not logged in → ask the user to log in themselves.
3. Click **Advanced** (tabs: Simple / Advanced; Songs / Speech / Sounds).
   Check the model chip (top right of the form) shows the Settings model;
   change it via that dropdown when needed.
4. Fill the fields:
   - **Lyrics** — a contenteditable editor (`aria-label="Lyrics editor"`):
     click into it and type the Lyrics block verbatim.
   - **Styles** — the textarea whose placeholder is a suggestion list:
     set it with the native value setter plus an `input` event
     (`Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value').set.call(el, text); el.dispatchEvent(new Event('input',{bubbles:true}))`).
   - **More Options** (expand) → `Exclude styles` input, then **Song Title**
     input — same setter pattern for inputs.
   - Never click the blue wand next to Styles ("Personalize style prompt to
     match your taste") — it rewrites the style text.
5. More Options rows (labels as shown in the UI):
   | Row | Control | How |
   |---|---|---|
   | Vocal Gender | Male / Female buttons | click; leave both off for instrumentals or with a Voice |
   | Duration | Custom / Auto; Custom shows a slider 10–360 s (default 180 = 3:00) | click Custom, then set the slider |
   | Max Mode | Off / On | click |
   | Weirdness | slider 0–100 (default 50) | keyboard |
   | Style Influence | slider 0–100 (default 50) | keyboard |
   | Variety | slider 0–4: 0 Off "Exact style", 1 Normal (default), 2 High, 3 Extra, 4 Max | keyboard |
   | Personalize | My Taste Off / On (acts only when Variety > Off) | click |

   **Sliders ignore synthetic mouse clicks.** Set them by focusing the
   visible `[role=slider][aria-label="<name>"]` element and dispatching
   `keydown` ArrowLeft/ArrowRight one step at a time (step 1; Duration step
   = seconds) until `aria-valuenow` matches. The DOM holds a second hidden
   Variety slider — always take the visible one (`offsetParent !== null`).
6. **Verify before spending:** zoom-screenshot the form (lyrics tail,
   style, the More Options panel) and compare every value with the
   Settings block. Fix mismatches first.
7. **Spend only after the yes**, cost stated (10 credits, 20 with Max
   Mode). Click **Create**. If Turnstile appears, ask the user to solve it.
8. New rows appear under "Today" with the model label (`V6`, `V6-WILD`).
   Get the clip ids with `suno list --json` / `suno search "<title>"`
   (or pp-cli library reads), wait for `complete` (`suno status <ids>
   --wait`), then download and log exactly as in `suno-cli.md` with
   `"route": "browser"` and every UI setting in `settings`.
9. Close the tab you used when done, unless the user wants it open.
