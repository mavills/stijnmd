#!/usr/bin/env python3
"""Convert markdown blog posts to standalone HTML files."""

import re
import sys
from datetime import datetime
from pathlib import Path

import markdown

TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} &mdash; stijn.md</title>
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/geist@1/dist/fonts/geist-sans/style.min.css">
  <link rel="stylesheet" href="/style.css">
</head>
<body>
  <div class="page">
    <a href="/blog/" class="back">&larr; Blog</a>
    <article>
      <header>
        <h1>{title}</h1>
        <time datetime="{date_iso}">{date_display}</time>
      </header>
      {body}
    </article>
  </div>
  <footer>
    <p>&copy; {year} Stijn</p>
  </footer>
</body>
</html>
"""

FILENAME_PATTERN = re.compile(r"^(\d{4}-\d{2}-\d{2})-(.+)\.md$")


def parse_md(path: Path) -> tuple[str, str, str]:
    text = path.read_text()

    title_match = re.match(r"^#\s+(.+)$", text, re.MULTILINE)
    if not title_match:
        raise ValueError(f"No '# title' found in {path}")
    title = title_match.group(1).strip()

    body = text[title_match.end() :].strip()

    html_body = markdown.markdown(body)

    return title, html_body


def build_post(md_path: Path) -> Path:
    match = FILENAME_PATTERN.match(md_path.name)
    if not match:
        raise ValueError(
            f"Filename must be YYYY-MM-DD-slug.md, got: {md_path.name}"
        )

    date_str, slug = match.group(1), match.group(2)
    date = datetime.strptime(date_str, "%Y-%m-%d")

    title, body = parse_md(md_path)

    html = TEMPLATE.format(
        title=title,
        date_iso=date_str,
        date_display=date.strftime("%B %-d, %Y"),
        year=date.year,
        body=body,
        slug=slug,
    )

    out_path = md_path.with_name(f"{slug}.html")
    out_path.write_text(html)
    return out_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <post.md> [post2.md ...]")
        sys.exit(1)

    for arg in sys.argv[1:]:
        path = Path(arg)
        if not path.exists():
            print(f"Error: {path} not found", file=sys.stderr)
            sys.exit(1)
        out = build_post(path)
        print(f"{path.name} -> {out.name}")
