# Diagrams

Every SVG in this directory is **generated**. Edit the Python, not the markup.

```bash
python docs/diagrams/generate_diagrams.py     # or: npm run diagrams
```

| File | What it shows |
|---|---|
| `01-system-architecture.svg` | Both runtimes, layer by layer, and what each depends on |
| `02-indexing-pipeline.svg` | PDF to FAISS index, with the chunking parameters |
| `03-query-flow.svg` | One turn through the console, including the ungrounded fallback |
| `04-answer-contract.svg` | The four response fields, mapped onto the rendered card |
| `05-request-sequence.svg` | The web client's request, from keystroke to card, with the failure path |
| `06-frontend-composition.svg` | Component tree, state ownership, module boundaries |

## How they are built

- `_engine.py` — the drawing library: palette, type scale, node anatomy,
  connectors, frames, page chrome. Change it and every diagram changes together.
- `generate_diagrams.py` — one function per figure, holding only content and layout.

## Conventions

- **Square corners.** Nothing is rounded.
- **Colour is semantic**, never decorative: blue is a client surface, black an
  application service, green a retrieval step, amber a model provider, violet a
  store, red a stated limitation.
- **Every node carries a kicker, a title and a detail line**, so a figure reads
  without its legend.
- **Connectors are orthogonal and labelled**; a dashed line means optional,
  conditional, or implicit.
- **No external assets and no web fonts** — the files render identically on
  GitHub, in a PDF, and in slides.
