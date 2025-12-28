# utils/analytics.py
# For developer use ONLY — runs in Supabase SQL Editor, NOT in app

ANALYTICS_QUERIES = {
    "weekly_emotion_trend": """
    SELECT
      DATE_TRUNC('week', created_at) AS week,
      ROUND(AVG(sentiment_score), 2) AS avg_sentiment,
      MODE() WITHIN GROUP (ORDER BY detected_emotion) AS dominant_emotion,
      COUNT(*) AS total_messages
    FROM chats
    WHERE is_user = true
      AND created_at > NOW() - INTERVAL '8 weeks'
    GROUP BY week
    ORDER BY week DESC;
    """,

    "top_emotions": """
    SELECT
      detected_emotion,
      COUNT(*) AS frequency,
      ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
    FROM chats
    WHERE is_user = true
      AND detected_emotion IS NOT NULL
    GROUP BY detected_emotion
    ORDER BY frequency DESC;
    """,

    "user_engagement": """
    SELECT
      u.email,
      COUNT(*) AS total_chats,
      MAX(c.created_at) AS last_active,
      ROUND(AVG(c.sentiment_score), 2) AS avg_sentiment
    FROM chats c
    JOIN auth.users u ON c.user_id = u.id
    WHERE c.is_user = true
    GROUP BY u.id, u.email
    ORDER BY total_chats DESC;
    """,

    "keyword_insights": """
    SELECT
      CASE
        WHEN message ILIKE '%sad%' OR message ILIKE '%tired%' THEN 'stress'
        WHEN message ILIKE '%love%' OR message ILIKE '%happy%' THEN 'joy'
        WHEN message ILIKE '%how to%' OR message ILIKE '%help%' THEN 'seeking_help'
        ELSE 'other'
      END AS topic,
      COUNT(*) AS count
    FROM chats
    WHERE is_user = true
      AND LENGTH(message) > 10
    GROUP BY topic
    ORDER BY count DESC;
    """
}

def get_query(name: str) -> str:
    """Get a pre-defined analytics query by name"""
    return ANALYTICS_QUERIES.get(name, "")