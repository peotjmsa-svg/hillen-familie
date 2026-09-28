// Interactieve stamboom (D3.js) voor Familie Hillen.
(function () {
  "use strict";

  let DATA = null;
  let root = null;
  let svg, g, zoomBehavior;
  let SPOUSES = {};            // personId -> array of spouse personIds
  let PARTNERS_IN_TREE = {};   // personId -> reachable partner personId
  let CHILDREN_IN_TREE = {};   // personId -> reachable child personId
  let TREE_PERSON_IDS = new Set(); // IDs directly reachable in the D3 hierarchy

  const width = () => document.getElementById("tree-svg").clientWidth || 900;
  const height = () => document.getElementById("tree-svg").clientHeight || 600;

  // Vertical layout spacing
  const NODE_H_SPACING = 260; // horizontal space per node
  const NODE_V_SPACING = 120; // vertical space between generations

  let hideExtinctLines = false;

  // A line counts as "extinct" if nobody in its subtree was born in or after 1600.
  // Unknown birth years never count as evidence of extinction (avoids hiding people we simply lack dates for).
  function computeExtinct(d) {
    const kids = d.children || [];
    let maxYear = d.data.birth_year != null ? d.data.birth_year : -Infinity;
    for (const k of kids) {
      computeExtinct(k);
      if (k.maxYear > maxYear) maxYear = k.maxYear;
    }
    d.maxYear = maxYear;
    d.extinct = maxYear !== -Infinity && maxYear < 1600;
  }

  function yearsLabel(p) {
    if (!p) return "";
    const b = p.birth_year != null ? p.birth_year : "?";
    const d = p.death_year != null ? p.death_year : "";
    return d ? `${b}–${d}` : `${b}`;
  }

  function buildHierarchy(rootId) {
    const seen = new Set();
    function node(id) {
      if (seen.has(id)) return null;
      seen.add(id);
      const p = DATA.people[id];
      if (!p) return null;
      const children = (p.children || [])
        .map(node)
        .filter(Boolean)
        .sort((a, b) => (a.data.birth_year || 9999) - (b.data.birth_year || 9999));
      return { data: p, children: children.length ? children : undefined };
    }
    return node(rootId);
  }

  function indexRelationships() {
    SPOUSES = {};
    PARTNERS_IN_TREE = {};
    CHILDREN_IN_TREE = {};

    const fams = DATA.families || {};
    for (const fam of Object.values(fams)) {
      const h = fam.husb;
      const w = fam.wife;
      if (h && w) {
        SPOUSES[h] = SPOUSES[h] || [];
        if (!SPOUSES[h].includes(w)) SPOUSES[h].push(w);

        SPOUSES[w] = SPOUSES[w] || [];
        if (!SPOUSES[w].includes(h)) SPOUSES[w].push(h);
      }
    }

    // For all people not in tree, find their reachable partner or child
    for (const [pid, p] of Object.entries(DATA.people)) {
      if (!TREE_PERSON_IDS.has(pid)) {
        const partners = SPOUSES[pid] || [];
        const treePartner = partners.find(s => TREE_PERSON_IDS.has(s));
        if (treePartner) {
          PARTNERS_IN_TREE[pid] = treePartner;
        }

        const kids = p.children || [];
        const treeKid = kids.find(c => TREE_PERSON_IDS.has(c));
        if (treeKid) {
          CHILDREN_IN_TREE[pid] = treeKid;
        }
      }
    }
  }

  function renderTree() {
    svg = d3.select("#tree-svg");
    svg.selectAll("*").remove();
    g = svg.append("g");

    zoomBehavior = d3.zoom().scaleExtent([0.1, 2.5]).on("zoom", (event) => {
      g.attr("transform", event.transform);
    });
    svg.call(zoomBehavior);

    const hierarchyData = buildHierarchy(DATA.root_id);
    const rootNode = d3.hierarchy(hierarchyData, (d) => d.children);
    rootNode.each((d) => { d.data = d.data.data; });
    computeExtinct(rootNode);

    // Track all people who are in the tree
    TREE_PERSON_IDS = new Set();
    rootNode.each((d) => { TREE_PERSON_IDS.add(d.data.id); });

    indexRelationships();

    const treeLayout = d3.tree().nodeSize([NODE_H_SPACING, NODE_V_SPACING]);
    treeLayout(rootNode);

    // Collapse everything except first two generations
    rootNode.each((d) => {
      if (d.depth >= 2 && d.children) {
        d._children = d.children;
        d.children = null;
      }
    });

    root = rootNode;
    update(root);
    centerOn(root);
  }

  function update(source) {
    const treeLayout = d3.tree().nodeSize([NODE_H_SPACING, NODE_V_SPACING]);
    treeLayout(root);

    const nodes = root.descendants().filter((d) => !(hideExtinctLines && d.extinct));
    const links = root.links().filter((d) => !(hideExtinctLines && d.target.extinct));

    // --- Links ---
    const link = g.selectAll(".tree-link").data(links, (d) => d.target.data.id);
    link.exit().remove();
    link
      .enter()
      .append("path")
      .attr("class", "tree-link")
      .merge(link)
      .transition()
      .duration(350)
      .attr("d", (d) => {
        const sx = d.source.x;
        const sy = d.source.y;
        const tx = d.target.x;
        const ty = d.target.y;
        const midY = (sy + ty) / 2;
        return `M${sx},${sy} V${midY} H${tx} V${ty}`;
      });

    // --- Nodes ---
    const node = g.selectAll(".tree-node").data(nodes, (d) => d.data.id);
    node.exit().remove();

    const nodeEnter = node
      .enter()
      .append("g")
      .attr("class", (d) => "tree-node" + ((d.children || d._children) ? " has-children" : ""))
      .attr("transform", (d) => `translate(${d.x},${d.y})`);

    // Click on circle: toggle children with smooth focus
    nodeEnter.append("circle")
      .attr("r", 7)
      .attr("cy", 0)
      .on("click", (event, d) => {
        event.stopPropagation();
        toggle(d);
      });

    // Click on name: open profile
    nodeEnter.append("text")
      .attr("dy", "-1em")
      .attr("text-anchor", "middle")
      .attr("class", "node-name")
      .text((d) => d.data.name)
      .on("click", (event, d) => {
        event.stopPropagation();
        highlightNode(d.data.id);
        showDetail(d.data);
      });

    // Years
    nodeEnter.append("text")
      .attr("dy", "1.8em")
      .attr("text-anchor", "middle")
      .attr("class", "node-years")
      .text((d) => yearsLabel(d.data));

    // Toggle indicator (+ / -)
    nodeEnter.append("text")
      .attr("dy", "0.35em")
      .attr("text-anchor", "middle")
      .attr("class", "node-toggle")
      .text((d) => d._children ? "+" : "")
      .on("click", (event, d) => {
        event.stopPropagation();
        toggle(d);
      });

    node
      .merge(nodeEnter)
      .attr("class", (d) => "tree-node" + ((d.children || d._children) ? " has-children" : ""))
      .transition()
      .duration(350)
      .attr("transform", (d) => `translate(${d.x},${d.y})`);

    g.selectAll(".tree-node .node-toggle")
      .text((d) => d._children ? "+" : "");
  }

  // Toggle node expansion without losing screen position
  function toggle(d) {
    const isExpanding = !d.children && !!d._children;
    if (d.children) {
      d._children = d.children;
      d.children = null;
    } else if (d._children) {
      d.children = d._children;
      d._children = null;
    }
    update(d);

    // Keep the clicked node cleanly in view!
    // If expanding: place d at 28% from top so newly expanded children are visible below it.
    // If collapsing: place d at 38% from top.
    const currentTransform = d3.zoomTransform(svg.node());
    const currentK = currentTransform.k || 0.8;
    const k = Math.max(0.6, Math.min(1.1, currentK));

    const targetX = width() / 2;
    const targetY = isExpanding ? (height() * 0.28) : (height() * 0.38);

    const t = d3.zoomIdentity
      .translate(targetX, targetY)
      .scale(k)
      .translate(-d.x, -d.y);

    svg.transition()
      .duration(350)
      .ease(d3.easeCubicOut)
      .call(zoomBehavior.transform, t);
  }

  function expandAll(d) {
    if (d._children) {
      d.children = d._children;
      d._children = null;
    }
    if (d.children) d.children.forEach(expandAll);
  }

  // Mathematically accurate centering on ANY node in the tree
  function centerOn(d) {
    if (!d) return;
    const k = 0.85;
    const targetX = width() / 2;
    const targetY = height() * 0.32;

    const t = d3.zoomIdentity
      .translate(targetX, targetY)
      .scale(k)
      .translate(-d.x, -d.y);

    svg.transition()
      .duration(450)
      .ease(d3.easeCubicOut)
      .call(zoomBehavior.transform, t);
  }

  function highlightNode(id) {
    g.selectAll(".tree-node").classed("highlighted", (d) => d.data.id === id);
  }

  function findNode(id, node) {
    node = node || root;
    if (!node) return null;
    if (node.data.id === id) return node;
    const kids = node.children || node._children;
    if (!kids) return null;
    for (const k of kids) {
      const found = findNode(id, k);
      if (found) return found;
    }
    return null;
  }

  function expandPathTo(node) {
    let n = node.parent;
    while (n) {
      if (n._children) {
        n.children = n._children;
        n._children = null;
      }
      n = n.parent;
    }
  }

  // Thijn Hillen's own direct line, from himself up to stamvader Dederick Hillen.
  const MY_LINE_ID = "@P0009@";

  function showMyLine() {
    let node = findNode(MY_LINE_ID);
    if (!node) return;

    switchView("tree");
    expandPathTo(node);
    update(root);
    node = findNode(MY_LINE_ID);

    const lineNodes = [];
    for (let n = node; n; n = n.parent) lineNodes.push(n);
    const lineIds = new Set(lineNodes.map((n) => n.data.id));

    g.selectAll(".tree-node").classed("my-line", (d) => lineIds.has(d.data.id));
    g.selectAll(".tree-link").classed("my-line", (d) => lineIds.has(d.source.data.id) && lineIds.has(d.target.data.id));

    // Zoom to fit the WHOLE line (root to Thijn) in view, not just teleport to Thijn alone.
    const xs = lineNodes.map((n) => n.x);
    const ys = lineNodes.map((n) => n.y);
    const pad = 90;
    const boxW = (Math.max(...xs) - Math.min(...xs)) + pad * 2;
    const boxH = (Math.max(...ys) - Math.min(...ys)) + pad * 2;
    const k = Math.max(0.18, Math.min(1.2, Math.min(width() / boxW, height() / boxH)));
    const cx = (Math.max(...xs) + Math.min(...xs)) / 2;
    const cy = (Math.max(...ys) + Math.min(...ys)) / 2;
    const t = d3.zoomIdentity
      .translate(width() / 2, height() / 2)
      .scale(k)
      .translate(-cx, -cy);

    svg.transition().duration(650).ease(d3.easeCubicOut).call(zoomBehavior.transform, t);
    highlightNode(MY_LINE_ID);
    showDetail(node.data);
  }

  // Show person profile in the side panel
  function showDetail(p, options) {
    options = options || {};
    const panel = document.getElementById("detail-panel");

    // Spouses
    const spouseIds = SPOUSES[p.id] || [];
    const spousesHtml = spouseIds.length
      ? `<div class="detail-field">
          <span class="detail-label">${spouseIds.length > 1 ? "Echtgenoten / Partners" : "Echtgenoot / Partner"}</span>
          <span>${spouseIds.map(sid => {
            const sp = DATA.people[sid];
            return sp ? `<a class="detail-link" data-id="${sid}">${escapeHtml(sp.name)}</a>` : "";
          }).filter(Boolean).join(", ")}</span>
        </div>`
      : "";

    // Children
    const childrenHtml = (p.children && p.children.length)
      ? `<div class="detail-field">
          <span class="detail-label">Kinderen</span>
          <span>${p.children.map(cid => {
            const child = DATA.people[cid];
            return child ? `<a class="detail-link" data-id="${cid}">${escapeHtml(child.name)}</a>` : "";
          }).filter(Boolean).join(", ")}</span>
        </div>`
      : "";

    // Banner if navigated via spouse or child
    let bannerHtml = "";
    if (options.partnerOf) {
      const partner = options.partnerOf;
      bannerHtml = `
        <div class="detail-banner partner">
          💍 <strong>Aangetrouwd familielid</strong><br>
          Gehuwd met <strong><a class="detail-link" data-id="${partner.id}">${escapeHtml(partner.name)}</a></strong>.<br>
          <small>In de stamboom hiernaast aangewezen bij haar/zijn gezin.</small>
        </div>`;
    } else if (options.childOf) {
      const child = options.childOf;
      bannerHtml = `
        <div class="detail-banner partner">
          👨‍👩‍👧 <strong>Familielid</strong><br>
          Ouder van <strong><a class="detail-link" data-id="${child.id}">${escapeHtml(child.name)}</a></strong>.<br>
          <small>In de stamboom hiernaast aangewezen bij het gezin.</small>
        </div>`;
    } else if (options.unlinked) {
      // Check for known relations mentioned in notes
      let suggestHtml = "";
      if (p.id === "@P0009@") {
        suggestHtml = `<br><button class="btn-suggest" data-id="@P0008@">Bekijk tak Felix Hillen (1900–1973)</button>`;
      } else if (["@P0260@", "@P0262@", "@P0264@"].includes(p.id)) {
        suggestHtml = `<br><button class="btn-suggest" data-id="@P0139@">Bekijk tak Henricus Hubertus Hillen</button>`;
      }
      bannerHtml = `
        <div class="detail-banner unlinked">
          📌 <strong>Plaats in stamboom in onderzoek</strong><br>
          Deze persoon is opgenomen in het familie-archief, maar de exacte aansluiting op de hoofdlijn vanaf 1380 wordt nog uitgezocht.${suggestHtml}
        </div>`;
    }

    const occ = p.occupation ? `<div class="detail-field"><span class="detail-label">Beroep</span><span>${escapeHtml(p.occupation)}</span></div>` : "";
    const place = p.place ? `<div class="detail-field"><span class="detail-label">Plaats</span><span>${escapeHtml(p.place)}</span></div>` : "";
    const note = p.note ? `<div class="detail-note">${escapeHtml(p.note)}</div>` : "";
    const sources = (p.sources && p.sources.length)
      ? `<div class="detail-sources"><span class="detail-label">Bronnen</span><ul>${p.sources.map(s => `<li>${escapeHtml(s)}</li>`).join("")}</ul></div>`
      : "";

    const sexIcon = p.sex === "M" ? "♂" : p.sex === "F" ? "♀" : "";
    const sexClass = p.sex === "M" ? "male" : p.sex === "F" ? "female" : "";

    panel.innerHTML = `
      <button class="detail-close" id="detail-close-btn" title="Sluiten">&times;</button>
      <div class="detail-header ${sexClass}">
        <span class="detail-sex">${sexIcon}</span>
        <h3>${escapeHtml(p.name)}</h3>
        <div class="detail-years">${yearsLabel(p)}</div>
      </div>
      <div class="detail-body">
        ${bannerHtml}
        ${occ}
        ${place}
        ${spousesHtml}
        ${childrenHtml}
        ${note}
        ${sources}
      </div>
    `;
    panel.classList.add("active");

    // Close button
    document.getElementById("detail-close-btn").addEventListener("click", () => {
      panel.classList.remove("active");
    });

    // Clickable links to other people
    panel.querySelectorAll(".detail-link, .btn-suggest").forEach(link => {
      link.addEventListener("click", () => {
        const id = link.getAttribute("data-id");
        if (id) selectPerson(id);
      });
    });
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  // Full-profile search: matches name, occupation, place, notes, sources, years.
  function searchPerson(p, q) {
    if (p.name && p.name.toLowerCase().includes(q)) return null;
    if (p.occupation && p.occupation.toLowerCase().includes(q)) return `Beroep: ${p.occupation}`;
    if (p.place && p.place.toLowerCase().includes(q)) return `Plaats: ${p.place}`;
    if (p.note && p.note.toLowerCase().includes(q)) {
      const idx = p.note.toLowerCase().indexOf(q);
      const start = Math.max(0, idx - 30);
      const end = Math.min(p.note.length, idx + q.length + 30);
      const snippet = (start > 0 ? "…" : "") + p.note.substring(start, end) + (end < p.note.length ? "…" : "");
      return `Notitie: ${snippet}`;
    }
    if (p.sources && p.sources.some(s => s.toLowerCase().includes(q))) {
      const src = p.sources.find(s => s.toLowerCase().includes(q));
      return `Bron: ${src.length > 60 ? src.substring(0, 57) + "…" : src}`;
    }
    const yearStr = q.replace(/\D/g, "");
    if (yearStr.length >= 3) {
      if (p.birth_year != null && String(p.birth_year).includes(yearStr)) return `Geboortejaar: ${p.birth_year}`;
      if (p.death_year != null && String(p.death_year).includes(yearStr)) return `Overlijdensjaar: ${p.death_year}`;
    }
    return undefined;
  }

  function setupSearch() {
    const input = document.getElementById("person-search");
    const results = document.getElementById("search-results");

    input.addEventListener("input", () => {
      const q = input.value.trim().toLowerCase();
      if (q.length < 2) {
        results.style.display = "none";
        results.innerHTML = "";
        return;
      }

      const matches = [];
      for (const p of Object.values(DATA.people)) {
        const reason = searchPerson(p, q);
        if (reason !== undefined) {
          matches.push({ person: p, reason });
        }
        if (matches.length >= 30) break;
      }

      matches.sort((a, b) => {
        const aName = a.reason === null ? 0 : 1;
        const bName = b.reason === null ? 0 : 1;
        if (aName !== bName) return aName - bName;
        return a.person.name.localeCompare(b.person.name, "nl");
      });

      if (!matches.length) {
        results.innerHTML = '<div style="color:#888;">Geen resultaten</div>';
        results.style.display = "block";
        return;
      }

      results.innerHTML = matches
        .map(({ person: p, reason }) => {
          let spouseHint = "";
          // If spouse is in tree, indicate that
          if (!TREE_PERSON_IDS.has(p.id) && PARTNERS_IN_TREE[p.id]) {
            const partner = DATA.people[PARTNERS_IN_TREE[p.id]];
            if (partner) spouseHint = ` <span class="search-spouse">(gehuwd met ${escapeHtml(partner.name)})</span>`;
          }
          const hint = reason ? `<span class="search-hint">${escapeHtml(reason)}</span>` : "";
          return `<div data-id="${p.id}">${escapeHtml(p.name)}${spouseHint} <span class="search-years">(${yearsLabel(p)})</span>${hint}</div>`;
        })
        .join("");
      results.style.display = "block";
    });

    results.addEventListener("click", (e) => {
      const el = e.target.closest("[data-id]");
      if (!el) return;
      const id = el.getAttribute("data-id");
      results.style.display = "none";
      input.value = "";
      selectPerson(id);
    });

    document.addEventListener("click", (e) => {
      if (!results.contains(e.target) && e.target !== input) {
        results.style.display = "none";
      }
    });
  }

  // Navigate to any person, whether directly in the tree, married to someone in tree, or unlinked
  function selectPerson(id) {
    const person = DATA.people[id];
    if (!person) return;

    let node = findNode(id);
    if (node) {
      // 1. Direct descendant in tree
      switchView("tree");
      expandPathTo(node);
      update(root);
      node = findNode(id);
      centerOn(node);
      highlightNode(id);
      showDetail(node.data);
      return;
    }

    // 2. Person is married to someone in the tree
    const partnerId = PARTNERS_IN_TREE[id];
    if (partnerId) {
      const partner = DATA.people[partnerId];
      let partnerNode = findNode(partnerId);
      if (partnerNode) {
        switchView("tree");
        expandPathTo(partnerNode);
        update(root);
        partnerNode = findNode(partnerId);
        centerOn(partnerNode);
        highlightNode(partnerId);
        showDetail(person, { partnerOf: partner });
        return;
      }
    }

    // 3. Person has a child in the tree
    const childId = CHILDREN_IN_TREE[id];
    if (childId) {
      const child = DATA.people[childId];
      let childNode = findNode(childId);
      if (childNode) {
        switchView("tree");
        expandPathTo(childNode);
        update(root);
        childNode = findNode(childId);
        centerOn(childNode);
        highlightNode(childId);
        showDetail(person, { childOf: child });
        return;
      }
    }

    // 4. Truly unlinked (e.g. Thijn Hillen, Dederik Hillen, Nicolaas Theodorus Hillen)
    showDetail(person, { unlinked: true });
  }

  function buildAlphaList() {
    const container = document.getElementById("alpha-list");
    const people = Object.values(DATA.people).sort((a, b) => a.name.localeCompare(b.name, "nl"));
    const groups = {};
    people.forEach((p) => {
      const letter = (p.name.trim()[0] || "?").toUpperCase();
      groups[letter] = groups[letter] || [];
      groups[letter].push(p);
    });
    const letters = Object.keys(groups).sort();
    container.innerHTML = letters
      .map(
        (letter) => `
      <div class="letter-group">
        <h4>${letter}</h4>
        <ul>
          ${groups[letter]
            .map(
              (p) =>
                `<li data-id="${p.id}">${escapeHtml(p.name)} <span class="yrs">(${yearsLabel(p)})</span></li>`
            )
            .join("")}
        </ul>
      </div>`
      )
      .join("");

    container.addEventListener("click", (e) => {
      const id = e.target.closest("[data-id]")?.getAttribute("data-id");
      if (id) selectPerson(id);
    });
  }

  function switchView(which) {
    const treeBtn = document.getElementById("view-tree-btn");
    const listBtn = document.getElementById("view-list-btn");
    const treeView = document.getElementById("tree-view");
    const listView = document.getElementById("list-view");
    if (which === "tree") {
      treeBtn.classList.add("active");
      listBtn.classList.remove("active");
      treeView.classList.remove("hidden");
      listView.classList.remove("active");
    } else {
      listBtn.classList.add("active");
      treeBtn.classList.remove("active");
      treeView.classList.add("hidden");
      listView.classList.add("active");
    }
  }

  function init() {
    // Mobile hamburger menu toggle
    const navToggle = document.getElementById("nav-toggle");
    const mainNav = document.getElementById("main-nav");
    if (navToggle && mainNav) {
      navToggle.addEventListener("click", () => {
        navToggle.classList.toggle("open");
        mainNav.classList.toggle("open");
      });
    }

    fetch("data/stamboom.json")
      .then((r) => r.json())
      .then((data) => {
        DATA = data;
        renderTree();
        buildAlphaList();
        setupSearch();

        document.getElementById("view-tree-btn").addEventListener("click", () => switchView("tree"));
        document.getElementById("view-list-btn").addEventListener("click", () => switchView("list"));
        document.getElementById("reset-view-btn").addEventListener("click", () => centerOn(root));
        document.getElementById("my-line-btn").addEventListener("click", showMyLine);
        document.getElementById("toggle-extinct-btn").addEventListener("click", () => {
          hideExtinctLines = !hideExtinctLines;
          const btn = document.getElementById("toggle-extinct-btn");
          btn.textContent = hideExtinctLines ? "Uitgestorven lijnen tonen" : "Uitgestorven lijnen verbergen";
          btn.classList.toggle("active", hideExtinctLines);
          update(root);
        });
        document.getElementById("expand-all-btn").addEventListener("click", () => {
          expandAll(root);
          update(root);
        });
        window.addEventListener("resize", () => centerOn(root));

        // Close detail panel on backdrop click (mobile-friendly)
        document.addEventListener("click", (e) => {
          const panel = document.getElementById("detail-panel");
          if (panel.classList.contains("active") && !panel.contains(e.target) && !e.target.closest(".tree-node") && !e.target.closest("#alpha-list") && !e.target.closest("#search-results") && !e.target.closest("#my-line-btn")) {
            panel.classList.remove("active");
          }
        });
      })
      .catch((err) => {
        document.getElementById("tree-wrap").innerHTML =
          '<p style="padding:2rem;color:#7a1f22;">Kon de stamboomgegevens niet laden.</p>';
        console.error(err);
      });
  }

  init();
})();
