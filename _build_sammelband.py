# -*- coding: utf-8 -*-
"""Generate Sammelbandartikel pages with shared TOC and prev/next navigation."""
from pathlib import Path
import html
import json
import re
import shutil

root = Path(__file__).resolve().parent

SECTIONS = [
    ("einleitung", "Einleitung", None),
    ("kapitel-1", "1. Neue Technologien und Innovationen", 1),
    ("kapitel-2", "2. Regulierung und Governance", 2),
    ("kapitel-3", "3. Ökonomie", 3),
    ("kapitel-4", "4. Kultur, Öffentlichkeit und Medien", 4),
    ("kapitel-5", "5. Denkmuster, Routinen und Verhalten", 5),
]

# (section_num or 'einleitung', filename, authors, title, toc_label, has_full_body)
ARTICLES = [
    (
        "einleitung",
        "einleitung.html",
        "Yuca Meubrink, Ulrike Kuhlmann und Mike Schlaich",
        "Einleitung: Hindernisse nachhaltigen Bauens als Forschungs- und Handlungsfeld",
        "Einleitung: Hindernisse nachhaltigen Bauens als Forschungs- und Handlungsfeld",
        False,
    ),
    # 1
    (
        1,
        "artikel-1-1.html",
        "Philippe Block",
        "Transferring sustainability innovations in construction from research to industry: Reflections on hindrances",
        "Transferring sustainability innovations in construction from research to industry: Reflections on hindrances",
        False,
    ),
    (
        1,
        "artikel-1-2.html",
        "Yuca Meubrink, Mike Schlaich und Ulrike Kuhlmann",
        "Wo drückt der Schuh? Eine Umfrage unter Planungsbüros zu den Hindernissen nachhaltigen Bauens",
        "Wo drückt der Schuh? Eine Umfrage unter Planungsbüros zu den Hindernissen nachhaltigen Bauens",
        False,
    ),
    (
        1,
        "artikel-1-3.html",
        "Andreas Hofer",
        "Wie Internationale Bauausstellungen die Innovation im Bauwesen befördern und Hindernisse aus dem Weg räumen können",
        "Wie Internationale Bauausstellungen die Innovation im Bauwesen befördern und Hindernisse aus dem Weg räumen können",
        False,
    ),
    (
        1,
        "artikel-1-4.html",
        "Achim Menges",
        "Integratives computerbasiertes Planen und Bauen",
        "Integratives computerbasiertes Planen und Bauen",
        False,
    ),
    (
        1,
        "artikel-1-5.html",
        "Cordula Kropp",
        "Anders Wohnen. Zwischen Experimenten für nachhaltige Wohnungsbauprojekte und Umsetzungsblockaden",
        "Anders Wohnen. Zwischen Experimenten für nachhaltige Wohnungsbauprojekte und Umsetzungsblockaden",
        False,
    ),
    (
        1,
        "artikel-1-6.html",
        "Stefan Winter",
        "Holzbau und Klimawandel. Langfristige Holzverwendung in Holzbauwerken – Kohlenstoffspeicher und CO₂-Senke",
        "Holzbau und Klimawandel. Langfristige Holzverwendung in Holzbauwerken – Kohlenstoffspeicher und CO₂-Senke",
        False,
    ),
    (
        1,
        "artikel-1-7.html",
        "Thomas Ummenhofer",
        "Klimagerechtes Bauen mit Stahl",
        "Klimagerechtes Bauen mit Stahl",
        False,
    ),
    (
        1,
        "artikel-1-8.html",
        "Markus Stommel",
        "Kunststoffe im Kontext des nachhaltigen Bauens",
        "Kunststoffe im Kontext des nachhaltigen Bauens",
        False,
    ),
    (
        1,
        "artikel-1-9.html",
        "Bernd Hillemeier",
        "BETON gestern – heute – morgen",
        "BETON gestern – heute – morgen",
        False,
    ),
    # 2
    (
        2,
        "artikel-2-1.html",
        "Florian Summa",
        "Wände ohne Beipackzettel. Bauvorschriften als Anreiz zum nachhaltigen Bauen",
        "Wände ohne Beipackzettel. Bauvorschriften als Anreiz zum nachhaltigen Bauen",
        False,
    ),
    (
        2,
        "artikel-2-2.html",
        "Türk Schellenberg und Anja Schwarzlos",
        "Anders bauen – bauordnungsrechtlich möglich machen",
        "Anders bauen – bauordnungsrechtlich möglich machen",
        False,
    ),
    (
        2,
        "artikel-2-3.html",
        "Anna Menegazzi",
        "Die Merkmale zur ökologischen Nachhaltigkeit aus der Bauproduktenverordnung 2024 – ein Impuls für mehr Nachhaltigkeit und Innovation im Bausektor",
        "Die Merkmale zur ökologischen Nachhaltigkeit aus der Bauproduktenverordnung 2024 – ein Impuls für mehr Nachhaltigkeit und Innovation im Bausektor",
        False,
    ),
    (
        2,
        "artikel-2-4.html",
        "Jürgen Odszuck und Carla Jung-König",
        "Die Stadt als Rohstofflager – Vorbereitungen für Urban Mining auf einer Heidelberger Militärkonversionsfläche",
        "Die Stadt als Rohstofflager – Vorbereitungen für Urban Mining auf einer Heidelberger Militärkonversionsfläche",
        False,
    ),
    (
        2,
        "artikel-2-5.html",
        "Angelika Mettke",
        "Wiederverwendung von Betonfertigteilen – Nutzung wertvoller Baubestände für neue Bauvorhaben",
        "Wiederverwendung von Betonfertigteilen – Nutzung wertvoller Baubestände für neue Bauvorhaben",
        False,
    ),
    (
        2,
        "artikel-2-6.html",
        "Marcel de Groot",
        "Lebensort Vielfalt – Nachhaltig wohnen, vielfältig leben",
        "Lebensort Vielfalt – Nachhaltig wohnen, vielfältig leben",
        False,
    ),
    (
        2,
        "artikel-2-7.html",
        "Helena Gervásio",
        "Greenwashing in the construction sector",
        "Greenwashing in the construction sector",
        False,
    ),
    # 3
    (
        3,
        "artikel-3-1.html",
        "Christine Lemaitre",
        "Chancen und Grenzen des CO₂-Schattenpreises",
        "Chancen und Grenzen des CO₂-Schattenpreises",
        False,
    ),
    (
        3,
        "artikel-3-2.html",
        "Michael Jäger und Philip Leistner",
        "Ökobilanzierung als Hebel der Transformation",
        "Ökobilanzierung als Hebel der Transformation",
        False,
    ),
    (
        3,
        "artikel-3-3.html",
        "Johannes Wall, Christina Dallinger und Niklot von Bülow",
        "Fehlende Messbarkeit und Bewertungsgrundlagen für nachhaltige Bauprojekte",
        "Fehlende Messbarkeit und Bewertungsgrundlagen für nachhaltige Bauprojekte",
        False,
    ),
    (
        3,
        "artikel-3-4.html",
        "Claire Thomas",
        "Navigating the challenges to normalise building reuse",
        "Navigating the challenges to normalise building reuse",
        False,
    ),
    (
        3,
        "artikel-3-5.html",
        "Tobias Lehnert, im Gespräch mit Ulrike Kuhlmann und Yuca Meubrink",
        "Wie schaffen wir die Transformation der Stahlindustrie?",
        "Wie schaffen wir die Transformation der Stahlindustrie?",
        False,
    ),
    # 4
    (
        4,
        "artikel-4-1.html",
        "Reiner Nagel",
        "Gestaltung als Schlüssel für gelingendes Bauen",
        "Gestaltung als Schlüssel für gelingendes Bauen",
        False,
    ),
    (
        4,
        "artikel-4-2.html",
        "Ortwin Renn",
        "Akzeptanz von nachhaltigem Bauen und Wohnen. Ausgangskonzept und Erkenntnisse aus zwei Bürgerforen",
        "Akzeptanz von nachhaltigem Bauen und Wohnen. Ausgangskonzept und Erkenntnisse aus zwei Bürgerforen",
        False,
    ),
    (
        4,
        "artikel-4-3.html",
        "Thomas Gloning",
        "Nachhaltiges Bauen. Überlegungen zu sprachlichen, kommunikativen und medialen Hindernissen",
        "Nachhaltiges Bauen. Überlegungen zu sprachlichen, kommunikativen und medialen Hindernissen",
        False,
    ),
    (
        4,
        "artikel-4-4.html",
        "Yuca Meubrink, Johanna Klausing und Andreas Scheu",
        "Warum nachhaltiges Bauen nur schwer die Medien erreicht: Journalistische Perspektiven auf ein unterbelichtetes Thema",
        "Warum nachhaltiges Bauen nur schwer die Medien erreicht: Journalistische Perspektiven auf ein unterbelichtetes Thema",
        False,
    ),
    # 5
    (
        5,
        "artikel-5-1.html",
        "Benedict Esche",
        "Skeptizismus und fehlende Risikobereitschaft",
        "Skeptizismus und fehlende Risikobereitschaft",
        False,
    ),
    (
        5,
        "artikel-5-2.html",
        "Amandus Samsøe Sattler",
        "Suffizienz als Booster zum Erreichen der Klimaschutzziele",
        "Suffizienz als Booster zum Erreichen der Klimaschutzziele",
        False,
    ),
    (
        5,
        "artikel-5-3.html",
        "Ulrike Kuhlmann und Mike Schlaich",
        "Das Konzept der entwurfsorientierten und werkstoffübergreifenden Lehre im Bauingenieurstudium",
        "Das Konzept der entwurfsorientierten und werkstoffübergreifenden Lehre im Bauingenieurstudium",
        False,
    ),
    (
        5,
        "artikel-5-4.html",
        "Celina Hunschok, Johanna Ruge, Max Dombrowski und Oliver André Wege",
        "Zwischen Tragwerk und Tragweite. Das Berufsbild Bauingenieur:in in planetaren Grenzen",
        "Zwischen Tragwerk und Tragweite. Das Berufsbild Bauingenieur:in in planetaren Grenzen",
        True,
    ),
]


