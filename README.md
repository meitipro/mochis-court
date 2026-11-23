# Mochi's Court

A 2-minute browser game about GenLayer-style consensus. You are one validator on a four-validator jury.
Educational simulation, not financial advice. GEN in the game is play money.

## Open it
Double-click `index.html`. One file, no build step, no network calls (the JetBrains Mono web font is optional; a monospace fallback is used offline).

- Keys: Left = Side with A, Right = Side with B, Enter = continue, A = appeal.
- `?demo=1` auto-plays a scripted ~16 s run (3 cases, one appeal that flips) with a visible tap cursor, for screen recording.
- `?seed=7` makes the random case order repeatable.

## Edit the cases
Open `index.html`, find `const CASES = [` and edit the array. Each case:

```js
{ id, title, deal, claimA, claimB, evidence,
  validators: ["A","A","B"],      // Model Alpha, Beta, Gamma
  explanation: "one-line why",
  appealVotes: ["B","B","A"] }    // 3 extra validators if the player appeals (7 votes total)
```
- Unanimous `validators` = clear-cut. A 2-1 split shows the "Split jury" tag.
- To make an appeal flip a verdict, choose `appealVotes` so the 7-vote majority differs from the first verdict (see cases 19 and 20).
- Tie rule (a game rule, not a GenLayer claim): if player + 3 validators tie 2-2, the validators' earlier majority stands.
- Currently 14 clear, 4 split (15-18), 2 appeal-flip (19, 20).

## Rebuild from sources
`build/template.html` is the source; `build/prep.py` embeds the images (needs Pillow and the mascot PNGs), `build/build.py` writes `index.html`.
To use the real GenLayer logo PNG, save it as `build/GenLayer_Logo_White_2048.png` and re-run `prep.py` then `build.py`.
`build/test.py` and `build/demo_test.py` are the Playwright checks that produced `screenshots/`.

## Credits
Mochi and stickers: genlayer-foundation/genlayer-mascot (CC0). Logo and art are unmodified apart from downscaling.
