/* Badge evaluation - the JS twin of engine/badges.py (SPEC.md §3).
 * Rules are data (docs/data/badges.json); unknown kinds never fire. */
(function (global) {
  "use strict";

  function epoch(ts) {
    return Date.parse(ts) / 1000;
  }

  function moduleCompletionTs(state) {
    var out = {};
    for (var i = 0; i < state.completed.length; i++) {
      out[state.completed[i].module] = state.completed[i].ts;
    }
    return out;
  }

  function earnedTs(rule, state) {
    var kind = rule && rule.kind;
    var events = state.events, done = state.done;
    var i, ids;

    if (kind === "first_event") {
      for (i = 0; i < state.counted.length; i++) {
        if (state.counted[i].type === "pass") return state.counted[i].ts;
      }
      return null;
    }
    if (kind === "exercise") {
      return done[rule.id] ? done[rule.id].ts : null;
    }
    if (kind === "exercises_all") {
      ids = rule.ids || [];
      if (!ids.length) return null;
      var max = "";
      for (i = 0; i < ids.length; i++) {
        if (!done[ids[i]]) return null;
        if (done[ids[i]].ts > max) max = done[ids[i]].ts;
      }
      return max;
    }
    if (kind === "modules_all") {
      var byMod = moduleCompletionTs(state);
      ids = rule.ids || [];
      if (!ids.length) return null;
      var maxTs = "";
      for (i = 0; i < ids.length; i++) {
        if (!byMod[ids[i]]) return null;
        if (byMod[ids[i]] > maxTs) maxTs = byMod[ids[i]];
      }
      return maxTs;
    }
    if (kind === "devices") {
      var need = rule.count || 2, seen = {}, n = 0;
      for (i = 0; i < events.length; i++) {
        if (!seen[events[i].device]) { seen[events[i].device] = 1; n++; }
        if (n >= need) return events[i].ts;
      }
      return null;
    }
    if (kind === "gap_return") {
      var gap = (rule.days || 7) * 86400;
      var prev = null;
      for (i = 0; i < events.length; i++) {
        var t = epoch(events[i].ts);
        if (prev !== null && t - prev >= gap) return events[i].ts;
        prev = prev === null ? t : Math.max(prev, t);
      }
      return null;
    }
    return null; // unknown kind
  }

  function evaluate(defs, state) {
    var earned = [];
    for (var i = 0; i < defs.length; i++) {
      var ts = earnedTs(defs[i].rule || {}, state);
      if (ts !== null) {
        var row = {};
        for (var k in defs[i]) if (k !== "rule") row[k] = defs[i][k];
        row.earned_ts = ts;
        earned.push(row);
      }
    }
    earned.sort(function (a, b) {
      return a.earned_ts < b.earned_ts ? -1 : a.earned_ts > b.earned_ts ? 1 : 0;
    });
    return earned;
  }

  function nextTeasers(defs, state, limit) {
    limit = limit || 3;
    var have = {};
    var earned = evaluate(defs, state);
    for (var i = 0; i < earned.length; i++) have[earned[i].key] = 1;
    var out = [];
    for (i = 0; i < defs.length && out.length < limit; i++) {
      if (!have[defs[i].key]) {
        out.push({
          key: defs[i].key, name: defs[i].name, tier: defs[i].tier,
          icon: defs[i].icon, desc: defs[i].desc,
        });
      }
    }
    return out;
  }

  global.CodinBadges = { evaluate: evaluate, nextTeasers: nextTeasers };
})(typeof window !== "undefined" ? window : globalThis);