def site_header() -> str:
    return """    <header class="site-header">
      <a class="brand" href="index.html"
        >IAG Anders Bauen – für Ressourcenschonung und Klimaschutz</a
      >
      <nav aria-label="Hauptnavigation">
        <a href="index.html">KI-Synthese</a>
        <a href="einleitung.html" aria-current="page">Sammelbandartikel</a>
      </nav>
    </header>"""


FOOTER = """    <footer class="site-footer">
      <p>IAG Anders Bauen – für Ressourcenschonung und Klimaschutz</p>
    </footer>

    <script src="js/main.js"></script>
  </body>
</html>"""


def build_toc(active_file: str) -> str:
    by_section = {}
    for sec, filename, authors, title, toc_label, full in ARTICLES:
        by_section.setdefault(sec, []).append((filename, toc_label))

    chunks = [
        '      <nav class="topic-beam sammelband-toc" aria-label="Sammelbandartikel">'
    ]
    for key, label, num in SECTIONS:
        articles = by_section.get(key if key != "einleitung" else "einleitung", [])
        if key.startswith("kapitel-") and num is not None:
            articles = by_section.get(num, [])

        is_active_section = False
        sub_html = ""
        if key == "einleitung":
            active = active_file == "einleitung.html"
            ein_title = ARTICLES[0][4]
            link_cls = "topic-link is-active" if active else "topic-link"
            aria = ' aria-current="page"' if active else ""
            chunks.append(
                f'        <div class="topic-group{" is-open" if active else ""}" data-topic="{key}">'
            )
            chunks.append(
                f'          <a class="{link_cls}" href="einleitung.html"{aria}>{html.escape(ein_title)}</a>'
            )
            chunks.append("        </div>")
            continue

        if articles:
            for filename, toc_label in articles:
                if filename == active_file:
                    is_active_section = True
                cls = ' class="is-active" aria-current="page"' if filename == active_file else ""
                sub_html += (
                    f'            <a href="{filename}"{cls}>{html.escape(toc_label)}</a>\n'
                )

        open_cls = " is-open" if is_active_section else ""
        chunks.append(
            f'        <div class="topic-group{open_cls}" data-topic="{key}">'
        )
        chunks.append(f'          <span class="topic-label">{html.escape(label)}</span>')
        if sub_html:
            chunks.append('          <div class="topic-subnav">')
            chunks.append(sub_html.rstrip())
            chunks.append("          </div>")
        chunks.append("        </div>")

    chunks.append("      </nav>")
    return "\n".join(chunks)


