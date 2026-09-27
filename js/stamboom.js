// Interactieve stamboom (D3.js) voor Familie Hillen.
(function () {
  "use strict";

  let DATA = null;
  let root = null;
  let svg, g, zoomBehavior;
  const width = () => document.getElementById("tree-svg").clientWidth || 900;
  const height = () => document.getElementById("tree-svg").clientHeight || 600;

  function yearsLabel(p) {
    const b = p.birth_year != null ? p.birth_year : "?";
    const d = p.death_year != null ? p.death_year : "";
    return d ? `${b}–${d}` : `${b}`;
  }

  function buildHierarchy(rootId) {
    const seen = new Set();
    function node(id) {
      if (seen.has(id)) return null; // guard against accidental cycles
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

  function renderTree() {
    const container = document.getElementById("tree-wrap");
    svg = d3.select("#tree-svg");
    svg.selectAll("*").remove();
    g = svg.append("g");

    zoomBehavior = d3.zoom().scaleExtent([0.2, 2.5]).on("zoom", (event) => {
      g.attr("transform", event.transform);
    });
    svg.call(zoomBehavior);

    const hierarchyData = buildHierarchy(DATA.root_id);
    const rootNode = d3.hierarchy(hierarchyData, (d) => d.children);
    rootNode.each((d) => { d.data = d.data.data; }); // unwrap wrapper -> raw person object

    const treeLayout = d3.tree().nodeSize([26, 190]);
    treeLayout(rootNode);

    // Collapse everything except the first two generations for a manageable initial view.
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
    // Recompute layout on the (possibly collapsed) tree.
    const treeLayout = d3.tree().nodeSize([26, 190]);
    treeLayout(root);

    const nodes = root.descendants();
    const links = root.links();

    const link = g.selectAll(".tree-link").data(links, (d) => d.target.data.id);
    link.exit().remove();
    link
      .enter()
      .append("path")
      .attr("class", "tree-link")
      .merge(link)
      .attr(
        "d",
        d3
          .linkHorizontal()
          .x((d) => d.y)
          .y((d) => d.x)
      );

    const node = g.selectAll(".tree-node").data(nodes, (d) => d.data.id);
    node.exit().remove();

    const nodeEnter = node
      .enter()
      .append("g")
      .attr("class", (d) => "tree-node" + ((d.children || d._children) ? " has-children" : ""))
      .attr("transform", (d) => `translate(${d.y},${d.x})`)
      .on("click", (event, d) => {
        toggle(d);
        showDetail(d.data);
      });

    nodeEnter.append("circle").attr("r", 6);
    nodeEnter
      .append("text")
      .attr("dy", "0.32em")
      .attr("x", (d) => (d.children || d._children ? -10 : 10))
      .attr("text-anchor", (d) => (d.children || d._children ? "end" : "start"))
      .text((d) => `${d.data.name} (${yearsLabel(d.data)})`);

    node
      .merge(nodeEnter)
      .attr("class", (d) => "tree-node" + ((d.children || d._children) ? " has-children" : ""))
      .transition()
      .duration(300)
      .attr("transform", (d) => `translate(${d.y},${d.x})`);
  }

  function toggle(d) {
    if (d.children) {
      d._children = d.children;
      d.children = null;
    } else if (d._children) {
      d.children = d._children;
      d._children = null;
    }
    update(d);
  }

  function expandAll(d) {
    if (d._children) {
      d.children = d._children;
      d._children = null;
    }
    if (d.children) d.children.forEach(expandAll);
  }

  function centerOn(d) {
    const t = d3.zoomIdentity.translate(width() / 2 - (d.y || 0), height() / 2 - (d.x || 0)).scale(0.9);
    svg.transition().duration(400).call(zoomBehavior.transform, t);
  }

  function findNode(id, node) {
    node = node || root;
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

  function showDetail(p) {
    const panel = document.getElementById("detail-panel");
    const occ = p.occupation ? `<div class="occ">${escapeHtml(p.occupation)}</div>` : "";
    const place = p.place ? `<div><strong>Plaats:</strong> ${escapeHtml(p.place)}</div>` : "";
    const note = p.note ? `<p>${escapeHtml(p.note)}</p>` : "";
    panel.innerHTML = `
      <h3>${escapeHtml(p.name)}</h3>
      <div class="years">${yearsLabel(p)}</div>
      ${occ}
      ${place}
      ${note}
    `;
    panel.classList.add("active");
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
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
      const matches = Object.values(DATA.people)
        .filter((p) => p.name.toLowerCase().includes(q))
        .slice(0, 20);
      if (!matches.length) {
        results.innerHTML = '<div style="color:#888;">Geen resultaten</div>';
        results.style.display = "block";
        return;
      }
      results.innerHTML = matches
        .map((p) => `<div data-id="${p.id}">${escapeHtml(p.name)} (${yearsLabel(p)})</div>`)
        .join("");
      results.style.display = "block";
    });

    results.addEventListener("click", (e) => {
      const id = e.target.getAttribute("data-id");
      if (!id) return;
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

  function selectPerson(id) {
    let node = findNode(id);
    if (!node) {
      // Not part of the blood-line tree (e.g. a spouse who married into the
      // family and has no recorded parents) -- still show their details.
      const person = DATA.people[id];
      if (person) showDetail(person);
      return;
    }
    switchView("tree");
    expandPathTo(node);
    update(root);
    node = findNode(id);
    centerOn(node);
    showDetail(node.data);
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
      const id = e.target.getAttribute("data-id");
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
        document.getElementById("expand-all-btn").addEventListener("click", () => {
          expandAll(root);
          update(root);
        });
        window.addEventListener("resize", () => centerOn(root));
      })
      .catch((err) => {
        document.getElementById("tree-wrap").innerHTML =
          '<p style="padding:2rem;color:#7a1f22;">Kon de stamboomgegevens niet laden.</p>';
        console.error(err);
      });
  }

  init();
})();
