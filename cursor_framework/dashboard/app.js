/* Cursor Framework Dashboard - app logic.
   Loads /api/index + /api/stats every 3s, renders bento stats + categories.
   Wires copy-to-clipboard on every command card.
   Manages tab switching between Dashboard and Graph views. */

(function () {
  "use strict";

  // -------- Config --------
  var REFRESH_MS = 3000;
  var TOKEN = new URLSearchParams(location.search).get("token") || "";
  var authHeaders = TOKEN ? { "X-Auth-Token": TOKEN } : {};

  // -------- Tab state --------
  var currentTab = "dashboard";
  var graphInitialized = false;

  function switchTab(tab) {
    if (tab === currentTab) return;
    currentTab = tab;

    var dashPanel = document.getElementById("panel-dashboard");
    var contextPanel = document.getElementById("panel-context");
    var graphPanel = document.getElementById("panel-graph");
    var dashTab = document.getElementById("tab-dashboard");
    var contextTab = document.getElementById("tab-context");
    var graphTab = document.getElementById("tab-graph");

    if (tab === "dashboard") {
      dashPanel.style.display = "";
      if (contextPanel) contextPanel.style.display = "none";
      graphPanel.style.display = "none";
      dashTab.classList.add("is-active");
      dashTab.setAttribute("aria-selected", "true");
      if (contextTab) {
        contextTab.classList.remove("is-active");
        contextTab.setAttribute("aria-selected", "false");
      }
      graphTab.classList.remove("is-active");
      graphTab.setAttribute("aria-selected", "false");
    } else if (tab === "context") {
      dashPanel.style.display = "none";
      if (contextPanel) contextPanel.style.display = "";
      graphPanel.style.display = "none";
      if (contextTab) {
        contextTab.classList.add("is-active");
        contextTab.setAttribute("aria-selected", "true");
      }
      dashTab.classList.remove("is-active");
      dashTab.setAttribute("aria-selected", "false");
      graphTab.classList.remove("is-active");
      graphTab.setAttribute("aria-selected", "false");
    } else {
      dashPanel.style.display = "none";
      if (contextPanel) contextPanel.style.display = "none";
      graphPanel.style.display = "";
      graphTab.classList.add("is-active");
      graphTab.setAttribute("aria-selected", "true");
      dashTab.classList.remove("is-active");
      dashTab.setAttribute("aria-selected", "false");
      if (contextTab) {
        contextTab.classList.remove("is-active");
        contextTab.setAttribute("aria-selected", "false");
      }
      if (!graphInitialized && typeof window._initGraph === "function") {
        graphInitialized = true;
        window._initGraph();
      }
    }
  }

  function initTabs() {
    // Tab nav links switch panels without page navigation.
    document.querySelectorAll(".tab-nav__item").forEach(function (link) {
      link.addEventListener("click", function (e) {
        e.preventDefault();
        var href = link.getAttribute("href");
        if (href === "#dashboard") switchTab("dashboard");
        else if (href === "#context") switchTab("context");
        else if (href === "#graph") switchTab("graph");
      });
    });

    // Check hash on load.
    var hash = window.location.hash;
    if (hash === "#graph") switchTab("graph");
    else if (hash === "#context") switchTab("context");
  }

  // -------- Network --------
  async function load(url) {
    const sep = url.includes("?") ? "&" : "?";
    const full = url + (TOKEN ? sep + "token=" + encodeURIComponent(TOKEN) : "");
    try {
      const r = await fetch(full, { cache: "no-store", headers: authHeaders });
      if (!r.ok) return null;
      return await r.json();
    } catch (err) {
      console.error("[dashboard] fetch failed", url, err);
      return null;
    }
  }

  // -------- Formatters --------
  const fmt = (n) => Number(n || 0).toLocaleString("en-US");
  const escapeHtml = (s) =>
    String(s).replace(/[&<>"']/g, (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])
    );

  // -------- Icons (inline SVG; one-stroke, 1.5 weight) --------
  const ICONS = {
    package: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 8L12 3 3 8v8l9 5 9-5V8z"/><path d="M3 8l9 5 9-5"/><path d="M12 13v8"/></svg>`,
    layers: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>`,
    book: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>`,
    zap: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>`,
    terminal: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/></svg>`,
    cpu: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/></svg>`,
    database: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14a9 3 0 0 0 18 0V5"/><path d="M3 12a9 3 0 0 0 18 0"/></svg>`,
    activity: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>`,
    folder: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>`,
    shield: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>`,
    spark: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 3v4M3 5h4M19 17v4M17 19h4M11 5l1.5 4.5L17 11l-4.5 1.5L11 17l-1.5-4.5L5 11l4.5-1.5L11 5z"/></svg>`,
    grid: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>`,
    link: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>`,
    trash: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-2 14a2 2 0 0 1-2 2H9a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6M14 11v6"/></svg>`,
    copy: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>`,
    graph: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="6" r="3"/><circle cx="18" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="18" r="3"/><line x1="9" y1="6" x2="15" y2="6"/><line x1="6" y1="9" x2="6" y2="15"/><line x1="18" y1="9" x2="18" y2="15"/><line x1="9" y1="18" x2="15" y2="18"/></svg>`,
  };

  // -------- Bento cards (top of page) --------
  // Visual structure: 1 hero (wide) + 4 small, in 4-col grid.
  // Order matches data priority: total → skills/rules/knowledge/commands
  function renderBento(idx, stats) {
    const t = (idx && idx.totals) || {};
    const max = Math.max(1, ...Object.values(t).filter((v) => typeof v === "number" && v > 0));
    const top = Object.entries(t)
      .filter(([k]) => k !== "grand_total")
      .sort((a, b) => b[1] - a[1])
      .slice(0, 4);

    const hero = `
      <div class="bento__card bento__card--wide">
        <div class="bento__label">${ICONS.package}Grand total assets</div>
        <div class="bento__value bento__value--hero tnum">${fmt(t.grand_total || 0)}</div>
        <div class="bento__hint">Indexed from <span class="mono">${escapeHtml(idx?.root || ".cursor")}</span> · ${escapeHtml(idx?.scanned_at || "never")}</div>
      </div>`;

    const top4 = top
      .map(([k, v]) => {
        const pct = Math.max(8, Math.round((v / max) * 100));
        const icon =
          { skills: ICONS.spark, rules: ICONS.shield, knowledge: ICONS.book, commands: ICONS.terminal,
            agents: ICONS.cpu, hooks: ICONS.zap, references: ICONS.folder,
            memory: ICONS.database, prompts: ICONS.activity, templates: ICONS.layers,
            scripts: ICONS.grid, workflows: ICONS.link }[k] || ICONS.folder;
        return `
          <div class="bento__card">
            <div class="bento__label">${icon}${escapeHtml(k)}</div>
            <div class="bento__value tnum">${fmt(v)}</div>
            <div class="bento__spark" aria-hidden="true">
              ${Array.from({ length: 12 }, (_, i) =>
                `<span class="bento__spark-bar" style="height:${Math.max(4, Math.round((pct / 12) * (i + 1) / 2 + (pct / 12) * (i + 1) / 2))}%"></span>`
              ).join("")}
            </div>
          </div>`;
      })
      .join("");

    return hero + top4;
  }

  // -------- Memory cards --------
  function renderMemory(stats) {
    const m = (stats && stats.memory) || {};
    return [
      { label: "Entries", value: m.entries, icon: ICONS.database },
      { label: "Hits", value: m.hits, icon: ICONS.activity, accent: "ok" },
      { label: "Misses", value: m.misses, icon: ICONS.activity, accent: "warn" },
      { label: "Tokens saved", value: m.tokens_saved, icon: ICONS.zap, accent: "accent" },
    ].map((c) => `
        <div class="bento__card">
          <div class="bento__label">${c.icon}${escapeHtml(c.label)}</div>
          <div class="bento__value tnum">${fmt(c.value)}</div>
          <div class="bento__hint">${c.accent === "ok" ? "cache warming up" : c.accent === "warn" ? "cold lookups (good to warm)" : "estimated cost reduction"}</div>
        </div>`).join("");
  }

  // -------- Session Context panel --------
  async function loadSessionContext() {
    const data = await load("/api/session");
    if (!data) return null;
    return data;
  }

  function renderSessionContext(sessionData) {
    if (!sessionData) {
      return {
        files: 0,
        tokens: 0,
        hitRate: 0,
        lookups: 0,
        recentFiles: []
      };
    }
    return {
      files: sessionData.files_read || 0,
      tokens: sessionData.total_tokens || 0,
      hitRate: sessionData.cache_hit_rate || 0,
      lookups: (sessionData.cache_hits || 0) + (sessionData.cache_misses || 0),
      recentFiles: sessionData.recent_files || []
    };
  }

  function updateSessionContextUI(data) {
    if (!data) return;

    const el = document.getElementById("ctx-files");
    if (el) el.textContent = fmt(data.files);

    const tokEl = document.getElementById("ctx-tokens");
    if (tokEl) tokEl.textContent = fmt(data.tokens);

    const rateEl = document.getElementById("ctx-hit-rate");
    if (rateEl) rateEl.textContent = data.hitRate + "%";

    const lookupsEl = document.getElementById("ctx-lookups");
    if (lookupsEl) lookupsEl.textContent = fmt(data.lookups);

    const recentEl = document.getElementById("recentFilesList");
    if (recentEl) {
      if (data.recentFiles && data.recentFiles.length > 0) {
        recentEl.innerHTML = data.recentFiles.map(function(f) {
          return "<div style=\"padding:4px 0;border-bottom:1px solid var(--border-soft);\">" +
                 "<span style=\"color:var(--fg-1);\">" + escapeHtml(f) + "</span></div>";
        }).join("");
      } else {
        recentEl.innerHTML = "<span style=\"color:var(--fg-2);\">No files read yet</span>";
      }
    }
  }

  // -------- Workflow runtime cards --------
  function renderWorkflow(stats) {
    const w = (stats && stats.workflow) || {};
    const entries = Object.entries(w);
    if (!entries.length) {
      return `<div class="bento__card bento__card--wide">
        <div class="bento__label">${ICONS.cpu}Workflow runtime</div>
        <div class="bento__hint" style="margin-top:var(--sp-3)">No live workflow attached. Run <code class="mono">cursor-framework warm</code> then restart <code class="mono">serve</code> to enable telemetry.</div>
      </div>`;
    }
    return entries
      .map(([k, v]) => `
        <div class="bento__card">
          <div class="bento__label">${ICONS.cpu}${escapeHtml(k.replace(/_/g, " "))}</div>
          <div class="bento__value tnum">${fmt(v)}</div>
        </div>`)
      .join("");
  }

  // -------- Categories table --------
  function renderCategories(idx) {
    const t = (idx && idx.totals) || {};
    const rows = Object.entries(t)
      .filter(([k]) => k !== "grand_total")
      .sort((a, b) => b[1] - a[1]);
    const max = Math.max(1, ...rows.map(([, v]) => v));
    if (!rows.length) return `<tr><td colspan="3" style="color:var(--fg-2)">No categories indexed yet.</td></tr>`;
    return rows
      .map(
        ([k, v]) => `
        <tr>
          <td>${escapeHtml(k)}</td>
          <td class="num">${fmt(v)}</td>
          <td><span class="bar" style="width:${Math.max(2, Math.round((v / max) * 280))}px"></span></td>
        </tr>`
      )
      .join("");
  }

  // -------- Usage guide (static; command reference) --------
  const COMMANDS = [
    { icon: "terminal", cmd: "cursor-framework serve", args: "[--port 8765]", desc: "Start this dashboard server. Open http://127.0.0.1:8765 in your browser." },
    { icon: "graph", cmd: "cursor-framework serve-graph", args: "[--port 8766]", desc: "Visualize the skill/agent dependency graph (D3 force-directed)." },
    { icon: "zap", cmd: "cursor-framework ask", args: '"your request"', desc: "Run the framework once: detect skills, build context, return JSON summary." },
    { icon: "spark", cmd: "cursor-framework warm", args: "", desc: "Force a full re-index and persist memory. Run after editing .cursor/." },
    { icon: "grid", cmd: "cursor-framework index", args: "--root .cursor", desc: "Scan .cursor/ and write INDEX.json + INDEX.md (machine + human index)." },
    { icon: "shield", cmd: "cursor-framework stats", args: "", desc: "Print current framework stats as JSON (memory hits, assets indexed, ...)." },
    { icon: "layers", cmd: "cursor-framework graph", args: "", desc: "Print the skill dependency graph as nodes/edges JSON to stdout." },
    { icon: "trash", cmd: "cursor-framework clear-cache", args: "[--force]", desc: "Wipe memory + INDEX files. Default is dry-run; --force actually deletes." },
    { icon: "folder", cmd: "cursor-framework scan", args: "--root .cursor", desc: "Quick scan that prints category totals without writing any file." },
    { icon: "package", cmd: "pip install -e .", args: "", desc: "Install the package in editable mode (run once from repo root)." },
  ];
  const ICON_KEYS = new Set(Object.keys(ICONS));
  function renderCommands() {
    return COMMANDS.map((c) => {
      const icon = ICON_KEYS.has(c.icon) ? ICONS[c.icon] : ICONS.terminal;
      const full = (c.cmd + " " + c.args).trim();
      return `
        <div class="cmd" data-cmd="${escapeHtml(full)}" role="button" tabindex="0">
          <div class="cmd__icon">${icon}</div>
          <div class="cmd__name">${escapeHtml(c.cmd)}<span class="arg"> ${escapeHtml(c.args)}</span></div>
          <div class="cmd__desc">${escapeHtml(c.desc)}</div>
          <div class="cmd__copy" aria-label="Copy to clipboard">${ICONS.copy}</div>
        </div>`;
    }).join("");
  }

  // -------- Status dot --------
  function setStatus(state, label) {
    const dot = document.getElementById("statusDot");
    const text = document.getElementById("statusText");
    dot.classList.remove("is-stale", "is-error");
    if (state === "stale") dot.classList.add("is-stale");
    if (state === "error") dot.classList.add("is-error");
    text.textContent = label;
  }

  // -------- Toast --------
  let toastTimer = null;
  function toast(msg) {
    const el = document.getElementById("toast");
    el.textContent = msg;
    el.classList.add("is-shown");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => el.classList.remove("is-shown"), 1800);
  }

  // -------- Copy-to-clipboard (event delegation) --------
  document.addEventListener("click", async (e) => {
    const card = e.target.closest(".cmd");
    if (!card) return;
    const cmd = card.dataset.cmd || "";
    try {
      await navigator.clipboard.writeText(cmd);
    } catch {
      // ponytail: fallback for older browsers / non-secure contexts.
      const ta = document.createElement("textarea");
      ta.value = cmd;
      ta.style.position = "fixed";
      ta.style.opacity = "0";
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand("copy"); } catch {}
      document.body.removeChild(ta);
    }
    card.classList.add("copied");
    toast(`Copied: ${cmd}`);
    setTimeout(() => card.classList.remove("copied"), 1400);
  });
  document.addEventListener("keydown", (e) => {
    if ((e.key === "Enter" || e.key === " ") && e.target.classList.contains("cmd")) {
      e.preventDefault();
      e.target.click();
    }
  });

  // -------- Hero meta info (root path, scanned at) --------
  function renderHeroMeta(idx, stats) {
    const el = document.getElementById("heroMeta");
    if (!idx) {
      el.innerHTML = `<span class="hero__meta-row"><strong>Status</strong> No index found</span>`;
      return;
    }
    const scanned = idx.scanned_at || "—";
    const fresh = stats?.index_fresh !== false;
    el.innerHTML = `
      <span class="hero__meta-row"><strong>Root</strong> <code class="mono">${escapeHtml(idx.root || "")}</code></span>
      <span class="hero__meta-row"><strong>Last scan</strong> <code class="mono">${escapeHtml(scanned)}</code></span>
      <span class="hero__meta-row"><strong>Refresh</strong> every 3s</span>
    `;
    el.title = fresh ? "Index live" : "Index stale";
  }

  // -------- Main refresh loop --------
  async function refresh() {
    const [idx, stats, session] = await Promise.all([
      load("/api/index"),
      load("/api/stats"),
      load("/api/session")
    ]);

    if (!idx && !stats) {
      setStatus("error", "offline");
      document.getElementById("assets").innerHTML = `<div class="bento__card bento__card--wide"><div class="bento__label">${ICONS.shield}No data</div><div class="bento__hint" style="margin-top:var(--sp-3)">Dashboard could not reach the server. Is <code class="mono">cursor-framework serve</code> still running?</div></div>`;
      return;
    }

    const fresh = stats && stats.index_fresh !== false;
    setStatus(fresh ? "live" : "stale", fresh ? "live · 3s refresh" : "stale");

    document.getElementById("assets").innerHTML = renderBento(idx, stats);
    document.getElementById("memory").innerHTML = renderMemory(stats);
    document.getElementById("workflow").innerHTML = renderWorkflow(stats);
    document.getElementById("cats").innerHTML = renderCategories(idx);
    renderHeroMeta(idx, stats);

    // Update session context panel
    const sessionData = renderSessionContext(session);
    updateSessionContextUI(sessionData);

    // Update code graph stats in context panel
    const graphData = await load("/api/graph");
    if (graphData) {
      const modEl = document.getElementById("ctx-modules");
      if (modEl) modEl.textContent = fmt(graphData.module_count || 0);
      const depEl = document.getElementById("ctx-deps");
      if (depEl) depEl.textContent = fmt(graphData.dependency_count || 0);
      const langEl = document.getElementById("ctx-langs");
      if (langEl) langEl.textContent = Object.keys(graphData.languages || {}).length;
      const linesEl = document.getElementById("ctx-lines");
      if (linesEl) linesEl.textContent = fmt(graphData.stats?.total_lines || 0);
    }
  }

  // -------- Boot --------
  initTabs();
  document.getElementById("commands").innerHTML = renderCommands();
  refresh();
  setInterval(refresh, REFRESH_MS);
})();
