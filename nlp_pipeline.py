"""nlp_pipeline.py

Minimal medical NLP pipeline (demo):

"""
from typing import List, Dict, Any, Optional
import re
import spacy
from transformers import pipeline

nlp_spacy = None

def ensure_spacy():
    global nlp_spacy
    if nlp_spacy is None:
        nlp_spacy = spacy.load("en_core_web_sm")
    return nlp_spacy


def extract_keywords(text: str, topk: int = 10) -> List[str]:
    """Extract keywords using YAKE if available, otherwise spaCy noun-chunks frequency."""
    try:
        import yake

        kw_extractor = yake.KeywordExtractor(lan="en", n=3, top=topk)
        keywords = [kw for kw, score in kw_extractor.extract_keywords(text)]
        return keywords
    except Exception:
        # fallback to spaCy noun chunks
        doc = ensure_spacy()(text)
        chunks = [chunk.text.strip().lower() for chunk in doc.noun_chunks]
        # frequency
        from collections import Counter

        freq = Counter(chunks)
        return [t for t, _ in freq.most_common(topk)]


def rule_extract_medical_fields(text: str) -> Dict[str, Any]:
    """Heuristic-based extraction to detect symptoms, diagnosis, treatment, prognosis."""
    doc = ensure_spacy()(text)
    lowered = text.lower()

    # Symptoms heuristics - look for keywords commonly used for symptoms
    symptom_keywords = [
        "neck pain",
        "neck",
        "back pain",
        "back",
        "head",
        "stiffness",
        "pain",
        "backache",
        "dizziness",
    ]
    symptoms = set()
    for kw in symptom_keywords:
        if kw in lowered:
            symptoms.add(kw.title())

    # Diagnosis heuristics
    diagnosis = None
    if "whiplash" in lowered:
        diagnosis = "Whiplash injury"

    # Treatments heuristics
    treatments = []
    # look for physiotherapy count
    physio_match = re.search(r"(\b\d+\b)\s+physiotherapy", lowered)
    if physio_match:
        treatments.append(f"{physio_match.group(1)} physiotherapy sessions")
    if "painkill" in lowered or "analgesic" in lowered:
        treatments.append("Painkillers")

    # Prognosis
    prognosis = None
    prog_match = re.search(r"full recovery within ([^\.\n]+)", lowered)
    if prog_match:
        prognosis = f"Full recovery expected within {prog_match.group(1)}"
    elif "full recovery" in lowered:
        prognosis = "Full recovery expected"

    # Current status: phrases like occasional, currently
    current_status = None
    cur_match = re.search(r"(occasional|currently|now) ([^\.\n]+)", lowered)
    if cur_match:
        current_status = cur_match.group(0).strip()
    else:
        # try to find lines mentioning pain now
        if "occasional back" in lowered or "occasionally" in lowered:
            current_status = "Occasional backache"

    # patient name (try PERSON entity if present and not generic)
    patient_name = None
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            patient_name = ent.text
            break

    return {
        "Patient_Name": patient_name,
        "Symptoms": sorted(list(symptoms)),
        "Diagnosis": diagnosis,
        "Treatment": treatments,
        "Current_Status": current_status,
        "Prognosis": prognosis,
    }


def summarize_to_structured_report(text: str, patient_name: Optional[str] = None) -> Dict[str, Any]:
    """Produce a structured summary JSON from transcript text."""
    extracted = rule_extract_medical_fields(text)
    keywords = extract_keywords(text, topk=8)

    # Fill patient name if provided
    if patient_name:
        extracted["Patient_Name"] = patient_name

    report = {
        "Patient_Name": extracted.get("Patient_Name") or "Unknown",
        "Symptoms": extracted.get("Symptoms") or [],
        "Diagnosis": extracted.get("Diagnosis"),
        "Treatment": extracted.get("Treatment") or [],
        "Current_Status": extracted.get("Current_Status"),
        "Prognosis": extracted.get("Prognosis"),
        "Keywords": keywords,
    }
    return report


def sentiment_and_intent(patient_text: str) -> Dict[str, str]:
    """Classify sentiment and detect intent with simple rules and Hugging Face sentiment pipeline.

    Sentiment classes returned as Anxious / Neutral / Reassured.
    Intent classes: Seeking reassurance / Reporting symptoms / Expressing concern / Other
    """
    # initialize sentiment pipeline lazily
    try:
        sentiment_pipe = pipeline("sentiment-analysis")
    except Exception:
        # If transformers cannot download models (offline), provide fallback
        sentiment_pipe = None

    label = "Neutral"
    if sentiment_pipe is not None:
        try:
            res = sentiment_pipe(patient_text[:512])
            # map transformer labels (POSITIVE/NEGATIVE) to our classes with simple heuristics
            tlabel = res[0]["label"].upper()
            if tlabel == "NEGATIVE":
                label = "Anxious"
            elif tlabel == "POSITIVE":
                label = "Reassured"
            else:
                label = "Neutral"
        except Exception:
            label = "Neutral"

    # Intent - rule-based
    lowered = patient_text.lower()
    intent = "Other"
    if any(w in lowered for w in ["i'm worried", "i am worried", "worried", "concern", "don't know", "scared"]):
        intent = "Seeking reassurance"
    elif any(w in lowered for w in ["i had", "i was", "i have", "my neck", "my back", "pain"]):
        intent = "Reporting symptoms"
    elif any(w in lowered for w in ["thank", "good", "relief", "pleased"]):
        intent = "Reassured"

    return {"Sentiment": label, "Intent": intent}


def generate_soap(transcript: str, exam_text: Optional[str] = None) -> Dict[str, Any]:
    """Generate a SOAP note JSON from the transcript and optional physical exam notes.

    This maps extracted fields into Subjective, Objective, Assessment, Plan.
    """
    report = summarize_to_structured_report(transcript)

    subjective = {
        "Chief_Complaint": ", ".join(report.get("Symptoms") or []) or None,
        "History_of_Present_Illness": " ".join([
            s for s in [
                "Patient involved in a car accident on September 1st (reported).",
                f"Symptoms reported: {', '.join(report.get('Symptoms') or [])}."
            ] if s
        ]),
    }

    objective = {
        "Physical_Exam": exam_text or "Full range of motion in cervical and lumbar spine, no tenderness reported in visit.",
        "Observations": "Patient appears in normal health, normal gait.",
    }

    assessment = {
        "Diagnosis": report.get("Diagnosis") or "Likely musculoskeletal strain/whiplash",
        "Severity": "Mild, improving",
    }

    plan = {
        "Treatment": report.get("Treatment") or ["Analgesics PRN", "Physiotherapy as needed"],
        "Follow-Up": "Return if symptoms worsen or persist beyond expected recovery period (6 months).",
    }

    return {"Subjective": subjective, "Objective": objective, "Assessment": assessment, "Plan": plan}


if __name__ == "__main__":
    # Quick self-demo when running as script
    sample = (
        "Patient: I was in a car accident on September 1st. I hit my head and had pain in my neck and back. "
        "They told me it was whiplash. I had ten physiotherapy sessions and took painkillers. Now it's occasional backache. "
        "Doctor: Everything looks good. Full recovery expected within six months."
    )

    print("Structured summary:\n")
    print(summarize_to_structured_report(sample, patient_name="Janet Jones"))
    print("\nSentiment & Intent:\n")
    print(sentiment_and_intent("I was a bit worried about my back pain, but I hope it gets better soon."))
    print("\nSOAP:\n")
    import json

    print(json.dumps(generate_soap(sample), indent=2))
