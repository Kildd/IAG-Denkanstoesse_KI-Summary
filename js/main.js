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
