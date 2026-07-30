import os

import matplotlib.pyplot as plt


os.makedirs("output", exist_ok=True)

def plot_nucleotide_count(counts, save_path="output/nucleotide_count.png"):
    """
    Plot nucleotide frequency.
    """

    nucleotides = ["A", "T", "G", "C"]

    values = [counts.get(base, 0) for base in nucleotides]

    plt.figure(figsize=(6, 4))

    plt.bar(nucleotides, values)

    plt.title("Nucleotide Frequency")

    plt.xlabel("Nucleotide")

    plt.ylabel("Count")

    plt.tight_layout()

    plt.savefig(save_path)

    plt.close()


def plot_kmers(kmers, save_path="output/kmer_frequency.png"):
    """
    Plot Top K-mers.
    """

    labels = [item[0] for item in kmers]

    values = [item[1] for item in kmers]

    plt.figure(figsize=(8, 5))

    plt.bar(labels, values)

    plt.title("Top 10 K-mers")

    plt.xlabel("K-mer")

    plt.ylabel("Frequency")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(save_path)

    plt.close()