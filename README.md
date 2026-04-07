---
title: Email AI Ananlyser
emoji: 📧
colorForm: blue
colorTo: purple
sdk: docker
app_file: app.py
pinned: false
---

# 📧 Email AI Environment (OpenEnv Compatible)

## 🧠 Description

This project simulates a real-world **Email Assistant Environment** where an AI agent processes incoming emails and performs tasks such as:

- Spam detection
- Email categorization
- Urgency detection
- Automated reply generation

This environment is designed for evaluating intelligent agents in a realistic productivity use case.

## 🎯 Real-World Motivation

Managing emails manually is time-consuming. This environment models a real-world system used in businesses to automate email triage, prioritize urgent messages, and filter spam.


## 📦 Observation Space

The environment provides the following observation:

```json
{
  "text": "Email content"
}

## Action Space

- spam: spam / no
- category: work / personal / promotion / urgent
- urgent: yes / no
- reply: text

## Observation Space

- email text input

## Setup

pip install -r requirements.txt
uvicorn app:app --reload