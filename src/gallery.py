#!/usr/bin/env python3
"""Draw every preset coat in one labeled SVG (examples/gallery-*.svg)."""
import argparse
import re

import cat

COLS = 4
CELL_W = cat.CAT_W + cat.IDLE_GAP
LABEL_H = 30


def gallery(theme):
    names = list(cat.PRESETS)
    one = cat.build([cat.parse_cat(names[0])], 0, CELL_W, theme)
    style = re.search(r"<style>.*?</style>", one, re.S).group(0)
    cat_h = int(re.search(r'height="(\d+)"', one).group(1))
    cell_h = cat_h + LABEL_H
    rows = -(-len(names) // COLS)
    width, height = COLS * CELL_W, rows * cell_h
    ink = "#2b2b2b" if theme == "light" else "#d0d0d0"
    cells = []
    for i, name in enumerate(names):
        x, y = i % COLS * CELL_W, i // COLS * cell_h
        drawn = cat.cat_svg(cat.parse_cat(name), "idle", CELL_W, 0, 1)
        cells.append(
            f'<g transform="translate({x},{y})">'
            f'<g transform="translate(0,{cat.S + 2})">{drawn}</g>'
            f'<text x="{CELL_W / 2:g}" y="{cat_h + 18}" text-anchor="middle" fill="{ink}" '
            f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="16">{name}</text></g>'
        )
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" shape-rendering="crispEdges">\n'
            f'<title>github-readme-cat coats: {", ".join(names)}</title>\n{style}\n'
            f'{"".join(cells)}\n</svg>\n')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--theme", choices=["light", "dark"], default="light")
    ap.add_argument("--out", default="gallery.svg")
    a = ap.parse_args()
    with open(a.out, "w") as f:
        f.write(gallery(a.theme))
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
