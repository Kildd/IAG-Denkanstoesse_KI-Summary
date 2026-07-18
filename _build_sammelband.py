# -*- coding: utf-8 -*-
"""Generate Sammelbandartikel pages with shared TOC and prev/next navigation."""
from pathlib import Path
import html
import json
import re

from _sammelband_content import CHAPTER_INTROS, EINLEITUNG_SECTIONS, LITERATURE

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
        "Einleitung",
        True,
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
        "Benedikt Esche",
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


def chapter_file(num: int) -> str:
    return f"kapitel-{num}.html"


def articles_in_section(num: int):
    return [a for a in ARTICLES if a[0] == num]


def build_toc(active_file: str) -> str:
    chunks = [
        '      <nav class="topic-beam sammelband-toc" aria-label="Sammelbandartikel">'
    ]
    for key, label, num in SECTIONS:
        if key == "einleitung":
            active = active_file == "einleitung.html"
            link_cls = "topic-link is-active" if active else "topic-link"
            aria = ' aria-current="page"' if active else ""
            authors = ARTICLES[0][2]
            chunks.append(
                f'        <div class="topic-group" data-topic="{key}">'
            )
            chunks.append(
                f'          <a class="{link_cls}" href="einleitung.html"{aria}>'
                f'<span class="toc-entry-title">Einleitung</span>'
                f'<span class="toc-entry-authors">{html.escape(authors)}</span>'
                f"</a>"
            )
            chunks.append("        </div>")
            continue

        chapter_href = chapter_file(num)
        is_chapter = active_file == chapter_href
        articles = articles_in_section(num)
        is_article = any(filename == active_file for _, filename, *_ in articles)
        is_open = is_chapter or is_article
        link_cls = "topic-link is-active" if is_open else "topic-link"
        aria = ' aria-current="page"' if is_chapter else ""

        sub_html = ""
        for _, filename, authors, _title, toc_label, _full in articles:
            cls = (
                ' class="is-active" aria-current="page"'
                if filename == active_file
                else ""
            )
            sub_html += (
                f'            <a href="{filename}"{cls}>'
                f'<span class="toc-entry-title">{html.escape(toc_label)}</span>'
                f'<span class="toc-entry-authors">{html.escape(authors)}</span>'
                f"</a>\n"
            )

        open_cls = " is-open" if is_open else ""
        chunks.append(
            f'        <div class="topic-group{open_cls}" data-topic="{key}">'
        )
        chunks.append(
            f'          <a class="{link_cls}" href="{chapter_href}"{aria}>'
            f"{html.escape(label)}</a>"
        )
        if sub_html:
            chunks.append('          <div class="topic-subnav">')
            chunks.append(sub_html.rstrip())
            chunks.append("          </div>")
        chunks.append("        </div>")

    chunks.append("      </nav>")
    return "\n".join(chunks)


