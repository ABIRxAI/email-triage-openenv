import os
import time
from openai import OpenAI
from env.email_env import EmailEnv
from env.models import Action

API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("HF_TOKEN")
MODEL_NAME = os.getenv("MODEL_NAME")

if not API_KEY:
    print("No API key found. Running in fallback mode.")

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY) if API_KEY else None

env = EmailEnv()

def decide_action(observation):
    try:
        # Try using API
        prompt = f"""
You are an AI email triage assistant.

Classify the email and choose EXACTLY ONE action:

Rules:
- If email is phishing, fake, lottery, suspicious → mark_spam
- If email is high priority or urgent → mark_important
- If email contains legal/security issue → escalate
- If email is personal/work and requires response → reply
- If email is irrelevant → ignore

Email:
Subject: {observation.subject}
Body: {observation.body}
Sender: {observation.sender}
Priority: {observation.priority}
Attachments: {observation.attachments}

Return ONLY one word:
mark_spam OR mark_important OR reply OR ignore OR escalate
"""

        if client:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
            )
            text = response.choices[0].message.content.lower()
            
        else:
            raise Exception("No API client")

        if "spam" in text:
            return Action(action_type="mark_spam")
        elif "important" in text:
            return Action(action_type="mark_important")
        elif "escalate" in text:
            return Action(action_type="escalate")
        elif "ignore" in text:
            return Action(action_type="ignore")
        else:
            return Action(
                action_type="reply",
                content="Thank you for your email."
            )

    except Exception as e:
        print("Fallback triggered:", e)

        # Fallback logic
        subject = observation.subject.lower()
        body = observation.body.lower()
        sender = observation.sender.lower()

        # SPAM (VERY STRICT)
        spam_senders = ["fake", "spam", "promo", "ads", "fraud", "phishing"]
        spam_keywords = [
            "win", "lottery", "prize", "free", "offer",
            "click", "verify", "kyc", "suspended", "earn"
        ]

        if any(s in sender for s in spam_senders) or \
        any(word in subject or word in body for word in spam_keywords):
            return Action(action_type="mark_spam")


        # URGENT (HIGH PRIORITY)
        if observation.priority == "high":
            return Action(action_type="mark_important")


        # WORK EMAILS
        work_domains = ["company.com"]

        if any(domain in sender for domain in work_domains):
            return Action(
                action_type="reply",
                content="Acknowledged. I will review and get back shortly."
            )


        # PERSONAL EMAILS
        personal_domains = ["gmail.com", "yahoo.com"]

        if any(domain in sender for domain in personal_domains):
            return Action(
                action_type="reply",
                content="Thanks for your message! Will get back to you soon."
            )


        # ATTACHMENT → usually work → reply
        if observation.attachments:
            return Action(
                action_type="reply",
                content="Received the attachment. Will review it shortly."
            )


        # DEFAULT
        return Action(
            action_type="reply",
            content="Thank you for your email."
        )


def run():
    total_score = 0
    total_steps = 0

    EPISODES = 5  
    for _ in range(EPISODES):
        obs = env.reset()
        done = False

        while not done:
            action = decide_action(obs)

            obs, reward, done, _ = env.step(action)

            total_score += reward.value
            total_steps += 1

            print(f"Action: {action.action_type}")
            print(f"Reward: {reward.value} | Reason: {reward.reason}")
            print("-" * 40)

    print("\nFinal Score:", total_score / EPISODES)
    print("Total Steps:", total_steps)

if __name__ == "__main__":
    run()

    # Keep container alive for Hugging Face Spaces 
    print("Execution complete. Keeping container alive...") 
    while True: 
        time.sleep(60)