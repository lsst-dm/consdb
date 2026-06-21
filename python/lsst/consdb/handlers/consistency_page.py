# This file is part of consdb.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Static HTML page for the table consistency report.

The page is served at ``{url_prefix}/table_consistency`` and is a
self-contained HTML/CSS/JS document with no external dependencies.  In the
browser it fetches the sibling JSON endpoint
``{url_prefix}/table_consistency/{instrument}/{day_obs}``
on the same origin, so the Gafaelfawr session cookie is sent automatically.

The HTML is embedded as a string (rather than read from a file at runtime) so
it works identically whether the package is imported as
``lsst.consdb.handlers`` in development or flattened into
``consdb_pq.handlers`` inside the pqserver container.
"""

TABLE_CONSISTENCY_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ConsDB table consistency</title>
<style>
  :root { color-scheme: light dark; }
  body {
    font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
    margin: 0 auto; max-width: 1000px; padding: 1.5rem; line-height: 1.45;
  }
  h1 { font-size: 1.4rem; margin: 0 0 0.25rem; }
  p.sub { margin: 0 0 1.25rem; color: #666; font-size: 0.9rem; }
  .controls { display: flex; flex-wrap: wrap; gap: 0.5rem; align-items: flex-end; margin-bottom: 1rem; }
  .controls label { display: flex; flex-direction: column; font-size: 0.8rem; gap: 0.2rem; }
  .controls select, .controls input { padding: 0.4rem 0.5rem; font-size: 0.95rem; }
  .controls button { padding: 0.45rem 1rem; font-size: 0.95rem; cursor: pointer; }
  #status { margin: 0.75rem 0; font-size: 0.95rem; }
  #status.ok { color: #1a7f37; }
  #status.warn { color: #9a6700; }
  #status.error { color: #b42318; }
  #summary { margin: 0.5rem 0 1rem; font-size: 0.95rem; }
  details { border: 1px solid #ccc; border-radius: 6px; margin: 0.5rem 0; padding: 0.25rem 0.75rem; }
  summary { cursor: pointer; font-weight: 600; padding: 0.35rem 0; }
  summary code { font-weight: 600; }
  .badge {
    display: inline-block; font-size: 0.68rem; text-transform: uppercase;
    letter-spacing: 0.03em; padding: 0.1rem 0.4rem; border-radius: 999px;
    margin-right: 0.5rem; vertical-align: 0.08em; color: #fff;
  }
  .badge.structural { background: #b42318; }
  .badge.coverage { background: #9a6700; }
  .count { color: #666; font-weight: 400; }
  table { border-collapse: collapse; width: 100%; margin: 0.5rem 0; font-size: 0.9rem; }
  th, td { border-bottom: 1px solid #ddd; padding: 0.35rem 0.5rem; text-align: left; vertical-align: top; }
  th { font-weight: 600; }
  td.seq { font-variant-numeric: tabular-nums; white-space: nowrap; width: 6rem; }
</style>
</head>
<body>
  <h1>ConsDB table consistency</h1>
  <p class="sub">Consistency-rule violations for one instrument and observing day.</p>

  <form class="controls" id="form">
    <label>Instrument
      <select id="instrument">
        <option value="lsstcam">lsstcam</option>
        <option value="latiss">latiss</option>
      </select>
    </label>
    <label>Observing day (YYYYMMDD)
      <input id="day_obs" type="text" inputmode="numeric" pattern="[0-9]{8}" size="10">
    </label>
    <button type="submit">Check</button>
  </form>

  <div id="status"></div>
  <div id="summary"></div>
  <div id="results"></div>

<script>
(function () {
  "use strict";

  var STRUCTURAL = {
    ccdexposure_completeness: true,
    exposure_id_encoding: true,
    ccdexposure_key_agreement: true,
    no_guider_products: true
  };

  var form = document.getElementById("form");
  var instrumentEl = document.getElementById("instrument");
  var dayObsEl = document.getElementById("day_obs");
  var statusEl = document.getElementById("status");
  var summaryEl = document.getElementById("summary");
  var resultsEl = document.getElementById("results");

  function setStatus(text, kind) {
    statusEl.textContent = text;
    statusEl.className = kind || "";
  }

  function clearOutput() {
    summaryEl.textContent = "";
    resultsEl.textContent = "";
  }

  function apiUrl(instrument, dayObs) {
    var base = window.location.pathname;
    while (base.charAt(base.length - 1) === "/") {
      base = base.slice(0, -1);
    }
    return base + "/" + encodeURIComponent(instrument) + "/" + encodeURIComponent(dayObs);
  }

  function groupByRule(rows) {
    var groups = {};
    rows.forEach(function (row) {
      var rule = row.rule;
      if (!groups[rule]) { groups[rule] = []; }
      groups[rule].push(row);
    });
    return groups;
  }

  function render(rows, instrument, dayObs) {
    clearOutput();
    if (rows.length === 0) {
      setStatus("No violations for " + instrument + " on " + dayObs + ".", "ok");
      return;
    }

    var groups = groupByRule(rows);
    var ruleNames = Object.keys(groups).sort();
    setStatus(
      rows.length + " violation" + (rows.length === 1 ? "" : "s") +
      " across " + ruleNames.length + " rule" + (ruleNames.length === 1 ? "" : "s") +
      " for " + instrument + " on " + dayObs + ".",
      "warn"
    );

    ruleNames.forEach(function (rule) {
      var items = groups[rule];
      var details = document.createElement("details");

      var summary = document.createElement("summary");
      var badge = document.createElement("span");
      var structural = STRUCTURAL[rule] === true;
      badge.className = "badge " + (structural ? "structural" : "coverage");
      badge.textContent = structural ? "structural" : "coverage";
      summary.appendChild(badge);
      var code = document.createElement("code");
      code.textContent = rule;
      summary.appendChild(code);
      var count = document.createElement("span");
      count.className = "count";
      count.textContent = "  —  " + items.length +
        " exposure" + (items.length === 1 ? "" : "s");
      summary.appendChild(count);
      details.appendChild(summary);

      var table = document.createElement("table");
      var thead = document.createElement("thead");
      var hrow = document.createElement("tr");
      ["seq_num", "detail"].forEach(function (h) {
        var th = document.createElement("th");
        th.textContent = h;
        hrow.appendChild(th);
      });
      thead.appendChild(hrow);
      table.appendChild(thead);

      var tbody = document.createElement("tbody");
      items.sort(function (a, b) { return a.seq_num - b.seq_num; });
      items.forEach(function (row) {
        var tr = document.createElement("tr");
        var seq = document.createElement("td");
        seq.className = "seq";
        seq.textContent = row.seq_num;
        tr.appendChild(seq);
        var detail = document.createElement("td");
        detail.textContent = row.detail;
        tr.appendChild(detail);
        tbody.appendChild(tr);
      });
      table.appendChild(tbody);
      details.appendChild(table);
      resultsEl.appendChild(details);
    });
  }

  function check(instrument, dayObs) {
    clearOutput();
    setStatus("Loading…", "");
    var qs = "?instrument=" + encodeURIComponent(instrument) +
      "&day_obs=" + encodeURIComponent(dayObs);
    history.replaceState(null, "", window.location.pathname + qs);

    fetch(apiUrl(instrument, dayObs), {
      headers: { "Accept": "application/json" },
      credentials: "same-origin",
      redirect: "manual"
    }).then(function (response) {
      if (response.type === "opaqueredirect" ||
          response.status === 401 || response.status === 403) {
        setStatus(
          "Your session has expired or you are not signed in. Reload the page to sign in again.",
          "error"
        );
        return null;
      }
      if (!response.ok) {
        return response.text().then(function (text) {
          setStatus("Error " + response.status + ": " + text, "error");
          return null;
        });
      }
      return response.json();
    }).then(function (data) {
      if (data === null) { return; }
      if (!Array.isArray(data)) {
        setStatus("Unexpected response from the server.", "error");
        return;
      }
      render(data, instrument, dayObs);
    }).catch(function (err) {
      setStatus("Request failed: " + err.message, "error");
    });
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    var instrument = instrumentEl.value;
    var dayObs = dayObsEl.value.trim();
    if (!/^[0-9]{8}$/.test(dayObs)) {
      setStatus("Enter an observing day as 8 digits, for example 20250424.", "error");
      return;
    }
    check(instrument, dayObs);
  });

  function defaultDayObs() {
    // The current observing night's day_obs, rolling over at 16:00 Chile time
    // (America/Santiago, so DST is handled): before 16:00 CLT this is the
    // previous night, at or after 16:00 it is the night now beginning.
    var parts = new Intl.DateTimeFormat("en-US", {
      timeZone: "America/Santiago",
      year: "numeric", month: "2-digit", day: "2-digit",
      hour: "2-digit", minute: "2-digit", second: "2-digit",
      hour12: false
    }).formatToParts(new Date());
    var wall = {};
    parts.forEach(function (p) { wall[p.type] = p.value; });
    // Represent the Chile wall-clock time as a UTC instant, then shift back
    // 16 hours so the calendar date flips at 16:00 CLT.
    var asUtc = Date.UTC(
      parseInt(wall.year, 10),
      parseInt(wall.month, 10) - 1,
      parseInt(wall.day, 10),
      parseInt(wall.hour, 10) % 24,
      parseInt(wall.minute, 10),
      parseInt(wall.second, 10)
    );
    var rolled = new Date(asUtc - 16 * 3600 * 1000);
    var month = ("0" + (rolled.getUTCMonth() + 1)).slice(-2);
    var day = ("0" + rolled.getUTCDate()).slice(-2);
    return "" + rolled.getUTCFullYear() + month + day;
  }

  // Initialise from the query string, defaulting to the previous night, and
  // show that result immediately.
  var params = new URLSearchParams(window.location.search);
  var qInstrument = params.get("instrument");
  var qDayObs = params.get("day_obs");
  if (qInstrument) {
    for (var i = 0; i < instrumentEl.options.length; i++) {
      if (instrumentEl.options[i].value === qInstrument) {
        instrumentEl.value = qInstrument;
        break;
      }
    }
  }
  dayObsEl.value = (qDayObs && /^[0-9]{8}$/.test(qDayObs)) ? qDayObs : defaultDayObs();
  check(instrumentEl.value, dayObsEl.value);
})();
</script>
</body>
</html>
"""
