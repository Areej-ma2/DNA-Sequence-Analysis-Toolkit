def compare_sequences(seq1, seq2):
    """
    Compare two DNA sequences and return similarity and mutation positions.
    """

    length = min(len(seq1), len(seq2))

    matches = 0

    mutations = []

    for i in range(length):

        if seq1[i] == seq2[i]:

            matches += 1

        else:

            mutations.append({

                "Position": i + 1,

                "Sequence1": seq1[i],

                "Sequence2": seq2[i]

            })

    similarity = round((matches / length) * 100, 2)

    result = {

        "Length Compared": length,

        "Similarity": similarity,

        "Total Mutations": len(mutations),

        "Mutations": mutations

    }

    return result