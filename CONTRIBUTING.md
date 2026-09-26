# Contributing

Thanks for taking an interest in Siraj.

## Getting set up

```bash
npm install                                   # web client
pip install -r rag_console/requirements.txt   # RAG console
```

Copy `.env.example` to `.env.local` and add a Gemini key if you want the web
client to answer. The app runs without one — it opens with a notice instead.

## Before opening a pull request

```bash
npm run typecheck        # strict TypeScript, must be clean
npm run build            # must succeed
npm run diagrams         # if you touched docs/diagrams/
git diff --exit-code -- docs/diagrams
```

CI runs the same four checks. The last one matters: the SVGs under
`docs/diagrams/` are build output. Edit `generate_diagrams.py` and regenerate —
a hand-edited SVG will fail the build.

## House style

- **TypeScript is strict.** No `any` in new code; give failures a `SirajErrorCode`
  rather than a bare `Error`.
- **Components stay presentational.** Turn logic belongs in `hooks/useChat.ts`,
  and provider calls belong in `services/`. Nothing else should import a model SDK.
- **The interface is Arabic and right-to-left.** User-visible strings are Arabic;
  code, comments and commit messages are English.
- **Comments explain why.** The what is already in the code.

## What is most useful right now

1. **A labelled retrieval evaluation set** — questions paired with the passages
   that should be retrieved. Without one, chunk tuning is guesswork.
2. **Arabic-first embeddings** measured against `nomic-embed-text-v1.5` on that set.
3. **Arabic text normalisation** at index time: alef forms, ta marbuta, tashkeel.
4. **An OCR ingestion path** so scanned manuscripts can be indexed at all.
5. **A server-side retrieval API** so the web client can stop asserting citations
   and start retrieving them.

## Reporting a problem with an answer

If the assistant produced a citation that does not check out, that is the most
important kind of bug in this project. Please open an issue with the question
asked, the reply, and the correct reference if you know it.
