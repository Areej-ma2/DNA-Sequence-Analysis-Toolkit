import os
import pandas as pd


def create_output_folder(folder="output"):
    """
    Create output folder if it does not exist.
    """

    os.makedirs(folder, exist_ok=True)


def save_results(result, file_name="output/analysis_report.csv"):
    """
    Save analysis results into a CSV file.
    """

    rows = []

    rows.append({
        "Metric": "Sequence Length",
        "Value": result["Length"]
    })

    rows.append({
        "Metric": "GC Content",
        "Value": result["GC_Content"]
    })

    counts = result["Counts"]

    for nucleotide in ["A", "T", "G", "C"]:

        rows.append({

            "Metric": nucleotide,

            "Value": counts.get(nucleotide, 0)

        })

    dataframe = pd.DataFrame(rows)

    dataframe.to_csv(file_name, index=False)

    return dataframe