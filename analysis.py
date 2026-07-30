from Bio import SeqIO
from collections import Counter

VALID_BASES = set("ATGCN")


def load_record(file_path):
    """
    Read the full FASTA record (id, description, sequence).
    """

    return SeqIO.read(file_path, "fasta")


def load_sequence(file_path):
    """
    Read DNA sequence from FASTA file.
    """

    record = SeqIO.read(file_path, "fasta")

    return str(record.seq).upper()


def validate_sequence(sequence):
    """
    Return the set of characters in the sequence that are not
    standard/ambiguous DNA bases (A, T, G, C, N).
    """

    return sorted(set(sequence.upper()) - VALID_BASES)


def sequence_length(sequence):

    return len(sequence)


def nucleotide_count(sequence):

    return Counter(sequence)


def gc_content(sequence):

    g = sequence.count("G")
    c = sequence.count("C")

    gc = ((g + c) / len(sequence)) * 100

    return round(gc, 2)


def kmer_frequency(sequence, k=3):

    kmers = []

    for i in range(len(sequence) - k + 1):

        kmers.append(sequence[i:i + k])

    counter = Counter(kmers)

    return counter.most_common(10)


def analyze_sequence(file_path):

    record = load_record(file_path)
    sequence = str(record.seq).upper()

    result = {

        "ID": record.id,

        "Description": record.description,

        "Sequence": sequence,

        "Length": sequence_length(sequence),

        "GC_Content": gc_content(sequence),

        "Counts": nucleotide_count(sequence),

        "Top_Kmers": kmer_frequency(sequence),

        "Invalid_Bases": validate_sequence(sequence),

    }

    return result