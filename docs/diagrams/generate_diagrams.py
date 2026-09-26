"""
Generate the Siraj documentation diagrams.

    python docs/diagrams/generate_diagrams.py

Every SVG in `docs/diagrams/` is build output - edit the definitions here, not
the markup. Drawing primitives and the palette live in `_engine.py`.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _engine import (  # noqa: E402
    BLUE, DARK, GRAY, GREEN, ORANGE, RED, YELLOW, Box, Cylinder, Diagram,
    FAINT, INK, LINE, PAPER, actor, arrow, brace, caption, dot, frame, line,
    page, panel, rect, row, tx,
)

OUT = os.path.dirname(os.path.abspath(__file__))
LEGEND = [
    ("client", BLUE),
    ("service", DARK),
    ("retrieval", GREEN),
    ("model API", YELLOW),
    ("output", ORANGE),
]


def out(name):
    return os.path.join(OUT, name)


# ==========================================================================
# 01 - System architecture
# ==========================================================================


def system_architecture():
    d = Diagram(1180, 648)
    d.add(frame(40, 50, 1100, 540, "System Architecture"))

    # ---- A: web client ---------------------------------------------------
    d.add(panel(70, 110, 1040, 190, "A  ·  web client"))
    d.add(actor(112, 175, "User", "Arabic"))

    spa = Box(182, 143, 150, 64, BLUE, "React SPA", ["Vite · Tailwind · RTL"], port=":3000")
    svc = Box(402, 143, 165, 64, DARK, "geminiService", ["prompt · schema", "validation"])
    gem = Box(637, 143, 165, 64, YELLOW, "Gemini 2.5 Flash", ["responseSchema enforced"])
    d.add(spa.svg(), svc.svg(), gem.svg())

    d.add(arrow((134, 175), spa.left, "browser"))
    d.add(arrow(spa.right, svc.left, "in-process", bidir=True))
    d.add(arrow(svc.right, gem.left, "HTTPS", bidir=True))

    card = Box(402, 240, 165, 48, ORANGE, "4-field answer",
               ["answer · passage · source · note"], title_size=11)
    d.add(card.svg())
    d.add(arrow(svc.bottom, card.top))
    d.add(arrow(card.left, (290, 207), "render", pts=[(402, 264), (290, 264), (290, 207)],
                label_dy=-6))

    d.add(caption(880, 236, ["no retrieval step -", "citations are produced by the model,",
                             "not looked up"], fill="#B03A2E"))

    # ---- B: RAG console --------------------------------------------------
    d.add(panel(70, 320, 1040, 240, "B  ·  RAG console"))
    d.add(actor(112, 380, "Researcher"))

    ui = Box(182, 348, 150, 64, BLUE, "Streamlit console", ["chat · sidebar"], port=":8501")
    chain = Box(402, 348, 165, 64, DARK, "RAG chain", ["prompt | model | parser"])
    ret = Box(637, 348, 150, 64, GREEN, "Retriever", ["similarity_search", "k = 3"])
    groq = Box(857, 348, 150, 64, YELLOW, "Groq LLM", ["gemma2 · llama-3.x"])
    d.add(ui.svg(), chain.svg(), ret.svg(), groq.svg())

    d.add(arrow((134, 380), ui.left, "browser"))
    d.add(arrow(ui.right, chain.left, "in-process", bidir=True))
    d.add(arrow(chain.right, ret.left, "question"))
    d.add(arrow(ret.right, groq.left, "context", bidir=True))

    store = Cylinder(637, 455, 150, 60, GREEN, "FAISS index", ["in memory"])
    d.add(store.svg())
    d.add(arrow(store.top, ret.bottom, bidir=True))
    d.add(caption(722, 438, "search", anchor="start"))

    d.add(page(300, 478, "PDF corpus", "text layer required"))
    nomic = Box(402, 458, 165, 50, YELLOW, "Nomic embeddings", ["nomic-embed-text-v1.5"],
                title_size=11)
    d.add(nomic.svg())
    d.add(arrow((320, 483), nomic.left, "chunks"))
    d.add(arrow(nomic.right, store.left, "vectors"))

    d.legend(LEGEND, 590, 622)
    d.save(out("01-system-architecture.svg"))


# ==========================================================================
# 02 - Indexing pipeline
# ==========================================================================


def indexing_pipeline():
    d = Diagram(1180, 340)
    d.add(frame(40, 50, 1100, 222, "Indexing Flow"))

    d.add(actor(104, 146, "User"))
    d.add(page(190, 142, "PDF", "uploaded once"))

    app = Box(262, 118, 115, 56, DARK, "Streamlit", ["file_uploader"])
    pages = Box(430, 118, 115, 56, BLUE, "Pages", ["PyPDFLoader", "one per page"])
    chunks = Box(598, 118, 125, 56, GREEN, "Chunks", ["500 chars", "overlap 50"])
    embed = Box(790, 118, 130, 56, YELLOW, "Nomic API", ["one vector per chunk"])
    store = Cylinder(968, 112, 130, 68, GREEN, "FAISS index", ["session state"])
    d.add(app.svg(), pages.svg(), chunks.svg(), embed.svg(), store.svg())

    d.add(arrow((209, 146), app.left, "upload"))
    d.add(arrow(app.right, pages.left, "load"))
    d.add(arrow(pages.right, chunks.left, "split"))
    d.add(arrow(chunks.right, (751, 146)))
    d.add(dot(761, 146))
    d.add(arrow((771, 146), embed.left, head=False))
    d.add(arrow(embed.right, store.left, "vectors"))

    d.add(caption(190, 202, ["scanned pages need OCR first -", "there is nothing to chunk",
                             "without a text layer"]))
    d.add(caption(660, 202, ["chunk size and overlap are sliders; moving",
                             "one does nothing until the index is rebuilt"]))
    d.add(caption(1033, 202, ["held in RAM, not on disk -", "a refresh clears it"]))

    d.legend(LEGEND, 590, 316)
    d.save(out("02-indexing-pipeline.svg"))


# ==========================================================================
# 03 - Query flow
# ==========================================================================


def query_flow():
    d = Diagram(1180, 482)
    d.add(frame(40, 50, 1100, 372, "Query & Answer Flow"))

    slots = row(186, 1112, 6, 40)
    store = Cylinder(slots[1][0] + slots[1][1] / 2.0 - 75, 74, 150, 52, GREEN, "FAISS index")
    d.add(store.svg())
    y1, y2, h = 152, 292, 58

    # ---- grounded path ---------------------------------------------------
    d.add(actor(104, 181, "User"))
    chain = Box(slots[0][0], y1, slots[0][1], h, DARK, "RAG chain")
    ret = Box(slots[1][0], y1, slots[1][1], h, GREEN, "Retriever", ["k = 3"])
    ctx = Box(slots[2][0], y1, slots[2][1], h, BLUE, "Context", ["3 passages"])
    prompt = Box(slots[3][0], y1, slots[3][1], h, GREEN, "RAG prompt")
    llm = Box(slots[4][0], y1, slots[4][1], h, YELLOW, "Groq LLM")
    ans = Box(slots[5][0], y1, slots[5][1], h, ORANGE, "Answer", ["sources shown"])
    d.add(chain.svg(), ret.svg(), ctx.svg(), prompt.svg(), llm.svg(), ans.svg())

    d.add(arrow((126, 181), chain.left, "question"))
    d.add(arrow(chain.right, ret.left, "embed"))
    d.add(arrow(ret.right, ctx.left, "top-k"))
    d.add(arrow(ctx.right, prompt.left, "fill slot"))
    d.add(arrow(prompt.right, llm.left, "stream"))
    d.add(arrow(llm.right, ans.left, "tokens"))
    d.add(arrow(store.bottom, ret.top, bidir=True))
    d.add(caption(ret.cx + 14, 140, "search", anchor="start"))

    # ---- fallback path ---------------------------------------------------
    d.add(actor(104, 321, "User"))
    chain2 = Box(slots[0][0], y2, slots[0][1], h, DARK, "RAG chain")
    none = Box(slots[1][0], y2, slots[1][1] + slots[2][1] + 40, h, RED,
               "No index in this session", ["nothing to retrieve, nothing to cite"])
    plain = Box(slots[3][0], y2, slots[3][1], h, GRAY, "Plain prompt")
    llm2 = Box(slots[4][0], y2, slots[4][1], h, YELLOW, "Groq LLM")
    ans2 = Box(slots[5][0], y2, slots[5][1], h, ORANGE, "Answer", ["marked unsourced"])
    d.add(chain2.svg(), none.svg(), plain.svg(), llm2.svg(), ans2.svg())

    d.add(arrow((126, 321), chain2.left, "question"))
    d.add(arrow(chain2.right, none.left))
    d.add(arrow(none.right, plain.left))
    d.add(arrow(plain.right, llm2.left, "stream"))
    d.add(arrow(llm2.right, ans2.left, "tokens"))

    d.add(caption(590, 384, ["With no index loaded the chain switches prompt and says so, instead of",
                             "quietly answering from model memory as though it were sourced."]))

    d.legend(LEGEND, 590, 458)
    d.save(out("03-query-flow.svg"))


# ==========================================================================
# 04 - Answer contract
# ==========================================================================


def answer_contract():
    d = Diagram(1180, 470)
    d.add(frame(40, 50, 1100, 372, "Answer Contract"))

    gem = Box(76, 190, 145, 56, YELLOW, "Gemini 2.5 Flash")
    schema = Box(266, 190, 160, 56, DARK, "responseSchema", ["four required fields"])
    d.add(gem.svg(), schema.svg())
    d.add(arrow(gem.right, schema.left, "JSON"))

    fields = [
        (BLUE, "rephrasedAnswer", "the explanation, in Arabic"),
        (GREEN, "originalText", "the passage, quoted"),
        (ORANGE, "source", "name + reference"),
        (GRAY, "aiNote", "how it was produced"),
    ]
    boxes = []
    for i, (style, name, note) in enumerate(fields):
        b = Box(500, 100 + i * 62, 190, 48, style, name, [note], title_size=11)
        boxes.append(b)
        d.add(b.svg())
    d.add(brace(474, 100, 334))
    d.add(arrow(schema.right, (468, 218)))

    # ---- the rendered card ----------------------------------------------
    cx0, cw = 770, 320
    d.add(tx(cx0, 92, "rendered message card", size=9.5, weight=600, fill=FAINT,
             anchor="start"))
    d.add(rect(cx0, 100, cw, 246, fill=PAPER, stroke="#C8C8C8", sw=1.2))
    d.add(rect(cx0 + 16, 114, 22, 22, fill="#0E8F6E", stroke="#0E8F6E", sw=1, r=3))
    d.add(tx(cx0 + 27, 130, "S", size=11, weight=700, fill=PAPER))
    d.add(tx(cx0 + 46, 130, "Assistant", size=9.5, weight=600, fill=INK, anchor="start"))

    bands = [
        ("Answer", "#E8EFFB", "#6D9EEB", 148, 46),
        ("Original passage", "#EAF4E3", "#82B366", 200, 46),
        ("Source", "#FDEEDC", "#E69138", 252, 42),
        ("Note", "#F2F2F2", "#B7B7B7", 300, 34),
    ]
    band_cy = []
    for label, fill, border, by, bh in bands:
        d.add(rect(cx0 + 16, by, cw - 32, bh, fill=fill, stroke=border, sw=1))
        d.add(tx(cx0 + 28, by + 14, label, size=8.6, weight=600, fill="#4A4A4A",
                 anchor="start"))
        for k in range(2 if bh > 40 else 1):
            d.add(line(cx0 + 28, by + 27 + k * 9, cx0 + cw - 44 - k * 46, by + 27 + k * 9,
                       stroke=border, sw=3))
        band_cy.append(by + bh / 2.0)

    for b, target in zip(boxes, band_cy):
        d.add(arrow(b.right, (cx0, target), route="h", mid=730, sw=1))

    d.add(caption(590, 400, ["A missing field or malformed JSON raises a typed error. A card with a blank "
                             "source line reads as a citation while carrying none, so it is never rendered."]))
    d.save(out("04-answer-contract.svg"))


# ==========================================================================
# 05 - Request sequence
# ==========================================================================


def request_sequence():
    d = Diagram(1180, 560)
    d.add(frame(40, 50, 1100, 462, "Request Sequence  ·  Web Client"))

    lanes = [
        ("User", BLUE), ("React SPA", BLUE), ("geminiService", DARK),
        ("Gemini API", YELLOW), ("Message card", ORANGE),
    ]
    slots = row(72, 1108, len(lanes), 28)
    cx = []
    for (x, w), (name, style) in zip(slots, lanes):
        b = Box(x, 80, w, 44, style, name, title_size=11)
        cx.append(b.cx)
        d.add(b.svg())
        d.add(line(b.cx, 124, b.cx, 446, stroke="#BFBFBF", sw=1, dash="3 4"))

    msgs = [
        (0, 1, 168, "types a question in Arabic", False),
        (1, 2, 212, "getIslamicBotResponse(query)", False),
        (2, 3, 256, "generateContent(prompt, responseSchema)", False),
        (3, 2, 300, "JSON payload", True),
        (2, 1, 392, "typed GeminiResponse", True),
        (1, 4, 428, "assistant message", False),
    ]
    for a, b, y, label, dashed in msgs:
        x1, x2 = cx[a], cx[b]
        s = 1 if x2 > x1 else -1
        d.add(arrow((x1 + s * 4, y), (x2 - s * 4, y), label, dashed=dashed))

    # self-call on the service lane
    sx = cx[2]
    d.add('<path d="M%.1f,%.1f h40 v22 h-36" fill="none" stroke="%s" stroke-width="1.1" '
          'marker-end="url(#tip)"/>' % (sx, 336, LINE))
    d.add(caption(sx + 50, 352, "validate against the contract", anchor="start"))

    d.add(caption(sx + 50, 366, "on failure: typed SirajError, rendered as a failed card",
                  anchor="start", fill="#B03A2E"))

    d.add(caption(590, 478, ["Every failure carries a SirajErrorCode, so the interface explains what went",
                             "wrong in Arabic instead of showing a provider stack trace."]))
    d.save(out("05-request-sequence.svg"))


# ==========================================================================
# 06 - Frontend composition
# ==========================================================================


def frontend_composition():
    d = Diagram(1180, 430)
    d.add(frame(40, 50, 1100, 330, "Frontend Composition"))

    d.add(panel(70, 96, 660, 256, "component tree"))
    app = Box(292, 124, 190, 52, DARK, "App.tsx", ["renders, holds no logic"])
    d.add(app.svg())

    kids = row(92, 708, 4, 18)
    names = ["Header.tsx", "MessageList", "ChatInput.tsx", "Feedback.tsx"]
    child_boxes = []
    for (x, w), name in zip(kids, names):
        b = Box(x, 212, w, 48, BLUE, name, title_size=10.5)
        child_boxes.append(b)
        d.add(b.svg())
    d.add(line(child_boxes[0].cx, 192, child_boxes[-1].cx, 192, stroke=LINE, sw=1.1))
    d.add(line(app.cx, 176, app.cx, 192, stroke=LINE, sw=1.1))
    for b in child_boxes:
        d.add(arrow((b.cx, 192), (b.cx, 212)))

    for name, x in (("Message.tsx", 190), ("EmptyState.tsx", 356)):
        b = Box(x, 292, 150, 44, BLUE, name, title_size=10.5)
        d.add(b.svg())
        d.add(arrow((child_boxes[1].cx, 260), (x + 75, 292), route="v", mid=276))

    d.add(panel(772, 96, 338, 256, "modules"))
    mods = [
        (GREEN, "hooks/useChat.ts", "turns · cancellation · failures", 128),
        (YELLOW, "services/geminiService.ts", "the only provider boundary", 196),
        (GRAY, "types · config · lib/errors", "shared vocabulary", 264),
    ]
    prev = None
    for style, name, note, y in mods:
        b = Box(796, y, 290, 52, style, name, [note], title_size=10.5)
        d.add(b.svg())
        if prev is not None:
            d.add(arrow(prev.bottom, b.top))
        prev = b

    d.add(arrow(app.right, (796, 154), "calls", route="h", mid=752))
    d.add(caption(590, 368, ["Swap geminiService for a real retrieval backend and nothing else moves."]))
    d.save(out("06-frontend-composition.svg"))


def main():
    system_architecture()
    indexing_pipeline()
    query_flow()
    answer_contract()
    request_sequence()
    frontend_composition()


if __name__ == "__main__":
    main()