# Author/name phrases as they appear in chapter intros → article file
ARTICLE_LINK_PHRASES = [
    (
        "Celina Hunschok, Johanna Ruge, Max Dombrowski und Oliver André Wege",
        "artikel-5-4.html",
    ),
    (
        "Johannes Wall, Christina Dallinger und Niklot von Bülow",
        "artikel-3-3.html",
    ),
    (
        "Yuca Meubrink, Johanna Klausing und Andreas Scheu",
        "artikel-4-4.html",
    ),
    (
        "Yuca Meubrink, Mike Schlaich und Ulrike Kuhlmann",
        "artikel-1-2.html",
    ),
    ("Jürgen Odszuck und Carla Jung-König", "artikel-2-4.html"),
    ("Türk Schellenberg und Anja Schwarzlos", "artikel-2-2.html"),
    ("Michael Jäger und Philip Leistner", "artikel-3-2.html"),
    ("Ulrike Kuhlmann und Mike Schlaich", "artikel-5-3.html"),
    ("Amandus Samsøe Sattler", "artikel-5-2.html"),
    ("Helena Gervásio", "artikel-2-7.html"),
    ("Christine Lemaitre", "artikel-3-1.html"),
    ("Angelika Mettke", "artikel-2-5.html"),
    ("Anna Menegazzi", "artikel-2-3.html"),
    ("Marcel de Groot", "artikel-2-6.html"),
    ("Florian Summa", "artikel-2-1.html"),
    ("Thomas Ummenhofer", "artikel-1-7.html"),
    ("Benedikt Esche", "artikel-5-1.html"),
    ("Philippe Block", "artikel-1-1.html"),
    ("Andreas Hofer", "artikel-1-3.html"),
    ("Achim Menges", "artikel-1-4.html"),
    ("Cordula Kropp", "artikel-1-5.html"),
    ("Stefan Winter", "artikel-1-6.html"),
    ("Markus Stommel", "artikel-1-8.html"),
    ("Bernd Hillemeier", "artikel-1-9.html"),
    ("Claire Thomas", "artikel-3-4.html"),
    ("Tobias Lehnert", "artikel-3-5.html"),
    ("Reiner Nagel", "artikel-4-1.html"),
    ("Ortwin Renn", "artikel-4-2.html"),
    ("Thomas Gloning", "artikel-4-3.html"),
]


def linkify_article_mentions(text: str, from_page: str | None = None) -> str:
    """Escape plain text, then wrap known author mentions with article links."""
    result = html.escape(text)
    phrases = sorted(ARTICLE_LINK_PHRASES, key=lambda item: len(item[0]), reverse=True)
    placeholders = []
    for i, (phrase, href) in enumerate(phrases):
        needle = html.escape(phrase)
        if needle not in result:
            continue
        target = href
        if from_page:
            target = f"{href}?from={from_page}"
        token = f"@@ARTICLELINK{i}@@"
        result = result.replace(needle, token, 1)
        placeholders.append(
            (
                token,
                f'<a class="article-inline-link" href="{html.escape(target)}">'
                f"{needle}</a>",
            )
        )
    for token, link in placeholders:
        result = result.replace(token, link)
    return result


def paras_to_html(
    paragraphs, *, linkify: bool = False, from_page: str | None = None
) -> str:
    if linkify:
        return "\n".join(
            f"            <p>{linkify_article_mentions(p, from_page=from_page)}</p>"
            for p in paragraphs
        )
    return "\n".join(f"            <p>{html.escape(p)}</p>" for p in paragraphs)


def build_einleitung_body() -> str:
    parts = []
    for section in EINLEITUNG_SECTIONS:
        parts.append(
            f'            <h2 id="{html.escape(section["id"])}">'
            f'{html.escape(section["heading"])}</h2>'
        )
        parts.append(paras_to_html(section["paragraphs"]))
    parts.append('            <h2 id="literatur">Literatur</h2>')
    parts.append('            <ul class="article-literature">')
    for entry in LITERATURE:
        parts.append(f"              <li>{html.escape(entry)}</li>")
    parts.append("            </ul>")
    return "\n".join(parts)


def load_article_5_4_body() -> str:
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


def page_shell(
    filename: str,
    title: str,
    authors_html: str,
    body: str,
    pager_html: str,
    subtitle_html: str = "",
) -> str:
    return f"""<!DOCTYPE html>
<html lang="de">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{html.escape(title)} – Sammelbandartikel</title>
    <link rel="stylesheet" href="css/styles.css" />
  </head>
  <body class="sammelband-page">
{site_header()}

    <div class="home-layout">
{build_toc(filename)}

      <main class="article-main">
{pager_html}

        <article class="article">
          <header class="article-header">
            <h1>{html.escape(title)}</h1>
{subtitle_html}{authors_html}
          </header>
          <div class="article-body prose-block">
{body}
          </div>
        </article>
      </main>
    </div>

{FOOTER}
"""


