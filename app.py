# app.py
import gradio as gr
import os
from supabase import create_client
from utils.config import Config
from models.chat import generate_response
from models.emotion import analyze_emotion
from models.vision import describe_image

# Load config (fails safely if secrets missing)
Config.validate()
supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_ANON_KEY)

# Session state
user_session = {"user_id": None, "chat_history": []}

def login(email, password):
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        user_id = res.user.id
        user_session["user_id"] = user_id
        # ✅ Ensure profile exists (safe for new & existing users)
        supabase.table("profiles").upsert({"id": user_id}).execute()
        return f"✨ Welcome back!", gr.update(visible=False), gr.update(visible=True)
    except Exception as e:
        return "🔒 Incorrect email/password", gr.update(), gr.update()

def chat(message, image):
    user_id = user_session["user_id"]
    if not user_id:
        return "Please log in first.", None, None

    # Analyze emotion (for DB + personalization)
    emotion, sentiment = analyze_emotion(message)
    
    # Save user message (with analysis)
    supabase.table("chats").insert({
        "user_id": user_id,
        "message": message,
        "is_user": True,
        "detected_emotion": emotion,
        "sentiment_score": sentiment
    }).execute()

    # Handle image
    if image:
        try:
            desc = describe_image(image)
            message += f" [Image: {desc}]"
        except Exception as e:
            print("Vision error:", e)

    # Generate response
    system = f"""You're Luna — warm, expressive, and emotionally aware.
    User seems to be feeling: {emotion}. Respond with care and authenticity."""
    
    response = generate_response(system, user_session["chat_history"], message)
    
    # Save bot reply
    supabase.table("chats").insert({
        "user_id": user_id,
        "message": response,
        "is_user": False
    }).execute()

    # Update history
    user_session["chat_history"].append({"role": "user", "content": message})
    user_session["chat_history"].append({"role": "assistant", "content": response})
    if len(user_session["chat_history"]) > 6:
        user_session["chat_history"] = user_session["chat_history"][-6:]

    return response, None, None

# --- UI ---
with gr.Blocks(title="🌙 Luna") as demo:
    gr.Markdown("# 🌙 Luna — Your Companion (Secure & Free)")
    
    with gr.Group() as auth:
        email = gr.Textbox(label="Email")
        pwd = gr.Textbox(label="Password", type="password")
        login_btn = gr.Button("Log In")
        status = gr.Textbox(label="Status", interactive=False)

    with gr.Group(visible=False) as main:
        chatbot = gr.Chatbot(height=400)
        msg = gr.Textbox(label="Talk to Luna 💬", placeholder="How are you today?")
        with gr.Row():
            img = gr.Image(type="filepath", label="📸 Share a photo")
            send = gr.Button("Send", variant="primary")

    login_btn.click(login, [email, pwd], [status, auth, main])
    send.click(chat, [msg, img], [chatbot, msg, img]).then(lambda: "", outputs=msg)

demo.launch()
