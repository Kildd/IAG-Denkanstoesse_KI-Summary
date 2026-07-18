document.documentElement.dataset.ready = "true";

(function initTopicBeam() {
  const beam = document.querySelector(".topic-beam");
  const sections = [...document.querySelectorAll(".topic-section[data-topic]")];
  if (!beam || sections.length === 0) return;

  const groups = [...beam.querySelectorAll(".topic-group[data-topic]")];
  const topicLinks = [...beam.querySelectorAll("a.topic-link[data-topic]")];
  const subLinks = [...beam.querySelectorAll(".topic-subnav a[href^='#']")];
  const markerOffset = 140;

  function setActiveTopic(topicId) {
    groups.forEach((group) => {
      group.classList.toggle("is-open", group.dataset.topic === topicId);
    });
    topicLinks.forEach((link) => {
      link.classList.toggle("is-active", link.dataset.topic === topicId);
    });
  }

  function setActiveSub(id) {
    subLinks.forEach((link) => {
      const href = link.getAttribute("href") || "";
      link.classList.toggle("is-active", href === `#${id}`);
    });
  }

  function topicIdFromHash() {
    const hash = (location.hash || "").slice(1);
    if (!hash) return null;
    if (hash.startsWith("abschnitt-")) return hash;
    const el = document.getElementById(hash);
    const section = el && el.closest(".topic-section[data-topic]");
    return section ? section.dataset.topic : null;
  }

  function updateActiveFromScroll() {
    let current = sections[0];
    for (const section of sections) {
      if (section.getBoundingClientRect().top <= markerOffset) {
        current = section;
      }
    }
    setActiveTopic(current.dataset.topic);

    let activeSub = null;
    for (const link of subLinks) {
      const id = (link.getAttribute("href") || "").slice(1);
      const target = id ? document.getElementById(id) : null;
      if (!target) continue;
      if (target.getBoundingClientRect().top <= markerOffset + 40) {
        activeSub = id;
      }
    }
    if (activeSub) setActiveSub(activeSub);
  }

  topicLinks.forEach((link) => {
    link.addEventListener("click", () => {
      const topicId = link.dataset.topic;
      if (topicId) setActiveTopic(topicId);
    });
  });

  subLinks.forEach((link) => {
    link.addEventListener("click", () => {
      const id = (link.getAttribute("href") || "").slice(1);
      const target = id ? document.getElementById(id) : null;
      const section = target && target.closest(".topic-section[data-topic]");
      if (section) setActiveTopic(section.dataset.topic);
      if (id) setActiveSub(id);
    });
  });

  window.addEventListener("scroll", updateActiveFromScroll, { passive: true });
  window.addEventListener("hashchange", () => {
    const fromHash = topicIdFromHash();
    if (fromHash) setActiveTopic(fromHash);
    requestAnimationFrame(updateActiveFromScroll);
  });

  const fromHash = topicIdFromHash();
  setActiveTopic(fromHash || sections[0].dataset.topic);
  updateActiveFromScroll();
})();

/** On KI-Synthese: append ?from=<nearest-id> to Sammelband article links. */
(function enhanceSynthesisArticleLinks() {
  if (!document.querySelector(".topic-section[data-topic]")) return;

  const isArticleHref = (href) =>
    /^(artikel-\d|kapitel-\d|einleitung\.html)/.test(href.split("?")[0]);

  document.querySelectorAll("main a[href]").forEach((anchor) => {
    const href = anchor.getAttribute("href");
    if (!href || href.startsWith("#") || href.startsWith("http")) return;
    if (!isArticleHref(href)) return;

    const host = anchor.closest("article[id], section[id], [id]");
    if (!host || !host.id) return;

    const [pathAndQuery, hash = ""] = href.split("#");
    const [path, query = ""] = pathAndQuery.split("?");
    const params = new URLSearchParams(query);
    if (params.has("from")) return;
    params.set("from", host.id);
    const next = `${path}?${params.toString()}${hash ? `#${hash}` : ""}`;
    anchor.setAttribute("href", next);
  });
})();

/**
 * On Sammelband pages: show a return link from ?from=.
 * - id only (e.g. akteur-6-6) → KI-Synthese
 * - kapitel-*.html → Abschnittsübersicht
 */
(function initBackFromMarker() {
  if (!document.body.classList.contains("sammelband-page")) return;

  const from = new URLSearchParams(location.search).get("from");
  if (!from) return;

  const main = document.querySelector(".article-main");
  const pager = document.querySelector(".article-pager");
  if (!main || !pager) return;

  let href;
  let label;
  if (/\.html(?:#|$)/.test(from) || from.endsWith(".html")) {
    href = from;
    if (from.startsWith("kapitel-")) {
      label = "← Zurück zur Übersicht";
    } else if (from.startsWith("einleitung")) {
      label = "← Zurück zur Einleitung";
    } else {
      label = "← Zurück";
    }
  } else {
    const anchorId = from.replace(/^#/, "");
    href = `index.html#${anchorId}`;
    label = "← Zurück zur KI-Synthese";
  }

  const back = document.createElement("a");
  back.className = "synthesis-back-link";
  back.href = href;
  back.textContent = label;

  const wrap = document.createElement("nav");
  wrap.className = "synthesis-back";
  wrap.setAttribute("aria-label", label.replace(/^←\s*/, ""));
  wrap.appendChild(back);
  main.insertBefore(wrap, pager);

  pager.querySelectorAll("a.pager-prev, a.pager-next").forEach((link) => {
    const linkHref = link.getAttribute("href");
    if (!linkHref) return;
    const [pathAndQuery, hash = ""] = linkHref.split("#");
    const [path, query = ""] = pathAndQuery.split("?");
    const params = new URLSearchParams(query);
    params.set("from", from);
    link.setAttribute(
      "href",
      `${path}?${params.toString()}${hash ? `#${hash}` : ""}`
    );
  });
})();
