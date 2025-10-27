"""Simple smoke test for nlp_pipeline demo."""
from nlp_pipeline import summarize_to_structured_report, sentiment_and_intent, generate_soap
import json

SAMPLE_TRANSCRIPT = '''
Physician: Good morning, Ms. Jones. How are you feeling today?
Patient: Good morning, doctor. I'm doing better, but I still have some discomfort now and then.
Physician: I understand you were in a car accident last September. Can you walk me through what happened?
Patient: Yes, it was on September 1st, around 12:30 in the afternoon. I was driving from Cheadle Hulme to Manchester when I had to stop in traffic. Out of nowhere, another car hit me from behind, which pushed my car into the one in front.
Physician: That sounds like a strong impact. Were you wearing your seatbelt?
Patient: Yes, I always do.
Physician: What did you feel immediately after the accident?
Patient: At first, I was just shocked. But then I realized I had hit my head on the steering wheel, and I could feel pain in my neck and back almost right away.
Physician: Did you seek medical attention at that time?
Patient: Yes, I went to Moss Bank Accident and Emergency. They checked me over and said it was a whiplash injury, but they didn’t do any X-rays. They just gave me some advice and sent me home.
Physician: How did things progress after that?
Patient: The first four weeks were rough. My neck and back pain were really bad—I had trouble sleeping and had to take painkillers regularly. It started improving after that, but I had to go through ten sessions of physiotherapy to help with the stiffness and discomfort.
Physician: Are you still experiencing pain now?
Patient: It’s not constant, but I do get occasional backaches. It’s nothing like before, though.
Physician: Have you noticed any other effects, like anxiety while driving or difficulty concentrating?
Patient: No, nothing like that. I don’t feel nervous driving, and I haven’t had any emotional issues from the accident.
Physician: And how has this impacted your daily life? Work, hobbies, anything like that?
Patient: I had to take a week off work, but after that, I was back to my usual routine. It hasn’t really stopped me from doing anything.
Physician: Everything looks good. Your neck and back have a full range of movement, and there’s no tenderness or signs of lasting damage. Your muscles and spine seem to be in good condition.
Patient: That’s a relief!
Physician: Given your progress, I’d expect you to make a full recovery within six months of the accident.
Patient: Thank you, doctor. I appreciate it.
'''


def run_demo():
    summary = summarize_to_structured_report(SAMPLE_TRANSCRIPT, patient_name="Janet Jones")
    print("Structured Summary:")
    print(json.dumps(summary, indent=2))

    senti = sentiment_and_intent("I'm doing better, but I still have some discomfort now and then.")
    print("\nSentiment/Intent:")
    print(json.dumps(senti, indent=2))

    soap = generate_soap(SAMPLE_TRANSCRIPT, exam_text="Neck and back: full ROM, no tenderness.")
    print("\nSOAP Note:")
    print(json.dumps(soap, indent=2))


if __name__ == "__main__":
    run_demo()
