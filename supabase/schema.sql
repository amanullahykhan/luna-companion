-- Run in Supabase SQL Editor AFTER creating project
-- 1. Extend users table
ALTER TABLE auth.users
ADD COLUMN IF NOT EXISTS full_name TEXT,
ADD COLUMN IF NOT EXISTS preferences JSONB DEFAULT '{}';

-- 2. Chats table — for analysis + privacy
CREATE TABLE IF NOT EXISTS chats (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  message TEXT NOT NULL,
  is_user BOOLEAN NOT NULL,
  -- Analysis fields (filled by free local model)
  sentiment_score FLOAT CHECK (sentiment_score BETWEEN -1 AND 1),
  detected_emotion TEXT,
  -- Metadata (safe to store)
  model_used TEXT DEFAULT 'mistral-7b',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Enable RLS (critical!)
ALTER TABLE chats ENABLE ROW LEVEL SECURITY;

-- 4. Policies: users see ONLY their data
CREATE POLICY "User own chats SELECT" 
ON chats FOR SELECT 
TO authenticated 
USING (auth.uid() = user_id);

CREATE POLICY "User own chats INSERT" 
ON chats FOR INSERT 
TO authenticated 
WITH CHECK (auth.uid() = user_id);

-- 5. Indexes for fast analysis
CREATE INDEX IF NOT EXISTS idx_chats_user_time ON chats (user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_chats_emotion ON chats (detected_emotion);
CREATE INDEX IF NOT EXISTS idx_chats_sentiment ON chats (sentiment_score);