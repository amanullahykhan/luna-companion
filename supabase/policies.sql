-- supabase/policies.sql
-- Granular RLS policies for chats table

-- Allow authenticated users to SELECT their own chats
CREATE POLICY "User can view own chats" 
ON chats FOR SELECT 
TO authenticated 
USING (auth.uid() = user_id);

-- Allow authenticated users to INSERT their own chats
CREATE POLICY "User can insert own chats" 
ON chats FOR INSERT 
TO authenticated 
WITH CHECK (auth.uid() = user_id);

-- Allow authenticated users to UPDATE their own chats (optional)
CREATE POLICY "User can update own chats" 
ON chats FOR UPDATE 
TO authenticated 
USING (auth.uid() = user_id);

-- Allow authenticated users to DELETE their own chats (optional)
CREATE POLICY "User can delete own chats" 
ON chats FOR DELETE 
TO authenticated 
USING (auth.uid() = user_id);

-- Optional: Allow service_role to run analytics (safe in SQL Editor only)
-- CREATE POLICY "Service role can read all chats for analysis"
-- ON chats FOR SELECT 
-- TO service_role 
-- USING (true);