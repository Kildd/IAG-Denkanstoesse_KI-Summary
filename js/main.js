document.documentElement.dataset.ready = "true";

(function initTopicBeam() {
  const beam = document.querySelector(".topic-beam");
  const sections = [...document.querySelectorAll(".topic-section[data-topic]")];
  if (!beam || sections.length === 0) return;

  const links = [...beam.querySelectorAll("a[data-topic]")];

  function setActive(topicId) {
    links.forEach((link) => {
      link.classList.toggle("is-active", link.dataset.topic === topicId);
    });
  }

  const observer = new IntersectionObserver(
    (entries) => {
      const visible = entries
        .filter((entry) => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio);

      if (visible[0]) {
        setActive(visible[0].target.dataset.topic);
      }
    },
    {
      rootMargin: "-20% 0px -55% 0px",
      threshold: [0.1, 0.25, 0.5],
    }
  );

  sections.forEach((section) => observer.observe(section));
  setActive(sections[0].dataset.topic);
})();
