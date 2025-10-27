# Submission Cover Note

Candidate: Tuba Ahmed Khan

SAP ID: 500105642

Assignment: Physician Notetaker (AI Engineer Intern assessment)

Date (submission): 29-Oct-2025

Repository: https://github.com/tubakhxn/physician-notetaker-500105642

Resume: [My Resume](https://drive.google.com/file/d/1nVaAYmXvelvwpVphtiBZyAfyViXwCNKb/view?usp=sharing)

What this repo includes

- `nlp_pipeline.py` — core pipeline: heuristic NER, summarization, keyword extraction, sentiment & intent classification, and SOAP note generator.
- `test_nlp_pipeline.py` — demo smoke test that prints structured summary, sentiment/intent, and SOAP note for the provided transcript.
- `demo_notebook.ipynb` — demo notebook that runs the pipeline on the sample conversation.
- `requirements.txt` — Python dependencies.
- `README.md` — setup and run instructions.

Instructions for reviewers

1. Create & activate a virtual environment (PowerShell):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

3. Run the smoke test:

```powershell
python test_nlp_pipeline.py
```

Notes & caveats

- This is a demo/hybrid (rule + spaCy + transformers pipelines) implementation intended for evaluation purposes only. It is not validated for clinical use.
- If internet is unavailable in the environment, the sentiment pipeline (transformers) may fail to download a model; the code handles this and falls back to a neutral label.

Checklist to submit

- [ ] Push this repo to GitHub and replace the `Repository` field above with the repo URL.
- [ ] Paste your resume link in the `Resume` field.
- [ ] Reply to the assignment email with the repo link and resume link before the deadline (29-Oct-2025).

Contact

If you need any clarifications on the repo or instructions, contact: Tuba Ahmed Khan (SAP ID: 500105642)

Screenshot placeholder removed — textual excerpt included

I removed the screenshot placeholder from the repo per the candidate's request. Below is the actual run output captured from the demo run on this machine (placed in `run_output.txt`). Reviewers can reproduce by running `python test_nlp_pipeline.py` as noted above.

```
python.exe : No model was supplied, defaulted to distilbert/distilbert-base-uncased-finetuned-sst-2-english
Device set to use cpu
Structured Summary:
{
	"Patient_Name": "Janet Jones",
	"Symptoms": [
		"Back",
		"Back Pain",
		"Backache",
		"Head",
		"Neck",
		"Pain",
		"Stiffness"
	],
	"Diagnosis": "Whiplash injury",
	"Treatment": [
		"Painkillers"
	],
	"Current_Status": "now and then",
	"Prognosis": "Full recovery expected within six months of the accident",
	"Keywords": [
		"Physician",
		"Patient",
		"accident",
		"Good morning",
		"Good",
		"back",
		"n\u2019t",
		"September"
	]
}

Sentiment/Intent:
{
	"Sentiment": "Anxious",
	"Intent": "Other"
}

SOAP Note:
{
	"Subjective": {
		"Chief_Complaint": "Back, Back Pain, Backache, Head, Neck, Pain, Stiffness",
		"History_of_Present_Illness": "Patient involved in a car accident on September 1st (reported). Symptoms reported: Back, Back Pain, Backache, Head, Neck, Pain, Stiffness."
	},
	"Objective": {
		"Physical_Exam": "Neck and back: full ROM, no tenderness.",
		"Observations": "Patient appears in normal health, normal gait."
	},
	"Assessment": {
		"Diagnosis": "Whiplash injury",
		"Severity": "Mild, improving"
	},
	"Plan": {
		"Treatment": [
			"Painkillers"
		],
		"Follow-Up": "Return if symptoms worsen or persist beyond expected recovery period (6 months)."
	}
}
```

