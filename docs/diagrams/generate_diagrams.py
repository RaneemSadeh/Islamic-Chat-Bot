"""
Generate the Siraj documentation diagrams.

    python docs/diagrams/generate_diagrams.py

Every SVG under `docs/diagrams/` is produced by this script - the files are
build output, so edit the definitions here rather than the markup. Diagrams are
plain SVG with no external assets, which keeps them sharp on GitHub, in PDF
exports and in slides.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _engine import (  # noqa: E402
    ALERT, BRAND, CLIENT, FAINT, HAIRLINE, INK, LEGEND, MODEL, MONO, MUTED,
    NOTE, PANEL, PAPER, RETRIEVE, RULE, SERVICE, STORE, Diagram, Node, actor,
    callout, columns, connect, cylinder, diamond, frame, kicker, line, path,
    plate, rail, rect, step, text_width, tx, wrap,
)

OUT = os.path.dirname(os.path.abspath(__file__))


def out(name):
    return os.path.join(OUT, name)


# ==========================================================================
# 01 - System architecture
# ==========================================================================


def system_architecture():
    W, H = 1580, 980
    d = Diagram(
        W, H,
        "System architecture",
        "Two runtimes share one purpose: answer an Arabic question and show where the answer came from.",
    )

    rail_x, rail_w = 60, 152
    a_x, a_w = 232, 424
    bl_x, br_x, b_w = 716, 1130, 370
    lane = 1540

    bands = [
        (166, "Experience", "What the user touches"),
        (310, "Orchestration", "Question to model call"),
        (454, "Retrieval", "Finding text to cite"),
        (598, "Inference", "Hosted model providers"),
        (742, "Knowledge", "Where the words come from"),
    ]
    BH = 110
    for y, title, sub in bands:
        d.add(rail(rail_x, y, rail_w, BH, title, sub))

    # column headers -------------------------------------------------------
    d.add(rect(a_x, 118, a_w, 30, fill=PANEL, stroke=HAIRLINE, sw=1.2))
    d.add('<rect x="%s" y="118" width="3" height="30" fill="#2557D6"/>' % a_x)
    d.add(kicker(a_x + 16, 137, "A - Web client - structured, cited answers", "#2557D6"))
    d.add(rect(bl_x, 118, 784, 30, fill=PANEL, stroke=HAIRLINE, sw=1.2))
    d.add('<rect x="%s" y="118" width="3" height="30" fill="#0E8F6E"/>' % bl_x)
    d.add(kicker(bl_x + 16, 137, "B - RAG console - retrieval over uploaded documents", "#0B7A5E"))

    # column A -------------------------------------------------------------
    a1 = Node(a_x, 166, a_w, BH, CLIENT, "React 19 single-page app",
              ["Vite 6 dev server, Tailwind, Tajawal type",
               "Right-to-left Arabic shell"], tag="browser", badge="TS")
    a2 = Node(a_x, 310, a_w, BH, SERVICE, "services/geminiService.ts",
              ["System instruction plus a strict response schema",
               "Typed errors, parsed and validated payload"], tag="answer service")
    a3 = Node(a_x, 454, a_w, BH, ALERT, "No local index",
              ["Citations are asserted by the model, not looked up.",
               "Treat them as leads to verify."], tag="known limitation")
    a4 = Node(a_x, 598, a_w, BH, MODEL, "Gemini 2.5 Flash",
              ["responseMimeType: application/json",
               "responseSchema enforced by the provider"], tag="google genai")
    a5 = Node(a_x, 742, a_w, BH, NOTE, "Parametric memory",
              ["Quran, hadith and fatwa wording recalled",
               "from the model weights"], tag="implicit source")
    d.add(a1.svg(), a2.svg(), a3.svg(), a4.svg(), a5.svg())

    d.add(connect(a1.bottom, a2.top, "question"))
    d.add(connect(a2.bottom, a3.top, "no retrieval step", dash="5 4", marker="soft"))
    d.add(connect(a3.bottom, a4.top, "prompt + schema"))
    d.add(connect(a5.top, (a5.cx, 708), "recall", dash="5 4", marker="soft"))

    # column B -------------------------------------------------------------
    b1 = Node(bl_x, 166, b_w, BH, CLIENT, "Streamlit chat console",
              ["Streamed tokens, clear and undo controls",
               "Full message history in session state"], tag="python app")
    b2 = Node(br_x, 166, b_w, BH, CLIENT, "Run configuration",
              ["Model picker, GROQ and Nomic keys",
               "chunk_size 100-1000, overlap 0-200"], tag="sidebar")
    b3 = Node(bl_x, 310, b_w, BH, SERVICE, "LangChain LCEL chain",
              ["prompt | ChatGroq | StrOutputParser"], tag="runnable", mono=True)
    b4 = Node(br_x, 310, b_w, BH, NOTE, "Grounding switch",
              ["Index present: retrieval prompt",
               "Index absent: plain chat prompt"], tag="branch")
    b5 = Node(bl_x, 454, 784, BH, RETRIEVE, "Retriever",
              ["database.similarity_search(question, k=3) - the three nearest chunks",
               "are concatenated into the context slot of the prompt"],
              tag="top-k over the vector index")
    b6 = Node(bl_x, 598, b_w, BH, MODEL, "Groq chat completions",
              ["gemma2-9b-it, llama-3.1-8b-instant,",
               "mixtral-8x7b-32768, llama3-8b-8192"], tag="generation")
    b7 = Node(br_x, 598, b_w, BH, MODEL, "Nomic embeddings",
              ["nomic-embed-text-v1.5",
               "one vector per chunk and per query"], tag="vectorisation")
    b8 = Node(bl_x, 742, b_w, BH, STORE, "Source PDFs",
              ["Quran, Sahih al-Bukhari, Sahih Muslim,",
               "IslamWeb exports, scanned manuscripts"], tag="corpus")
    d.add(b1.svg(), b2.svg(), b3.svg(), b4.svg(), b5.svg(), b6.svg(), b7.svg(), b8.svg())
    d.add(cylinder(br_x, 742, b_w, BH, STORE, "FAISS index",
                   "in memory, per session", tag="vector store"))

    d.add(connect(b1.bottom, b3.top, "question"))
    d.add(connect(b2.bottom, b4.top, "config", dash="5 4", marker="soft"))
    d.add(connect(b3.bottom, (b3.cx, 454), "retrieve"))
    d.add(connect(b4.bottom, (b4.cx, 454), "if indexed", dash="5 4", marker="soft"))
    d.add(connect((b3.cx, 564), b6.top, "context + history"))
    d.add(connect((b4.cx, 564), b7.top, "embed query"))
    d.add(connect((1086, 797), (1130, 797), marker="soft"))
    d.add(path([(1500, 797), (lane, 797), (lane, 509), (1500, 509)],
               stroke="#93A2B7", marker="soft"))

    d.legend(LEGEND, 60, 908)
    d.save(out("01-system-architecture.svg"))


# ==========================================================================
# 02 - Indexing pipeline
# ==========================================================================


def indexing_pipeline():
    W, H = 1520, 748
    d = Diagram(
        W, H,
        "Indexing pipeline",
        "How an uploaded PDF becomes a searchable vector index - run once per upload, before any question is asked.",
    )

    d.add(frame(60, 150, 1400, 230, "Build - streamlit sidebar, Create Database"))

    cols = columns(90, 1430, 5, 46)
    y, h = 196, 152
    specs = [
        (CLIENT, "Upload", ["st.file_uploader(type='pdf')",
                            "written to ./temp.pdf"], "source", True),
        (RETRIEVE, "Load pages", ["PyPDFLoader returns one",
                                  "Document per page with",
                                  "source and page metadata"], "pypdf", False),
        (RETRIEVE, "Split", ["RecursiveCharacterTextSplitter",
                             "chunk_size = 500",
                             "chunk_overlap = 50"], "chunking", True),
        (MODEL, "Embed", ["NomicEmbeddings",
                          "nomic-embed-text-v1.5",
                          "one vector per chunk"], "nomic api", False),
        (STORE, "Index", ["FAISS.from_documents(...)",
                          "flat index held in RAM"], "faiss", True),
    ]
    nodes = []
    for i, ((x, w), (style, title, detail, tag, mono)) in enumerate(zip(cols, specs)):
        n = Node(x, y, w, h, style, title, detail, tag=tag, mono=mono)
        nodes.append(n)
        d.add(n.svg())
        d.add(step(i + 1, x + w - 22, y - 1))
    for a, b in zip(nodes, nodes[1:]):
        d.add(connect(a.right, b.left, marker="head"))

    # what lands in session state
    store = Node(90, 440, 620, 104, STORE, "st.session_state.database",
                 ["The index is the only retrieval state the app keeps. It is not",
                  "written to disk, so a page refresh clears it."],
                 tag="run artefact", mono=False)
    d.add(store.svg())
    d.add(path([(nodes[-1].cx, 348), (nodes[-1].cx, 404), (400, 404), (400, 440)],
               stroke="#93A2B7", marker="soft"))

    # parameter panel
    d.add(frame(760, 440, 700, 104, "Tunable before the build", tone="#96630C"))
    d.add(tx(786, 472, "chunk_size", size=11.5, weight=600, fill=INK))
    d.add(tx(786, 518, "chunk_overlap", size=11.5, weight=600, fill=INK))
    for ty, lo, hi, val in ((478, 100, 1000, 500), (524, 0, 200, 50)):
        tx0, tw = 920, 380
        frac = (val - lo) / float(hi - lo)
        d.add(rect(tx0, ty - 3, tw, 6, fill="#E7ECF3", stroke="none", sw=0))
        d.add(rect(tx0, ty - 3, tw * frac, 6, fill="#B0740E", stroke="none", sw=0))
        d.add(rect(tx0 + tw * frac - 4, ty - 10, 8, 20, fill=PAPER, stroke="#B0740E", sw=1.6))
        d.add(tx(tx0 - 10, ty + 4, str(lo), size=10.4, fill=FAINT, anchor="end"))
        d.add(tx(tx0 + tw + 10, ty + 4, str(hi), size=10.4, fill=FAINT))
        d.add(tx(tx0 + tw * frac, ty - 18, str(val), size=10.6, weight=700,
                 fill="#96630C", anchor="middle"))

    body, ch = callout(
        60, 594, 1400, "Two things worth knowing", [
            "Chunk settings only take effect on the next build - moving a slider after the index exists changes nothing "
            "until Create Database is pressed again.",
            "Arabic text is split on characters, not tokens, so a 500-character chunk holds roughly 120-160 Arabic words. "
            "Short chunks sharpen retrieval and blunt context; long chunks do the opposite.",
        ], style=NOTE)
    d.add(body)
    d.save(out("02-indexing-pipeline.svg"))


# ==========================================================================
# 03 - Query flow
# ==========================================================================


def query_flow():
    W, H = 1240, 1232
    d = Diagram(
        W, H,
        "Query and answer flow",
        "One turn through the RAG console, including the ungrounded fallback path.",
    )

    L, R, CW = 60, 640, 540
    mid_x, mid_w = 310, 620

    q = Node(mid_x, 152, mid_w, 96, CLIENT, "Question typed in the chat box",
             ["st.chat_input, appended to history as a HumanMessage"], tag="turn starts")
    d.add(q.svg())

    d.add(connect(q.bottom, (620, 286), marker="head"))
    d.add(diamond(620, 336, 330, 104, "Is a FAISS index loaded?",
                  "st.session_state.database"))

    d.add(path([(455, 336), (L + CW / 2, 336), (L + CW / 2, 410)], marker="head"))
    d.add(plate(L + CW / 2 + 74, 320, "yes - grounded"))
    d.add(path([(785, 336), (R + CW / 2, 336), (R + CW / 2, 410)], marker="soft",
               stroke="#93A2B7"))
    d.add(plate(R + CW / 2 - 78, 320, "no - fallback"))

    r1 = Node(L, 410, CW, 122, RETRIEVE, "Retrieve nearest chunks",
              ["database.similarity_search(question, k=3)",
               "returns three Documents with metadata"], tag="step 2a", mono=True)
    r2 = Node(L, 572, CW, 122, SERVICE, "Assemble the context slot",
              ["[doc.page_content for doc in search_docs]",
               "joined verbatim - no re-ranking, no dedupe"], tag="step 3a", mono=True)
    f1 = Node(R, 410, CW, 122, ALERT, "No passages to cite",
              ["The chain answers from model memory alone.",
               "Nothing in the reply can be traced to a source."], tag="step 2b")
    f2 = Node(R, 572, CW, 122, NOTE, "Plain assistant prompt",
              ["chat_history and user_question only -",
               "the context slot is left out of the template."], tag="step 3b")
    d.add(r1.svg(), r2.svg(), f1.svg(), f2.svg())
    d.add(connect(r1.bottom, r2.top, marker="head"))
    d.add(connect(f1.bottom, f2.top, marker="soft", stroke="#93A2B7"))

    p = Node(mid_x, 744, mid_w, 118, SERVICE, "ChatPromptTemplate",
             ["Slots: context, chat_history, user_question",
              "Instruction: answer from the context, say so when it is silent"],
             tag="step 4")
    d.add(p.svg())
    d.add(path([(r2.cx, 694), (r2.cx, 720), (mid_x + 160, 720), (mid_x + 160, 744)],
               marker="head"))
    d.add(path([(f2.cx, 694), (f2.cx, 720), (mid_x + mid_w - 160, 720),
                (mid_x + mid_w - 160, 744)], marker="soft", stroke="#93A2B7"))

    m = Node(mid_x, 906, mid_w, 96, MODEL, "ChatGroq(model).stream()",
             ["Chunks arrive as they are produced"], tag="step 5", mono=True)
    o = Node(mid_x, 1042, mid_w, 96, CLIENT, "st.write_stream, then AIMessage",
             ["Rendered live, then appended to chat_history"], tag="step 6")
    d.add(m.svg(), o.svg())
    d.add(connect(p.bottom, m.top, "final prompt"))
    d.add(connect(m.bottom, o.top, "token stream"))

    d.save(out("03-query-flow.svg"))


# ==========================================================================
# 04 - Answer contract
# ==========================================================================


def answer_contract():
    W, H = 1520, 860
    d = Diagram(
        W, H,
        "Grounded answer contract",
        "The web client refuses free prose: Gemini must return four named fields, and each one owns a region of the card.",
    )

    # ---- left: the schema -------------------------------------------------
    d.add(frame(60, 150, 520, 560, "responseSchema - services/geminiService.ts"))
    fields = [
        ("rephrasedAnswer", "string", "The explanation, in clear Arabic", CLIENT),
        ("originalText", "string", "The passage the answer rests on", RETRIEVE),
        ("source", "object", "name + reference (book, page, fatwa id)", STORE),
        ("aiNote", "string", "How the answer was produced, in English", NOTE),
    ]
    rows = []
    for i, (name, typ, desc, style) in enumerate(fields):
        y = 196 + i * 126
        n = Node(90, y, 460, 100, style, name, [typ + " - " + desc],
                 tag="field %d" % (i + 1), mono=False)
        rows.append(n)
        d.add(n.svg())

    # ---- right: the rendered card ----------------------------------------
    cx0, cw = 900, 560
    d.add(frame(cx0, 150, cw, 560, "Rendered message card - components/Message.tsx"))
    card_x, card_w = cx0 + 30, cw - 60
    d.add(rect(card_x, 186, card_w, 494, fill=PAPER, stroke="#D7DEE9", sw=1.4, shadow=True))

    # avatar + role
    d.add(rect(card_x + 20, 206, 34, 34, fill="#0E8F6E", stroke="#0E8F6E", sw=1))
    d.add(tx(card_x + 37, 229, "S", size=16, weight=700, fill=PAPER, anchor="middle"))
    d.add(tx(card_x + 66, 222, "Assistant", size=12.5, weight=600, fill=INK))
    d.add(tx(card_x + 66, 238, "grounded reply", size=10.4, fill=MUTED))

    regions = []

    # answer block
    ry = 262
    d.add(kicker(card_x + 20, ry, "Answer", "#2557D6"))
    for i, w in enumerate((card_w - 44, card_w - 44, card_w - 130)):
        d.add(rect(card_x + 20, ry + 12 + i * 15, w, 7, fill="#DCE5F8", stroke="none", sw=0))
    regions.append((ry - 8, ry + 60))

    # original passage
    ry = 356
    d.add(kicker(card_x + 20, ry, "Original passage", "#0B7A5E"))
    d.add(rect(card_x + 20, ry + 10, card_w - 40, 66, fill="#EFFBF5", stroke="#D3EFE3", sw=1.2))
    d.add('<rect x="%s" y="%s" width="4" height="66" fill="#0E8F6E"/>'
          % (card_x + card_w - 24, ry + 10))
    for i, w in enumerate((card_w - 80, card_w - 120)):
        d.add(rect(card_x + 36, ry + 26 + i * 18, w, 7, fill="#C6E8DA", stroke="none", sw=0))
    regions.append((ry - 8, ry + 82))

    # source
    ry = 462
    d.add(kicker(card_x + 20, ry, "Verified source", "#5A2FB4"))
    d.add(rect(card_x + 20, ry + 10, card_w - 40, 58, fill="#F6F3FE", stroke="#DDD5F4", sw=1.2))
    d.add(tx(card_x + 36, ry + 32, "source.name", size=11.5, weight=600, fill=INK, family=MONO))
    d.add(tx(card_x + 36, ry + 52, "source.reference", size=11, fill="#6B5AA8", family=MONO))
    regions.append((ry - 8, ry + 74))

    # note
    ry = 560
    d.add(kicker(card_x + 20, ry, "System note", "#7C8CA3"))
    d.add(rect(card_x + 20, ry + 10, card_w - 40, 46, fill="#F7F9FC", stroke="#D7DEE9",
               sw=1.2, dash="4 3"))
    for i, w in enumerate((card_w - 80, card_w - 150)):
        d.add(rect(card_x + 36, ry + 22 + i * 15, w, 6, fill="#E3E9F1", stroke="none", sw=0))
    regions.append((ry - 8, ry + 62))

    d.add(tx(card_x + 20, 664, "Layout is right-to-left in the running app; mirrored here for the key.",
             size=10.2, fill=FAINT))

    # ---- mapping arrows ---------------------------------------------------
    for i, (n, (r0, r1)) in enumerate(zip(rows, regions)):
        target_y = (r0 + r1) / 2.0
        lane = 620 + i * 52
        d.add(path([(550, n.cy), (lane, n.cy), (lane, target_y), (card_x - 2, target_y)],
                   stroke="#93A2B7", marker="soft", sw=1.5))

    body, ch = callout(
        60, 738, 1400, "Failing loudly", [
            "If the payload is missing a field or is not valid JSON the client raises a typed error instead of showing a "
            "half-formed answer - a broken contract is a bug, not a message.",
        ], style=NOTE)
    d.add(body)
    d.save(out("04-answer-contract.svg"))


# ==========================================================================
# 05 - Request sequence
# ==========================================================================


def request_sequence():
    W, H = 1520, 900
    d = Diagram(
        W, H,
        "Request sequence - web client",
        "A single question, from keystroke to rendered card, including the failure path.",
    )

    lanes = [
        ("User", "Arabic question", CLIENT),
        ("ChatInput", "components/", CLIENT),
        ("App state", "App.tsx", CLIENT),
        ("geminiService", "services/", SERVICE),
        ("Gemini API", "2.5 Flash", MODEL),
        ("Message card", "components/", CLIENT),
    ]
    cols = columns(60, 1460, len(lanes), 40)
    top, bottom = 150, 782
    centers = []
    for (x, w), (name, sub, style) in zip(cols, lanes):
        cx = x + w / 2.0
        centers.append(cx)
        d.add(rect(x, top, w, 58, fill=style.fill, stroke=style.line, sw=1.4, shadow=True))
        d.add('<rect x="%.1f" y="%.1f" width="%.1f" height="3" fill="%s"/>' % (x, top, w, style.spine))
        d.add(tx(cx, top + 26, name, size=13, weight=600, fill=style.title, anchor="middle"))
        d.add(tx(cx, top + 43, sub, size=10.4, fill=style.detail, anchor="middle"))
        d.add(line(cx, top + 58, cx, bottom, stroke="#CBD5E1", sw=1.2, dash="3 5"))

    # activation bars
    for idx, (y0, y1) in ((2, (300, 720)), (3, (360, 660)), (4, (420, 560))):
        d.add(rect(centers[idx] - 6, y0, 12, y1 - y0, fill="#E9EEF6", stroke="#B7C2D2", sw=1.1))

    msgs = [
        (0, 1, 250, "types a question, presses Enter", "head", None),
        (1, 2, 300, "onSendMessage(text)", "head", None),
        (2, 2, 336, "append user message, isLoading = true", "self", None),
        (2, 3, 380, "getIslamicBotResponse(query)", "head", None),
        (3, 4, 428, "generateContent(prompt, responseSchema)", "head", None),
        (4, 3, 500, "JSON payload", "head", "6 4"),
        (3, 3, 540, "validate against the contract", "self", None),
        (3, 2, 596, "typed GeminiResponse", "head", "6 4"),
        (2, 5, 656, "assistant message with source and note", "head", None),
        (5, 5, 700, "render answer, passage, source, note", "self", None),
    ]
    for i, (src, dst, y, label, kind, dash) in enumerate(msgs):
        if kind == "self":
            cx = centers[src]
            flip = cx + 56 + text_width(label, 10.8) > W - 56
            side = -1 if flip else 1
            d.add(path([(cx, y - 12), (cx + side * 46, y - 12), (cx + side * 46, y + 10),
                        (cx + side * 6, y + 10)], stroke="#8FA0B6", sw=1.5, marker="soft"))
            d.add(tx(cx + side * 56, y + 2, label, size=10.8, fill=MUTED,
                     anchor="end" if flip else "start"))
        else:
            x1, x2 = centers[src], centers[dst]
            sign = 1 if x2 > x1 else -1
            d.add(path([(x1 + sign * 7, y), (x2 - sign * 7, y)],
                       stroke="#57647A" if not dash else "#8FA0B6", sw=1.6, dash=dash))
            d.add(plate((x1 + x2) / 2.0, y - 14, label))

    # failure path
    d.add(path([(centers[4], 736), (centers[3], 736)], stroke="#C0392B", sw=1.6, dash="6 4",
               marker="soft"))
    d.add(plate((centers[3] + centers[4]) / 2.0, 722, "network or schema failure",
                fill="#B03225"))
    d.add(path([(centers[3], 762), (centers[2], 762)], stroke="#C0392B", sw=1.6, dash="6 4",
               marker="soft"))
    d.add(plate((centers[2] + centers[3]) / 2.0, 748, "typed error, banner shown",
                fill="#B03225"))

    d.save(out("05-request-sequence.svg"))


# ==========================================================================
# 06 - Frontend composition
# ==========================================================================


def frontend_composition():
    W, H = 1520, 800
    d = Diagram(
        W, H,
        "Frontend composition and state",
        "Where state lives in the React client, and which module owns each responsibility.",
    )

    d.add(frame(60, 150, 880, 560, "src/ - component tree"))

    app = Node(96, 200, 808, 118, SERVICE, "App.tsx",
               ["Owns the only mutable state: messages, isLoading, error",
                "handleSendMessage orchestrates the turn and maps failures to a banner"],
               tag="container")
    d.add(app.svg())

    kids = columns(96, 904, 3, 28)
    specs = [
        (CLIENT, "Header.tsx", ["Brand, subtitle, build tag"], "presentational"),
        (CLIENT, "MessageList", ["Maps messages to cards,", "keeps the view pinned to the end"], "presentational"),
        (CLIENT, "ChatInput.tsx", ["Local draft state, Enter to send,", "Shift+Enter for a new line"], "controlled"),
    ]
    for (x, w), (style, title, detail, tag) in zip(kids, specs):
        n = Node(x, 384, w, 126, style, title, detail, tag=tag)
        d.add(n.svg())
        d.add(path([(n.cx, 318), (n.cx, 352), (n.cx, 384)], stroke="#93A2B7", marker="soft"))
    d.add(line(kids[0][0] + kids[0][1] / 2, 352, kids[2][0] + kids[2][1] / 2, 352,
               stroke="#CBD5E1", sw=1.2))

    leafs = [
        (CLIENT, "Message.tsx", "One card: answer, passage, source, note"),
        (NOTE, "IconComponents.tsx", "Inline SVG icon set, no icon dependency"),
    ]
    lc = columns(96, 904, 2, 28)
    for (x, w), (style, title, detail) in zip(lc, leafs):
        n = Node(x, 566, w, 104, style, title, [detail], tag="leaf")
        d.add(n.svg())
    d.add(path([(kids[1][0] + kids[1][1] / 2, 510), (kids[1][0] + kids[1][1] / 2, 540),
                (lc[0][0] + lc[0][1] / 2, 540), (lc[0][0] + lc[0][1] / 2, 566)],
               stroke="#93A2B7", marker="soft"))

    # right: contracts and boundaries
    d.add(frame(980, 150, 480, 560, "Module boundaries"))
    b1 = Node(1010, 200, 420, 118, STORE, "types.ts",
              ["The shared vocabulary: ChatMessage, Source,",
               "GeminiResponse, MessageRole"], tag="contract")
    b2 = Node(1010, 348, 420, 140, SERVICE, "services/geminiService.ts",
              ["The only module that knows a provider exists.",
               "Swap it for a real retrieval backend without",
               "touching a single component."], tag="boundary")
    b3 = Node(1010, 518, 420, 152, MODEL, "Environment",
              ["GEMINI_API_KEY is injected at build time by",
               "Vite. A browser bundle cannot keep a secret -",
               "put the key behind a server before shipping."],
              tag="configuration")
    d.add(b1.svg(), b2.svg(), b3.svg())
    d.add(connect(app.right, (1010, 259), "types", axis="h", mid=962, marker="soft",
                  stroke="#93A2B7"))
    d.add(connect((904, 300), (1010, 418), "calls", axis="h", mid=962, marker="soft",
                  stroke="#93A2B7"))
    d.add(connect(b2.bottom, b3.top, marker="soft", stroke="#93A2B7"))

    d.legend([LEGEND[0], LEGEND[1], LEGEND[3], LEGEND[4]], 60, 736, gap=200)
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
