document.documentElement.dataset.ready = "true";

(function initTopicBeam() {
  const beam = document.querySelector(".topic-beam");
  const sections = [...document.querySelectorAll(".topic-section[data-topic]")];
  if (!beam || sections.length === 0) return;

  const groups = [...beam.querySelectorAll(".topic-group[data-topic]")];
  const topicLinks = [...beam.querySelectorAll("a.topic-link[data-topic]")];
  const subLinks = [...beam.querySelectorAll(".topic-subnav a[href^='#']")];

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

  const sectionObserver = new IntersectionObserver(
    (entries) => {
      const visible = entries
        .filter((entry) => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio);

      if (visible[0]) {
        setActiveTopic(visible[0].target.dataset.topic);
      }
    },
    {
      rootMargin: "-15% 0px -55% 0px",
      threshold: [0.05, 0.15, 0.3, 0.5],
    }
  );

  sections.forEach((section) => sectionObserver.observe(section));

  const subTargets = subLinks
    .map((link) => {
      const id = (link.getAttribute("href") || "").slice(1);
      return id ? document.getElementById(id) : null;
    })
    .filter(Boolean);

  if (subTargets.length > 0) {
    const subObserver = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio);

        if (visible[0]) {
          setActiveSub(visible[0].target.id);
        }
      },
      {
        rootMargin: "-25% 0px -55% 0px",
        threshold: [0.1, 0.25, 0.4],
      }
    );

    subTargets.forEach((target) => subObserver.observe(target));
  }

  setActiveTopic(sections[0].dataset.topic);
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

/** On Sammelband pages: show return link to the KI-Synthese anchor in ?from=. */
(function initBackToSynthesis() {
  if (!document.body.classList.contains("sammelband-page")) return;

  const from = new URLSearchParams(location.search).get("from");
  if (!from) return;

  const anchorId = from.replace(/^#/, "");
  const main = document.querySelector(".article-main");
  const pager = document.querySelector(".article-pager");
  if (!main || !pager) return;

  const back = document.createElement("a");
  back.className = "synthesis-back-link";
  back.href = `index.html#${anchorId}`;
  back.textContent = "← Zurück zur KI-Synthese";

  const wrap = document.createElement("nav");
  wrap.className = "synthesis-back";
  wrap.setAttribute("aria-label", "Zurück zur KI-Synthese");
  wrap.appendChild(back);
  main.insertBefore(wrap, pager);

  pager.querySelectorAll("a.pager-prev, a.pager-next").forEach((link) => {
    const href = link.getAttribute("href");
    if (!href) return;
    const [pathAndQuery, hash = ""] = href.split("#");
    const [path, query = ""] = pathAndQuery.split("?");
    const params = new URLSearchParams(query);
    params.set("from", anchorId);
    link.setAttribute(
      "href",
      `${path}?${params.toString()}${hash ? `#${hash}` : ""}`
    );
  });
})();
