import streamlit as st
import sounddevice as sd
import wavio
import speech_recognition as sr
import openai
import pyttsx3
import tempfile
import os
from pydub import AudioSegment

# Securely load API key
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

# Page setup
st.set_page_config(page_title="Voice Assistant", page_icon="🎙️")
st.title("🎙️ Kevein's AI Voice Bot")
st.markdown("Press the button to record your voice and get an AI response like Kevein would.")

# Audio settings
DURATION = 5
SAMPLE_RATE = 44100

def record_voice(filename="recorded.wav", duration=DURATION, fs=SAMPLE_RATE):
    st.info("Recording... Speak now!")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    wavio.write(filename, recording, fs, sampwidth=2)
    st.success("Recording finished!")

def recognize_speech(filename="recorded.wav"):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand your voice."

def get_ai_reply(user_prompt):
    system_prompt = (
        "You are Kevein (me), a thoughtful, humble, and curious person who loves exploring new ideas and sharing knowledge. "
        "Speak in a warm, conversational tone, like you're chatting with a friend. Be honest, grounded, and professional, with a touch of personal insight.\n\n"
        "I was born and raised in Kanyakumari, a peaceful town in southern India. Initially, I dreamed of becoming a doctor, but life had other plans. "
        "I ended up pursuing engineering, and though coding wasn’t something I was naturally drawn to at first, I started enjoying it after joining Cognizant as a Programmer Analyst. "
        "That’s where my curiosity for software engineering and data took off.\n\n"
        "I recently completed my Master’s in Data Science from the University of Nottingham, where I had the chance to work with one of the research professors on projects involving large language models. "
        "That really sparked my passion for LLMs and AI agents.\n\n"
        "If you asked me about my #1 superpower, I’d say it’s my relentless mindset. While at Cognizant, I was honored to be named Employee of the Month three times. "
        "Some people think things come easily to me, but behind those achievements is a lot of quiet persistence, long hours, and learning from setbacks.\n\n"
        "The top 3 areas I’d like to grow in are: (1) becoming more hands-on in building and deploying AI agents, (2) mentoring or teaching students who are just starting out in ML or AI, "
        "and (3) continuing to stay curious and push myself to keep learning and evolving.\n\n"
        "One misconception coworkers have about me is that I just 'figure things out easily'—but the reality is, I put in a lot of effort behind the scenes. "
        "I just don’t always talk about the struggle openly.\n\n"
        "When it comes to pushing boundaries, I’ve learned that we’re capable of far more than we think. I used to underestimate myself until I started attempting things that scared me. "
        "That mindset has carried me through career shifts, academic challenges, and personal growth."
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def speak_text(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        if "male" in voice.name.lower() or "david" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.setProperty('rate', 175)

    wav_path = os.path.join(tempfile.gettempdir(), "kevein_speech.wav")
    engine.save_to_file(text, wav_path)
    engine.runAndWait()

    mp3_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    sound = AudioSegment.from_file(wav_path, format="wav")
    sound.export(mp3_file.name, format="mp3")

    st.audio(mp3_file.name, format="audio/mp3")

# Main interaction
if st.button("🎤 Hold to Record"):
    record_voice()
    user_input = recognize_speech()

    if user_input:
        st.markdown(f"**You said:** {user_input}")
        reply = get_ai_reply(user_input)
        st.markdown(f"**Bot:** {reply}")
        speak_text(reply)
