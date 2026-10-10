# recipe_art

Generates the flat SVG illustrations used for recipes (`frontend/public/images/*.svg`).

- `helpers.py` — canvas constants (`W`, `H`, `CX`, `CY`) and reusable shapes: backgrounds (`cloth`, `wood`), `blob`, `leaf`, `shadow`, `chopsticks`, and set-meal tray parts (`tray`, `rice_bowl`, `miso_bowl`, `takuan_dish`).
- `ham_egg_teishoku.py` — a complete example. Copy it for a new recipe, change the drawing function and output filename, then run it:

```bash
python3 tools/recipe_art/ham_egg_teishoku.py
```

Images are seeded with a fixed `random.Random(n)`, so re-running a script reproduces the same picture. Keep new images in the same style: 800x600, top-down view, a plate or bowl centered on a simple patterned background.
