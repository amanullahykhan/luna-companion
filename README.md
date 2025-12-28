# 🌙 Luna Companion — Secure Starter Kit

A free, open-source AI companion that runs on Hugging Face Spaces + Supabase Free Tier — no credit card required.

## ✅ Features

- 🧠 Emotional, expressive chat (Mistral-7B GGUF, CPU-friendly)
- 👁️ Image understanding (moondream2, CPU)
- 😊 Emotion detection (local, no API)
- 📊 Chat history stored in Supabase (analysis-ready)
- 🔐 RLS-secured — users see only their own data
- 💡 Built for data analysis (weekly trends, emotion stats)

## 🚀 Quick Setup

### 1. Create Supabase Project (Free, No Card)

1. Go to [supabase.com](https://supabase.com) → GitHub login
2. New Project → Region: **🇺🇸 Free (US East)** → **Skip billing**
3. Run `supabase/schema.sql` and `supabase/policies.sql` in SQL Editor
4. Copy `URL` and `anon public key` from **Project Settings → API**

### 2. Deploy to Hugging Face Spaces

1. Fork this repo
2. Create new Space → **Gradio SDK**, **CPU Basic**
3. Add Secrets:

SUPABASE_URL = https://your-project.supabase.co
SUPABASE_ANON_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxx

4. Deploy!

## 🔐 Security Checklist

- [ ] Rotated Supabase keys after exposure
- [ ] Enabled RLS on `chats` table
- [ ] Only `anon` key in frontend
- [ ] `.env` in `.gitignore`
- [ ] No `service_role` in code

## 📊 Data Analysis

Run these in Supabase SQL Editor:

```sql
-- Weekly emotional trends
SELECT DATE_TRUNC('week', created_at) AS week, AVG(sentiment_score) AS avg_sentiment FROM chats WHERE is_user = true GROUP BY week ORDER BY week DESC;

-- Top emotions
SELECT detected_emotion, COUNT(*) FROM chats WHERE is_user = true GROUP BY detected_emotion ORDER BY COUNT(*) DESC;
```

## 📜 License
MIT — use, modify, distribute freely.

Made with ❤️ for your companion.