def load_full_body() -> str:
    """Load previously extracted full article body for 5-4."""
    paras_path = root / "_article_paras.json"
    if not paras_path.exists():
        return "            <p>Beitrag folgt.</p>"

    paras = json.loads(paras_path.read_text(encoding="utf-8"))
    for i, p in enumerate(paras):
        if p.startswith("Celina Hunschok"):
            paras[i] = (
                "Celina Hunschok, Johanna Ruge, Max Dombrowski und Oliver André Wege"
            )

    # paras: title, subtitle, authors, org, keywords, ...
    keywords = paras[4] if len(paras) > 4 else ""
    body_paras = paras[5:]
    parts = []
    if keywords:
        parts.append(f'            <p class="article-keywords">{html.escape(keywords)}</p>')

    in_lit = False
    for p in body_paras:
        if p == "Literatur":
            in_lit = True
            parts.append('            <h3 id="literatur">Literatur</h3>')
            parts.append('            <ul class="article-literature">')
            continue
        if in_lit:
            parts.append(f"              <li>{html.escape(p)}</li>")
            continue
        m = re.match(r"^(\d+)\.\s+(.*)$", p)
        if m:
            num, text = m.group(1), m.group(2)
            parts.append(
                f'            <h3 class="numbered-heading" id="abschnitt-{num}">'
                f'<span class="heading-num">{num}.</span>'
                f'<span class="heading-text">{html.escape(text)}</span></h3>'
            )
        else:
            parts.append(f"            <p>{html.escape(p)}</p>")
    if in_lit:
        parts.append("            </ul>")
    return "\n".join(parts)


