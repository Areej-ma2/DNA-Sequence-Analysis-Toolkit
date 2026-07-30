import os

import matplotlib.pyplot as plt


os.makedirs("output", exist_ok=True)

BASE_COLORS = {
    "A": "#0F9D8C",
    "T": "#2E86AB",
    "G": "#F2A007",
    "C": "#C0392B",
}
KMER_COLOR = "#0F9D8C"

plt.rcParams.update({
    "font.family": "sans-serif",
    "axes.edgecolor": "#B9C7C6",
    "axes.labelcolor": "#122A2A",
    "text.color": "#122A2A",
    "xtick.color": "#3A4D4C",
    "ytick.color": "#3A4D4C",
})


def _style_axes(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", color="#E1E8E7", linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)


def plot_nucleotide_count(counts, save_path="output/nucleotide_count.png"):
    """
    Plot nucleotide frequency.
    """

    nucleotides = ["A", "T", "G", "C"]

    values = [counts.get(base, 0) for base in nucleotides]
    colors = [BASE_COLORS[base] for base in nucleotides]

    fig, ax = plt.subplots(figsize=(6, 4), dpi=150)

    bars = ax.bar(nucleotides, values, color=colors, width=0.6, zorder=3)

    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{value:,}",
            ha="center",
            va="bottom",
            fontsize=9,
            color="#122A2A",
        )

    ax.set_title("Nucleotide Frequency", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Nucleotide")
    ax.set_ylabel("Count")
    _style_axes(ax)

    fig.tight_layout()
    fig.savefig(save_path, facecolor="white")
    plt.close(fig)


def plot_kmers(kmers, save_path="output/kmer_frequency.png"):
    """
    Plot Top K-mers.
    """

    labels = [item[0] for item in kmers]
    values = [item[1] for item in kmers]

    fig, ax = plt.subplots(figsize=(8, 5), dpi=150)

    ax.bar(labels, values, color=KMER_COLOR, width=0.65, zorder=3)

    ax.set_title("Top 10 K-mers", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("K-mer")
    ax.set_ylabel("Frequency")
    ax.tick_params(axis="x", rotation=45)
    _style_axes(ax)

    fig.tight_layout()
    fig.savefig(save_path, facecolor="white")
    plt.close(fig)