def render_article_page(i: int, body_5_4: str, body_einleitung: str) -> str:
    sec, filename, authors, title, toc_label, has_full = ARTICLES[i]
    if filename == "einleitung.html":
        display_title = title
        subtitle_html = ""
        authors_html = (
            f'            <p class="article-authors">{html.escape(authors)}</p>\n'
        )
        body = body_einleitung
    elif has_full:
        display_title = "Zwischen Tragwerk und Tragweite"
        subtitle_html = (
            '            <p class="article-subtitle">'
            "Das Berufsbild Bauingenieur:in in planetaren Grenzen</p>\n"
        )
        authors_html = (
            f'            <p class="article-authors">{html.escape(authors)}</p>\n'
        )
        body = body_5_4
    else:
        display_title = title
        subtitle_html = ""
        authors_html = (
            f'            <p class="article-authors">{html.escape(authors)}</p>\n'
        )
        body = "            <p>Beitrag folgt.</p>"

    return page_shell(
        filename, display_title, authors_html, body, pager(i), subtitle_html
    )


def render_chapter_page(num: int) -> str:
    filename = chapter_file(num)
    label = next(label for key, label, n in SECTIONS if n == num)
    body_parts = [
        paras_to_html(CHAPTER_INTROS[num], linkify=True, from_page=filename)
    ]
    body_parts.append('            <h2>Beiträge in diesem Abschnitt</h2>')
    body_parts.append('            <ul class="chapter-article-list">')
    for _, art_file, authors, title, _toc, _full in articles_in_section(num):
        body_parts.append("              <li>")
        body_parts.append(
            f'                <a href="{art_file}?from={filename}">'
            f"{html.escape(title)}</a>"
        )
        body_parts.append(
            f'                <p class="chapter-article-authors">'
            f"{html.escape(authors)}</p>"
        )
        body_parts.append("              </li>")
    body_parts.append("            </ul>")

    first_art = articles_in_section(num)[0][1]
    next_href = f"{first_art}?from={filename}"
    pager_html = f"""        <nav class="article-pager" aria-label="Artikelnavigation">
          <a class="pager-link pager-prev" href="einleitung.html">← Zur Einleitung</a>
          <a class="pager-link pager-next" href="{next_href}">Erster Beitrag →</a>
        </nav>"""

    return page_shell(
        filename,
        label,
        "",
        "\n".join(body_parts),
        pager_html,
    )


def verify_chapter_links() -> None:
    """Ensure every non-Einleitung article is linkified once in its chapter intro."""
    expected = {
        filename
        for sec, filename, *_ in ARTICLES
        if isinstance(sec, int)
    }
    found = set()
    missing_phrases = []
    for num, paragraphs in CHAPTER_INTROS.items():
        blob = "\n".join(paragraphs)
        for phrase, href in ARTICLE_LINK_PHRASES:
            if href.startswith(f"artikel-{num}-") and phrase in blob:
                found.add(href)
            elif href.startswith(f"artikel-{num}-") and phrase not in blob:
                missing_phrases.append((href, phrase))
    missing = sorted(expected - found)
    if missing or missing_phrases:
        raise SystemExit(
            f"Chapter linkify incomplete. missing files={missing} "
            f"missing phrases={missing_phrases}"
        )


def main():
    verify_chapter_links()
    body_5_4 = load_article_5_4_body()
    body_einleitung = build_einleitung_body()

    for i, article in enumerate(ARTICLES):
        filename = article[1]
        html_out = render_article_page(i, body_5_4, body_einleitung)
        (root / filename).write_text(html_out, encoding="utf-8")
        print("wrote", filename)

    for num in range(1, 6):
        filename = chapter_file(num)
        html_out = render_chapter_page(num)
        (root / filename).write_text(html_out, encoding="utf-8")
        print("wrote", filename)

    print("done", len(ARTICLES) + 5, "pages")


if __name__ == "__main__":
    main()
