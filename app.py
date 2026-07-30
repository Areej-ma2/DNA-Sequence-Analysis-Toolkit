import hashlib
import os

import pandas as pd
import streamlit as st

from analysis import analyze_sequence, load_sequence
from motif import find_motif
from compare import compare_sequences
from visualization import plot_nucleotide_count, plot_kmers
from utils import create_output_folder, save_results


# ----------------------------
# Page Configuration
# ----------------------------

st.set_page_config(
    page_title="DNA Sequence Analysis Toolkit",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

create_output_folder()


# ----------------------------
# Styling
# ----------------------------

st.markdown(
    """
    <style>
        .block-container { padding-top: 2rem; max-width: 1100px; }

        .hero {
            background: linear-gradient(135deg, #0F9D8C 0%, #0B6E63 100%);
            padding: 2rem 2.25rem;
            border-radius: 14px;
            color: #FFFFFF;
            margin-bottom: 1.75rem;
        }
        .hero h1 { margin: 0 0 0.35rem 0; font-size: 1.9rem; }
        .hero p { margin: 0; opacity: 0.92; font-size: 1.02rem; }

        .seq-badge {
            display: inline-block;
            background: #EAF6F4;
            color: #0B6E63;
            border-radius: 999px;
            padding: 0.15rem 0.75rem;
            font-size: 0.8rem;
            font-weight: 600;
            margin-right: 0.4rem;
        }

        footer, #MainMenu { visibility: hidden; }
        .app-footer {
            margin-top: 3rem;
            padding-top: 1rem;
            border-top: 1px solid #E1E8E7;
            color: #6B7B7A;
            font-size: 0.85rem;
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ----------------------------
# Header
# ----------------------------

st.markdown(
    """
    <div class="hero">
        <h1>🧬 DNA Sequence Analysis Toolkit</h1>
        <p>Upload FASTA sequences to explore composition, k-mer patterns, motifs,
        and pairwise mutations — with exportable reports and charts.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ----------------------------
# Sidebar — Inputs
# ----------------------------

with st.sidebar:
    st.header("📂 Sequence Input")

    sequence1 = st.file_uploader(
        "Primary sequence (required)",
        type=["fasta", "fa"],
        key="seq1",
    )

    sequence2 = st.file_uploader(
        "Comparison sequence (optional)",
        type=["fasta", "fa"],
        key="seq2",
    )

    st.divider()

    st.header("⚙️ Settings")
    motif_query = st.text_input("DNA motif to search", value="ATG")

    st.divider()

    with st.expander("ℹ️ About this toolkit"):
        st.markdown(
            "Analyze DNA sequences from FASTA files: sequence length, GC "
            "content, nucleotide composition, top k-mers, motif positions, "
            "and similarity/mutations between two sequences.\n\n"
            "Built with **Streamlit**, **Biopython**, **Pandas** and "
            "**Matplotlib** by *Areej Al-Mohammadi*."
        )


def _save_upload(uploaded_file):
    """Persist an uploaded file under a content-hash filename to avoid
    collisions between sessions and to enable stable caching."""

    content = uploaded_file.getbuffer()
    digest = hashlib.md5(content).hexdigest()[:10]
    path = os.path.join("output", f"{digest}_{uploaded_file.name}")

    if not os.path.exists(path):
        with open(path, "wb") as f:
            f.write(content)

    return path


@st.cache_data(show_spinner=False)
def _cached_analysis(file_path):
    return analyze_sequence(file_path)


# ----------------------------
# Empty state
# ----------------------------

if sequence1 is None:
    st.info(
        "👈 Upload a FASTA file in the sidebar to get started. "
        "Add a second file to unlock sequence comparison."
    )

    cols = st.columns(4)
    features = [
        ("📏", "Length & GC%", "Core composition metrics at a glance."),
        ("🧩", "K-mer profiling", "Discover the most frequent k-mers."),
        ("🔍", "Motif search", "Locate every occurrence of a custom motif."),
        ("🧬", "Comparison", "Similarity and per-base mutation report."),
    ]
    for col, (icon, title, desc) in zip(cols, features):
        with col:
            with st.container(border=True):
                st.markdown(f"### {icon} {title}")
                st.caption(desc)

    st.stop()


# ----------------------------
# Load & validate sequence 1
# ----------------------------

file1_path = _save_upload(sequence1)

try:
    result = _cached_analysis(file1_path)
except Exception as exc:
    st.error(f"Could not parse **{sequence1.name}** as FASTA: {exc}")
    st.stop()

if result["Invalid_Bases"]:
    st.warning(
        "Unexpected characters found in the sequence: "
        f"`{', '.join(result['Invalid_Bases'])}`. Results below still "
        "reflect the raw sequence."
    )


# ----------------------------
# Tabs
# ----------------------------

tab_overview, tab_motif, tab_compare = st.tabs(
    ["📊 Overview", "🔍 Motif Search", "🧬 Comparison"]
)


# ----------------------------
# Overview
# ----------------------------

with tab_overview:
    st.markdown(
        f'<span class="seq-badge">{result["ID"]}</span>'
        f'<span class="seq-badge">{result["Length"]:,} bp</span>',
        unsafe_allow_html=True,
    )
    if result["Description"] and result["Description"] != result["ID"]:
        st.caption(result["Description"])

    col1, col2 = st.columns(2)
    col1.metric("Sequence Length", f'{result["Length"]:,} bp')
    col2.metric("GC Content", f'{result["GC_Content"]}%')

    with st.expander("Preview raw sequence"):
        preview = result["Sequence"]
        st.code(
            preview[:500] + ("..." if len(preview) > 500 else ""),
            language=None,
        )

    left, right = st.columns(2)

    with left:
        st.subheader("Nucleotide Counts")
        st.write(dict(result["Counts"]))
        plot_nucleotide_count(result["Counts"])
        st.image("output/nucleotide_count.png", use_container_width=True)

    with right:
        st.subheader("Top 10 K-mers")
        st.table(result["Top_Kmers"])
        plot_kmers(result["Top_Kmers"])
        st.image("output/kmer_frequency.png", use_container_width=True)

    report_df = save_results(result)

    st.download_button(
        "⬇️ Download analysis report (CSV)",
        data=report_df.to_csv(index=False).encode("utf-8"),
        file_name=f"{result['ID']}_analysis_report.csv",
        mime="text/csv",
    )

    st.success("Analysis completed.")


# ----------------------------
# Motif Search
# ----------------------------

with tab_motif:
    st.subheader("Search for a DNA Motif")

    query = st.text_input("Motif", value=motif_query, key="motif_input")

    if st.button("Search Motif", type="primary"):
        if not query.strip():
            st.warning("Enter a motif to search for.")
        else:
            positions = find_motif(result["Sequence"], query)

            if positions:
                st.success(f"Motif **{query.upper()}** found {len(positions)} time(s).")
                st.write(positions)
            else:
                st.info(f"Motif **{query.upper()}** was not found in this sequence.")


# ----------------------------
# Sequence Comparison
# ----------------------------

with tab_compare:
    if sequence2 is None:
        st.info("Upload a second FASTA file in the sidebar to compare sequences.")
    else:
        file2_path = _save_upload(sequence2)

        try:
            seq2 = load_sequence(file2_path)
        except Exception as exc:
            st.error(f"Could not parse **{sequence2.name}** as FASTA: {exc}")
            st.stop()

        comparison = compare_sequences(result["Sequence"], seq2)

        st.subheader("Comparison Summary")

        col1, col2, col3 = st.columns(3)
        col1.metric("Bases Compared", f'{comparison["Length Compared"]:,}')
        col2.metric("Similarity", f'{comparison["Similarity"]}%')
        col3.metric("Mutations", comparison["Total Mutations"])

        st.subheader("Mutation Details")

        if comparison["Mutations"]:
            st.dataframe(comparison["Mutations"], use_container_width=True)

            mutations_csv = pd.DataFrame(comparison["Mutations"]).to_csv(index=False)
            st.download_button(
                "⬇️ Download mutations (CSV)",
                data=mutations_csv.encode("utf-8"),
                file_name="mutations_report.csv",
                mime="text/csv",
            )
        else:
            st.success("No mutations detected in the compared region.")


# ----------------------------
# Footer
# ----------------------------

st.markdown(
    """
    <div class="app-footer">
        🧬 DNA Sequence Analysis Toolkit &middot; built with Streamlit &amp; Biopython
        &middot; by Areej Al-Mohammadi
    </div>
    """,
    unsafe_allow_html=True,
)
