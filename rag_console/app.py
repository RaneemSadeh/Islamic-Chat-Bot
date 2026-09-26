"""
Siraj RAG console - retrieval-augmented question answering over your own PDFs.

    streamlit run rag_console/app.py

Unlike the web client in `src/`, nothing here is simulated: the answer is built
from passages actually retrieved out of a FAISS index, and the passages that were
used are shown next to the answer so a claim can be checked against its source.

Pipeline, end to end, is drawn in:
  docs/diagrams/02-indexing-pipeline.svg
  docs/diagrams/03-query-flow.svg
"""

from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass
from typing import Iterable, Sequence

import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_nomic import NomicEmbeddings

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

AVAILABLE_MODELS = (
    "gemma2-9b-it",
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile",
    "llama3-8b-8192",
)

EMBEDDING_MODEL = "nomic-embed-text-v1.5"
TOP_K = 3

GROUNDED_PROMPT = """أنت "سراج"، مساعد معرفي إسلامي. أجب بالعربية الفصحى المبسّطة معتمداً \
على المقاطع المرفقة وحدها.

المقاطع المسترجَعة:
{context}

سياق المحادثة:
{chat_history}

السؤال: {user_question}

التعليمات:
- استند إلى المقاطع أعلاه فقط، ولا تُضف معلومة من خارجها.
- إن لم تكفِ المقاطع للإجابة فقل ذلك صراحةً واطلب مصدراً إضافياً.
- انقل الشاهد من النص كما ورد، ثم اشرحه بلغة واضحة.
- إن كانت المسألة خلافية أو تحتاج فتوى، نبّه المستخدم إلى مراجعة أهل العلم.

الإجابة:"""

UNGROUNDED_PROMPT = """أنت مساعد عربي متعاون. لا توجد مصادر مرفقة في هذه الجلسة، \
لذا نبّه المستخدم إلى أن إجابتك عامة وغير مستندة إلى مرجع محدّد.

سياق المحادثة:
{chat_history}

السؤال: {user_question}

الإجابة:"""


@dataclass(frozen=True)
class ChunkSettings:
    size: int
    overlap: int


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------


