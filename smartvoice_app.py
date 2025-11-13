#smart voice_app.py

import streamlit as st
from transformers import pipeline, MarianMTModel, MarianTokenizer
import pyttsx3
import tempfile
import os
import speech_recognition as sr
import soundfile as sf

# 🧠 GPT-2 Response Generator
nlp = pipeline("text-generation", model="gpt2")

# 🌍 Translation Setup
def load_translator(src, tgt):
    model_name = f"Helsinki-NLP/opus-mt-{src}-{tgt}"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    return tokenizer, model

def translate(text, src="en", tgt="sw"):
    tokenizer, model = load_translator(src, tgt)
    tokens = tokenizer.prepare_seq2seq_batch([text], return_tensors="pt")
    translated = model.generate(**tokens)
    return tokenizer.decode(translated[0], skip_special_tokens=True)

# 🔊 Text-to-Speech
def speak(text, lang="en"):
    engine = pyttsx3.init()
    engine.setProperty("rate", 160)
    voices = engine.getProperty("voices")
    for voice in voices:
        if lang == "sw" and "swahili" in voice.name.lower():
            engine.setProperty("voice", voice.id)
            break
        elif lang == "en" and "english" in voice.name.lower():
            engine.setProperty("voice", voice.id)
            break
    engine.say(text)
    engine.runAndWait()

# 🎤 Speech Recognition
def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        return "Sorry, I couldn't understand the audio."

# 🖥️ Streamlit UI
st.set_page_config(page_title="SmartVoice Chatbot", layout="centered")
st.title("🗣️ SmartVoice Chatbot")

lang = st.selectbox("Choose Language", ["English", "Swahili"])
lang_code = "en" if lang == "English" else "sw"

st.markdown("### 🎤 Speak or 💬 Type your message")

audio_file = st.file_uploader("Upload voice (WAV format)", type=["wav"])
text_input = st.text_input("Or type your message here")

if st.button("Submit"):
    if audio_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_file.read())
            user_text = transcribe_audio(tmp.name)
            os.unlink(tmp.name)
    else:
        user_text = text_input

    st.markdown(f"**🧑 You:** {user_text}")

    response = nlp(user_text, max_length=50, num_return_sequences=1)[0]["generated_text"]
    if lang_code == "sw":
        response = translate(response, src="en", tgt="sw")

    st.markdown(f"**🤖 Chatbot:** {response}")
    speak(response, lang=lang_code)