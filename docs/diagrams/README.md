# Diagrams

Every SVG in this directory is **generated**. Edit the Python, not the markup.

```bash
python docs/diagrams/generate_diagrams.py     # or: npm run diagrams
```

| File | What it shows |
|---|---|
| `01-system-architecture.svg` | Both runtimes side by side, and what each one depends on |
| `02-indexing-pipeline.svg` | PDF to FAISS index, and what each step costs you |
| `03-query-flow.svg` | One turn through the console, grounded path and fallback |
| `04-answer-contract.svg` | The four response fields, mapped onto the rendered card |
| `05-request-sequence.svg` | The web client's request, from keystroke to card |
| `06-frontend-composition.svg` | Component tree, state ownership, module boundaries |

## How they are built

- `_engine.py` — the drawing library: palette, type scale, box and cylinder
  shapes, stick figures, page glyphs, connectors, frames. Change it once and
  every figure changes together.
- `generate_diagrams.py` — one function per figure, holding only content and layout.

## Conventions

- **A thin framed figure** with its title sitting on the top border.
- **Compact flat-coloured boxes**, short labels, small grey sub-lines. The
  picture carries the shape of the system; the prose around it carries detail.
- **Colour is semantic**, never decorative: blue is a client surface, black an
  application service, green retrieval or a store, yellow a model provider,
  orange an output, red a stated limitation.
- **Stick figures for people, page glyphs for documents, a cylinder for a store.**
- **Thin black connectors** with small captions; dashed means conditional or
  a return value; a double head means request and response.
- **No external assets and no web fonts** — the files render identically on
  GitHub, in a PDF export, and in slides.