def pager(i: int) -> str:
    prev_link = ""
    next_link = ""
    if i > 0:
        prev_file = ARTICLES[i - 1][1]
        prev_link = (
            f'          <a class="pager-link pager-prev" href="{prev_file}">'
            f"← Vorheriger Beitrag</a>"
        )
    if i < len(ARTICLES) - 1:
        next_file = ARTICLES[i + 1][1]
        next_link = (
            f'          <a class="pager-link pager-next" href="{next_file}">'
            f"Nächster Beitrag →</a>"
        )
    return f"""        <nav class="article-pager" aria-label="Artikelnavigation">
{prev_link}
{next_link}
        </nav>"""


def render_page(i: int, full_body: str) -> str:
    sec, filename, authors, title, toc_label, has_full = ARTICLES[i]
    if has_full:
        body = full_body
        # For full article, show main title + authors; subtitle already in body as lead
        display_title = "Zwischen Tragwerk und Tragweite"
        subtitle_html = (
            '            <p class="article-subtitle">'
            "Das Berufsbild Bauingenieur:in in planetaren Grenzen</p>\n"
        )
    else:
        body = "            <p>Beitrag folgt.</p>"
        display_title = title
        subtitle_html = ""

    return f"""<!DOCTYPE html>
<html lang="de">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{html.escape(display_title)} – Sammelbandartikel</title>
    <link rel="stylesheet" href="css/styles.css" />
  </head>
  <body class="sammelband-page">
{site_header()}

    <div class="home-layout">
{build_toc(filename)}

      <main class="article-main">
{pager(i)}

        <article class="article">
          <header class="article-header">
            <h1>{html.escape(display_title)}</h1>
{subtitle_html}            <p class="article-authors">{html.escape(authors)}</p>
          </header>
          <div class="article-body prose-block">
{body}
          </div>
        </article>
      </main>
    </div>

{FOOTER}
"""


def main():
    full_body = load_full_body()

    # Remove old single article file if it will be replaced by dummies
    old = root / "artikel-5-1.html"
    # Will be overwritten

    for i, article in enumerate(ARTICLES):
        filename = article[1]
        html_out = render_page(i, full_body)
        (root / filename).write_text(html_out, encoding="utf-8")
        print("wrote", filename)

    print("done", len(ARTICLES), "pages")


if __name__ == "__main__":
    main()
