def find_motif(sequence, motif):
    """
    Find all occurrences of a DNA motif.
    """

    sequence = sequence.upper()
    motif = motif.upper()

    positions = []

    for i in range(len(sequence) - len(motif) + 1):

        if sequence[i:i + len(motif)] == motif:

            positions.append(i + 1)

    return positions