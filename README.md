# 🧬 DNA Sequence Analysis Toolkit

An interactive bioinformatics application built with **Python** and **Streamlit** for analyzing DNA sequences from FASTA files. The toolkit provides essential sequence analysis features through an easy-to-use web interface, making biological sequence exploration more accessible.

---

## ✨ Features

- 📂 Upload DNA sequences in FASTA format
- 📏 Calculate sequence length
- 🧪 Calculate GC content
- 🔬 Count nucleotide frequencies (A, T, G, C)
- 🧩 Identify the most frequent k-mers
- 🔍 Search for DNA motifs
- 🧬 Compare two DNA sequences
- 📊 Visualize analysis results with charts
- 📄 Export analysis reports as CSV files

---

## 🛠️ Technologies Used

- Python
- Streamlit
- Biopython
- Pandas
- Matplotlib

---

## 📂 Project Structure

```text
DNA-Sequence-Analysis-Toolkit/
│
├── app.py
├── analysis.py
├── compare.py
├── motif.py
├── visualization.py
├── utils.py
├── requirements.txt
├── README.md
├── output/
└── sample.fasta
```

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/Areej-ma2/DNA-Sequence-Analysis-Toolkit.git
```

Move into the project folder:

```bash
cd DNA-Sequence-Analysis-Toolkit
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

---

## 📖 How to Use

1. Launch the Streamlit application.
2. Upload a FASTA file containing a DNA sequence.
3. View the sequence statistics and visualizations.
4. Search for DNA motifs.
5. Optionally upload a second FASTA file to compare two DNA sequences.
6. Download the generated analysis report.

---

## 📊 Output

The application provides:

- Sequence Length
- GC Content
- Nucleotide Composition
- Top Frequent k-mers
- DNA Motif Positions
- Sequence Similarity
- Mutation Details
- Charts
- CSV Analysis Report

---

## 🎯 Project Purpose

This project was developed as a practical bioinformatics application to demonstrate DNA sequence analysis using Python. It combines biological sequence processing, data visualization, and an interactive web interface to provide an accessible analysis workflow.

---

## 🔮 Future Improvements

- Support RNA and protein sequence analysis
- Interactive Plotly visualizations
- Multiple sequence alignment
- BLAST integration
- Enhanced statistical analysis
- Downloadable PDF reports

---

## 📜 License

This project is released under the MIT License.

---

## 👩‍💻 Author

**Areej Al-Mohammadi**

Master's Student in Biochemistry | Bioinformatics
