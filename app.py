import os
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
    layout="centered"
)

st.title("🧬 DNA Sequence Analysis Toolkit")

st.write(
    "Upload one or two FASTA files to analyze DNA sequences."
)

create_output_folder()


# ----------------------------
# Upload Files
# ----------------------------

sequence1 = st.file_uploader(
    "Upload Sequence 1",
    type=["fasta", "fa"],
    key="seq1"
)

sequence2 = st.file_uploader(
    "Upload Sequence 2 (Optional)",
    type=["fasta", "fa"],
    key="seq2"
)


# ----------------------------
# Analyze Sequence 1
# ----------------------------

if sequence1 is not None:

    file1_path = os.path.join(
        "output",
        sequence1.name
    )

    with open(file1_path, "wb") as f:

        f.write(sequence1.getbuffer())

    result = analyze_sequence(file1_path)

    st.header("Sequence Analysis")

    st.metric(
        "Sequence Length",
        result["Length"]
    )

    st.metric(
        "GC Content",
        f'{result["GC_Content"]}%'
    )

    st.subheader("Nucleotide Counts")

    st.write(result["Counts"])

    st.subheader("Top 10 K-mers")

    st.table(result["Top_Kmers"])

    plot_nucleotide_count(result["Counts"])

    plot_kmers(result["Top_Kmers"])

    st.image(
        "output/nucleotide_count.png",
        caption="Nucleotide Frequency"
    )

    st.image(
        "output/kmer_frequency.png",
        caption="Top K-mers"
    )

    save_results(result)

    st.success("Analysis Completed")


# ----------------------------
# Motif Search
# ----------------------------

    st.header("Motif Search")

    motif = st.text_input(
        "Enter DNA Motif",
        value="ATG"
    )

    if st.button("Search Motif"):

        sequence = load_sequence(file1_path)

        positions = find_motif(
            sequence,
            motif
        )

        st.write(
            f"Motif found {len(positions)} times."
        )

        st.write(positions)


# ----------------------------
# Sequence Comparison
# ----------------------------

if sequence1 is not None and sequence2 is not None:

    file2_path = os.path.join(
        "output",
        sequence2.name
    )

    with open(file2_path, "wb") as f:

        f.write(sequence2.getbuffer())

    seq1 = load_sequence(file1_path)

    seq2 = load_sequence(file2_path)

    comparison = compare_sequences(
        seq1,
        seq2
    )

    st.header("Sequence Comparison")

    st.metric(
        "Similarity",
        f'{comparison["Similarity"]}%'
    )

    st.metric(
        "Mutations",
        comparison["Total Mutations"]
    )

    st.subheader("Mutation Details")

    st.table(comparison["Mutations"])