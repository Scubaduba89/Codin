/* Load everything a page needs, replay through the shared engine.
 * All URLs are relative (GitHub Pages serves this repo at a subpath). */
"use strict";

async function loadWorld() {
  const v = "?v=" + Date.now(); // bust Pages' cache after a push
  const j = (p, fallback) =>
    fetch(p + v).then((r) => {
      if (!r.ok) throw new Error(p);
      return r.json();
    }).catch(() => fallback);

  const [logText, curriculum, badgeDefs, profile] = await Promise.all([
    fetch("data/events.jsonl" + v).then((r) => (r.ok ? r.text() : "")),
    j("data/curriculum.json", { modules: [] }),
    j("data/badges.json", []),
    j("data/profile.json", {}),
  ]);

  const parsed = CodinRules.parseLines(logText.split("\n"));
  const state = CodinRules.replay(parsed.events, curriculum);
  const earned = CodinBadges.evaluate(badgeDefs, state);
  return {
    state, curriculum, badgeDefs, earned, profile,
    ignored: parsed.ignored,
  };
}
