---
title: Email Triage OpenEnv
emoji: 📧
colorFrom: blue
colorTo: purple
sdk: docker
app_file: inference.py
pinned: false
---
# Email Triage OpenEnv
## Description
This environment simulates real-world email triage tasks including spam detection, priority handling, and intelligent response generation.
It uses a realistic dataset with phishing emails, work communication, and personal messages.

## Tasks
### Task 1: Spam Detection (Easy)
- Goal: Identify spam emails
- Expected action: mark_spam

### Task 2: Priority Handling (Medium)
- Goal: Detect urgent emails
- Expected action: mark_important

###  Task 3: Escalation Handling (Hard)
- Goal: Handle legal/critical emails
- Expected action: escalate

## Action Space
- mark_spam
- mark_important
- reply
- ignore
- escalate

## Observation Space
- email_id
- subject
- body
- sender
- priority
- attachments
- thread_id
- history

## OpenEnv API Compliance
The environment follows the OpenEnv standard API:
- `reset()` → Initializes a new episode and returns the first observation
- `step(action)` → Executes an action and returns (observation, reward, done, info)
- `state()` → Returns the internal state of the environment
All data models (Observation, Action, Reward) are implemented using typed Pydantic schemas.

## Reward
- Positive reward for correct action
- Bonus for detecting spam/phishing
- Bonus for handling high-priority emails
- Penalty for wrong actions or ignoring urgent emails
- Reply quality evaluation

## Grading Logic
The environment uses a deterministic grading system:
- Correct action → +0.6
- Incorrect action → penalty
- Spam detection → bonus reward
- High-priority handling → bonus reward
- Ignoring urgent emails → penalty
- Reply quality → evaluated based on tone keywords (e.g., "sorry", "thanks")
Final reward is normalized between 0.0 and 1.0.

## Episode Design
- Each episode corresponds to processing one email
- Maximum steps per episode: 5
- Episode terminates when:
  - Correct action is taken
  - Maximum steps are reached

## Environment Variables
- API_BASE_URL: LLM API endpoint
- HF_TOKEN: Hugging Face API key
- MODEL_NAME: Model used for inference

## Setup (Optional for local development)
### Install dependencies
```bash
pip install -r requirements.txt
```

## Run
### Build Docker Image
```bash
docker build -t email_env .
```
### Run Container
```bash
docker run -e API_BASE_URL="https://router.huggingface.co/v1" \
           -e HF_TOKEN="your_token" \
           -e MODEL_NAME="meta-llama/Meta-Llama-3-8B-Instruct" \
           email_env
```

### Run Without API (Fallback Mode)
If API keys are not provided, the environment will run using rule-based fallback logic.
```bash
docker run email_env
```