def initialise_state() -> None:
    defaults = {
        "database": None,
        "chat_history": [],
        "backup_history": [],
        "indexed_file": None,
        "chunk_count": 0,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


# ---------------------------------------------------------------------------
# Indexing
# ---------------------------------------------------------------------------


def load_pdf(uploaded) -> list[Document]:
    """Write the upload somewhere PyPDFLoader can open, then read it back."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as handle:
        handle.write(uploaded.getvalue())
        temp_path = handle.name
    try:
        return PyPDFLoader(temp_path).load()
    finally:
        os.unlink(temp_path)


def build_index(docs: Sequence[Document], settings: ChunkSettings) -> tuple[FAISS | None, int]:
    """Split, embed and index. Returns the store and the number of chunks."""
    if not docs:
        st.sidebar.error("لم يتم تحميل أي مستند بعد.")
        return None, 0
    if settings.size <= 0 or settings.overlap >= settings.size:
        st.sidebar.error("حجم المقطع يجب أن يكون أكبر من التداخل.")
        return None, 0

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.size,
        chunk_overlap=settings.overlap,
    )
    chunks = splitter.split_documents(list(docs))
    if not chunks:
        st.sidebar.error("لم ينتج عن التقسيم أي مقطع نصّي - هل الملف ممسوح ضوئياً بلا طبقة نص؟")
        return None, 0

    embeddings = NomicEmbeddings(model=EMBEDDING_MODEL)
    return FAISS.from_documents(chunks, embedding=embeddings), len(chunks)


# ---------------------------------------------------------------------------
# Retrieval and generation
# ---------------------------------------------------------------------------


def format_context(docs: Iterable[Document]) -> str:
    """One numbered block per passage, so the model can refer to them by number."""
    blocks = []
    for index, doc in enumerate(docs, start=1):
        page = doc.metadata.get("page")
        label = f"[{index}] صفحة {page + 1}" if isinstance(page, int) else f"[{index}]"
        blocks.append(f"{label}\n{doc.page_content.strip()}")
    return "\n\n".join(blocks)


def format_history(history: Sequence[object], limit: int = 6) -> str:
    recent = history[-limit:]
    lines = []
    for message in recent:
        speaker = "المستخدم" if isinstance(message, HumanMessage) else "سراج"
        lines.append(f"{speaker}: {getattr(message, 'content', '')}")
    return "\n".join(lines) if lines else "(بداية المحادثة)"


def answer(question: str, llm, database: FAISS | None):
    """Stream an answer, and hand back the passages it was built from."""
    history = format_history(st.session_state.chat_history)

    if database is not None:
        retrieved = database.similarity_search(question, k=TOP_K)
        chain = ChatPromptTemplate.from_template(GROUNDED_PROMPT) | llm | StrOutputParser()
        stream = chain.stream(
            {
                "context": format_context(retrieved),
                "chat_history": history,
                "user_question": question,
            }
        )
        return stream, retrieved

    chain = ChatPromptTemplate.from_template(UNGROUNDED_PROMPT) | llm | StrOutputParser()
    stream = chain.stream({"chat_history": history, "user_question": question})
    return stream, []


def render_sources(documents: Sequence[Document]) -> None:
    if not documents:
        return
    with st.expander(f"المصادر المستخدمة ({len(documents)})"):
        for index, doc in enumerate(documents, start=1):
            page = doc.metadata.get("page")
            where = f"صفحة {page + 1}" if isinstance(page, int) else "موضع غير محدّد"
            st.markdown(f"**[{index}] {where}**")
            st.caption(doc.page_content.strip()[:600])


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------


def sidebar() -> tuple[str, bool, list[Document] | None, ChunkSettings]:
    st.sidebar.title("الإعدادات")

    model = st.sidebar.selectbox("نموذج التوليد", AVAILABLE_MODELS)

    st.sidebar.subheader("المفاتيح")
    groq_key = st.sidebar.text_input("GROQ API key", type="password")
    nomic_key = st.sidebar.text_input("Nomic API key", type="password")
    if groq_key:
        os.environ["GROQ_API_KEY"] = groq_key
    if nomic_key:
        os.environ["NOMIC_API_KEY"] = nomic_key

    st.sidebar.divider()
    st.sidebar.subheader("المستند")
    uploaded = st.sidebar.file_uploader("ارفع ملف PDF", type="pdf")

    docs: list[Document] | None = None
    if uploaded is not None:
        try:
            docs = load_pdf(uploaded)
            st.sidebar.success(f"تم تحميل {uploaded.name} - {len(docs)} صفحة.")
        except Exception as exc:  # noqa: BLE001 - surfaced to the user verbatim
            st.sidebar.error(f"تعذّرت قراءة الملف: {exc}")

    st.sidebar.divider()
    st.sidebar.subheader("التقطيع")
    settings = ChunkSettings(
        size=st.sidebar.slider("حجم المقطع", 100, 1000, 500, 50),
        overlap=st.sidebar.slider("التداخل", 0, 200, 50, 10),
    )

    return model, bool(groq_key), docs, settings


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------


def main() -> None:
    st.set_page_config(page_title="سراج · RAG console", page_icon="📖", layout="wide")
    initialise_state()

    st.title("سراج · وحدة الاسترجاع")
    st.caption("ارفع مصدراً، ابنِ الفهرس، ثم اسأل - وكل إجابة تُعرض بجانب المقاطع التي بُنيت عليها.")

    model, has_groq_key, docs, settings = sidebar()

    st.sidebar.divider()
    st.sidebar.subheader("الفهرس")
    if st.sidebar.button("بناء الفهرس", type="primary", use_container_width=True):
        if not os.environ.get("NOMIC_API_KEY"):
            st.sidebar.error("أدخل مفتاح Nomic أولاً.")
        else:
            with st.spinner("جارٍ بناء الفهرس…"):
                database, count = build_index(docs or [], settings)
            if database is not None:
                st.session_state.database = database
                st.session_state.chunk_count = count
                st.sidebar.success(f"تم بناء الفهرس من {count} مقطعاً.")

    if st.session_state.database is not None:
        st.sidebar.info(f"وضع الاسترجاع مفعّل · {st.session_state.chunk_count} مقطعاً")
    else:
        st.sidebar.warning("لا يوجد فهرس - الإجابات ستكون عامة وبلا مصدر.")

    st.sidebar.divider()
    left, right = st.sidebar.columns(2)
    if left.button("مسح", use_container_width=True):
        st.session_state.backup_history = list(st.session_state.chat_history)
        st.session_state.chat_history = []
        st.rerun()
    if right.button("تراجع", use_container_width=True):
        if st.session_state.backup_history:
            st.session_state.chat_history = list(st.session_state.backup_history)
            st.rerun()

    if not has_groq_key:
        st.warning("أدخل مفتاح GROQ في الشريط الجانبي لبدء المحادثة.")
        st.stop()

    llm = ChatGroq(model=model)

    for message in st.session_state.chat_history:
        role = "user" if isinstance(message, HumanMessage) else "assistant"
        with st.chat_message(role):
            st.markdown(message.content)

    question = st.chat_input("اكتب سؤالك هنا…")
    if not question:
        return

    st.session_state.chat_history.append(HumanMessage(question))
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        try:
            stream, used = answer(question, llm, st.session_state.database)
            reply = st.write_stream(stream)
            render_sources(used)
        except Exception as exc:  # noqa: BLE001 - keep the session alive
            reply = f"تعذّر توليد الإجابة: {exc}"
            st.error(reply)

    st.session_state.chat_history.append(AIMessage(reply))


if __name__ == "__main__":
    main()
