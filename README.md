# Physician Notetaker - NLP Pipeline

This repository provides a minimal NLP pipeline for medical transcription processing: NER (symptoms/treatment/diagnosis/prognosis), extractive summarization, keyword extraction, sentiment & intent classification, and automated SOAP note generation.

Contents
- `nlp_pipeline.py` - core functions for extraction, summarization, sentiment/intent classification, and SOAP conversion.
- `demo_notebook.ipynb` - Jupyter notebook demonstrating the pipeline on the sample physician-patient conversation.
- `test_nlp_pipeline.py` - a small smoke test script.
- `requirements.txt` - Python dependencies.

Setup (PowerShell / Windows)

1. Create and activate a virtual environment (optional but recommended):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Download spaCy model:

```powershell
python -m spacy download en_core_web_sm
```

Quick demo (run the script):

```powershell
python test_nlp_pipeline.py
```

Notes
- This project uses a hybrid approach (spaCy + rule-based + Hugging Face transformers pipelines) so it runs without large model training. For production-grade clinical use, swap or fine-tune to clinical models (BioClinicalBERT, PubMedBERT, T5/BART fine-tuned on clinical summarization datasets).

Questions & choices
- Ambiguous / missing data: fields are set to `null` or empty lists and accompanied by a `confidence` estimate where possible; the pipeline flags missing critical fields.
- Recommended pre-trained models for medical summarization: `google/pegasus` family, `facebook/bart-large-cnn`, or domain-adapted T5/BART fine-tuned on clinical corpora. For clinical embeddings/classification: `emilyalsentzer/Bio_ClinicalBERT`, `microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract`.

License: MIT (demo code)

Optional: including run output or a screenshot

We recommend including a short textual log from the terminal rather than screenshots (text is searchable, smaller, and doesn't risk embedding extra system metadata). Two safe options:

1) Recommended — include a textual excerpt of the run (copy/paste):

	- Run and save output to a file:

	```powershell
	python "C:\Users\Tuba Khan\Downloads\Assement\test_nlp_pipeline.py" > run_output.txt 2>&1
	```

	- Open `run_output.txt`, copy a brief excerpt (2–6 lines) showing the Structured Summary or SOAP JSON, and paste it into `SUBMISSION.md` or the email reply.


Made with 🩷 by @tubakhxn


