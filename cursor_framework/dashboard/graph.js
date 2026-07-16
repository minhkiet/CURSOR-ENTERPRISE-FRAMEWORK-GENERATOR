/* Skill / agent dependency graph — D3 force-directed, CDN-hosted D3.
   Loaded only on the #graph tab (lazy: graph.js is not bundled, only
   referenced on the tab that needs it). */
(function () {
  "use strict";

  // Load D3 from CDN once, then run init().
  // Check if d3 is already loaded (tab-switch back from graph to dashboard).
  if (typeof d3 !== "undefined") {
    init();
    return;
  }
  var script = document.createElement("script");
  script.src = "https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js";
  script.onload = init;
  script.onerror = function () {
    var el = document.getElementById("graphSvg");
    if (el) {
      el.outerHTML =
        '<div style="display:grid;place-items:center;height:100%;color:var(--fg-2);font-family:JetBrains Mono,monospace;font-size:14px;text-align:center;padding:2rem;">' +
        '<div><svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>' +
        "<p>Could not load D3 from CDN.<br>Check your network connection.</p></div>";
    }
  };
  document.head.appendChild(script);

  // ---- Node radius map ----
  var KIND_RADIUS = {
    skill: 9,
    agent: 9,
    knowledge: 7,
    rule: 7,
  };

  // ---- Color map ----
  var KIND_COLOR = {
    skill: "#56d2ff",     // cyan
    agent: "#f0a35e",     // warm orange
    knowledge: "#5fd39a", // green
    rule: "#5b6573",      // gray
  };

  // ---- Tooltip ----
  var tooltip, ttName, ttKind, ttTags, ttPath;

  function showTooltip(event, d) {
    ttName.textContent = d.id;
    ttKind.textContent = d.kind;
    ttPath.textContent = d.path || "";
    ttTags.innerHTML = "";
    (d.tags || []).forEach(function (tag) {
      var span = document.createElement("span");
      span.className = "graph-tooltip__tag";
      span.textContent = tag;
      ttTags.appendChild(span);
    });
    tooltip.classList.add("is-visible");

    var wrap = document.getElementById("graphWrap");
    var wrapRect = wrap.getBoundingClientRect();
    var tx = event.clientX - wrapRect.left + 14;
    var ty = event.clientY - wrapRect.top - 8;

    // Keep tooltip inside the graph wrap.
    var ttRect = tooltip.getBoundingClientRect();
    if (tx + ttRect.width > wrapRect.width - 16)
      tx = event.clientX - wrapRect.left - ttRect.width - 14;
    if (ty + ttRect.height > wrapRect.height - 16)
      ty = event.clientY - wrapRect.top - ttRect.height - 8;

    tooltip.style.left = tx + "px";
    tooltip.style.top = ty + "px";
  }

  function hideTooltip() {
    tooltip.classList.remove("is-visible");
  }

  // ---- Main init ----
  function init() {
    tooltip = document.getElementById("graphTooltip");
    ttName = document.getElementById("tt-name");
    ttKind = document.getElementById("tt-kind");
    ttTags = document.getElementById("tt-tags");
    ttPath = document.getElementById("tt-path");

    var svgEl = document.getElementById("graphSvg");
    if (!svgEl) return;

    var container = svgEl.parentElement;
    var width = container.clientWidth || window.innerWidth;
    var height = container.clientHeight || window.innerHeight - 72; // subtract nav height

    var svg = d3
      .select(svgEl)
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height]);

    // Defs: arrowhead markers for directed edges.
    var defs = svg.append("defs");
    defs
      .append("marker")
      .attr("id", "arrow-dep")
      .attr("viewBox", "0 -4 8 8")
      .attr("refX", 18)
      .attr("refY", 0)
      .attr("markerWidth", 5)
      .attr("markerHeight", 5)
      .attr("orient", "auto")
      .append("path")
      .attr("d", "M0,-4L8,0L0,4")
      .attr("fill", "rgba(86,210,255,0.4)");

    // Arrow for co_occurrence edges.
    defs
      .append("marker")
      .attr("id", "arrow-co")
      .attr("viewBox", "0 -4 8 8")
      .attr("refX", 18)
      .attr("refY", 0)
      .attr("markerWidth", 4)
      .attr("markerHeight", 4)
      .attr("orient", "auto")
      .append("path")
      .attr("d", "M0,-3L6,0L0,3")
      .attr("fill", "rgba(91,101,115,0.3)");

    var g = svg.append("g");

    // Zoom/pan.
    svg.call(
      d3
        .zoom()
        .scaleExtent([0.2, 4])
        .on("zoom", function (event) {
          g.attr("transform", event.transform);
        })
    );

    // Fetch graph data.
    var TOKEN = new URLSearchParams(location.search).get("token") || "";
    var sep = TOKEN ? "?token=" + encodeURIComponent(TOKEN) : "";
    fetch("/api/graph" + sep)
      .then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.json();
      })
      .then(function (graph) {
        renderGraph(graph, g, svg, width, height);
      })
      .catch(function (err) {
        console.error("[graph] failed to load", err);
        svg
          .append("text")
          .attr("x", width / 2)
          .attr("y", height / 2)
          .attr("text-anchor", "middle")
          .attr("fill", "#5b6573")
          .attr("font-family", "JetBrains Mono, monospace")
          .attr("font-size", 14)
          .text("Could not load graph data. Run cursor-framework warm first.");
      });

    // Resize handler.
    window.addEventListener("resize", function () {
      var w2 = container.clientWidth || window.innerWidth;
      var h2 = container.clientHeight || window.innerHeight - 72;
      svg.attr("width", w2).attr("height", h2).attr("viewBox", [0, 0, w2, h2]);
    });
  }

  function renderGraph(graph, g, svg, width, height) {
    // Stats bar.
    document.getElementById("graphNodeCount").textContent = graph.node_count || 0;
    document.getElementById("graphEdgeCount").textContent = graph.edge_count || 0;
    var genAt = graph.generated_at
      ? new Date(graph.generated_at).toLocaleTimeString()
      : "—";
    document.getElementById("graphGeneratedAt").textContent = genAt;

    // Deep-copy so D3 can mutate safely.
    var nodes = (graph.nodes || []).map(function (n) {
      return Object.assign({}, n);
    });
    var edges = (graph.edges || []).map(function (e) {
      return Object.assign({}, e);
    });

    var nodeById = {};
    nodes.forEach(function (n) {
      nodeById[n.id] = n;
    });

    // Simulation.
    var simulation = d3
      .forceSimulation(nodes)
      .force(
        "link",
        d3
          .forceLink(edges)
          .id(function (d) {
            return d.id;
          })
          .distance(130)
          .strength(0.5)
      )
      .force("charge", d3.forceManyBody().strength(-320).distanceMax(400))
      .force("center", d3.forceCenter(width / 2, height / 2).strength(0.05))
      .force("collision", d3.forceCollide().radius(function (d) {
        return (KIND_RADIUS[d.kind] || 8) + 18;
      }));

    // Edges.
    var link = g
      .append("g")
      .attr("class", "links")
      .selectAll("line")
      .data(edges)
      .join("line")
      .attr("class", function (d) {
        return "g-link " + (d.kind === "dependency" ? "dep" : d.kind);
      })
      .attr("marker-end", function (d) {
        return d.kind === "dependency" ? "url(#arrow-dep)" : "url(#arrow-co)";
      });

    // Nodes.
    var node = g
      .append("g")
      .attr("class", "nodes")
      .selectAll("g")
      .data(nodes)
      .join("g")
      .attr("class", function (d) {
        return "g-node " + (d.kind || "skill");
      })
      .call(
        d3
          .drag()
          .on("start", function (event, d) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
          })
          .on("drag", function (event, d) {
            d.fx = event.x;
            d.fy = event.y;
          })
          .on("end", function (event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
          })
      );

    // Circles.
    node
      .append("circle")
      .attr("r", function (d) {
        return KIND_RADIUS[d.kind] || 8;
      })
      .attr("fill", function (d) {
        return KIND_COLOR[d.kind] || "#5b6573";
      })
      .attr("fill-opacity", 0.85)
      .attr("stroke", function (d) {
        return KIND_COLOR[d.kind] || "#5b6573";
      })
      .attr("stroke-width", 1.5)
      .attr("stroke-opacity", 0.4);

    // Hover glow ring (hidden by default, shown on hover).
    node
      .append("circle")
      .attr("class", "glow-ring")
      .attr("r", function (d) {
        return (KIND_RADIUS[d.kind] || 8) + 5;
      })
      .attr("fill", "none")
      .attr("stroke", function (d) {
        return KIND_COLOR[d.kind] || "#5b6573";
      })
      .attr("stroke-width", 1)
      .attr("stroke-opacity", 0)
      .attr("pointer-events", "none");

    // ID label (always visible).
    node
      .append("text")
      .attr("class", "node-label")
      .attr("dx", 12)
      .attr("dy", "0.35em")
      .attr("fill", "#9aa3b0")
      .text(function (d) {
        return d.id;
      });

    // Hover name label (shown only on hover).
    node
      .append("text")
      .attr("class", "hover-label")
      .attr("dx", 14)
      .attr("dy", "0.35em")
      .attr("fill", "#e8ecf2")
      .text(function (d) {
        return d.id + " · v" + (d.version || "?");
      });

    // Title tooltip (native browser).
    node.append("title").text(function (d) {
      var tags = (d.tags || []).join(", ");
      return d.id + " (" + d.kind + ", v" + (d.version || "?") + ")" + (tags ? "\nTags: " + tags : "");
    });

    // Hover events.
    node
      .on("mouseenter", function (event, d) {
        d3.select(this).select(".glow-ring").attr("stroke-opacity", 0.6);
        d3.select(this).select(".node-label").attr("opacity", 0);
        showTooltip(event, d);
      })
      .on("mousemove", function (event) {
        showTooltip(event, d3.select(this).datum());
      })
      .on("mouseleave", function () {
        d3.select(this).select(".glow-ring").attr("stroke-opacity", 0);
        d3.select(this).select(".node-label").attr("opacity", 1);
        hideTooltip();
      });

    // Simulation tick.
    simulation.on("tick", function () {
      link
        .attr("x1", function (d) {
          return d.source.x;
        })
        .attr("y1", function (d) {
          return d.source.y;
        })
        .attr("x2", function (d) {
          return d.target.x;
        })
        .attr("y2", function (d) {
          return d.target.y;
        });

      node.attr("transform", function (d) {
        return "translate(" + d.x + "," + d.y + ")";
      });
    });

    // Simpler version for reduced motion.
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      simulation.stop();
      // Lay out nodes in a circle manually.
      var cx = width / 2;
      var cy = height / 2;
      var r = Math.min(width, height) * 0.35;
      nodes.forEach(function (n, i) {
        var angle = (i / nodes.length) * 2 * Math.PI;
        n.fx = cx + r * Math.cos(angle);
        n.fy = cy + r * Math.sin(angle);
        n.x = n.fx;
        n.y = n.fy;
      });
      // Re-run tick once.
      simulation.alpha(0).restart();
    }
  }

  // ---- Tab switcher (wired from app.js tab init) ----
  window._initGraph = init;
})();
