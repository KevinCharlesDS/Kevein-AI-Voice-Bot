import openai
import speech_recognition as sr
import pyttsx3
import os

# Set your OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
tts = pyttsx3.init()

def speak(text):
    print(f"\nBot: {text}")
    tts.say(text)
    tts.runAndWait()

def get_openai_response(user_prompt):
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

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Error:\n", e)
        return "Sorry, I couldn't process that. Please try again."

def chat():
    speak("Hi! I'm Kevein. Go ahead and ask me anything.")

    with sr.Microphone() as source:
        while True:
            print("\nListening...")
            try:
                audio = recognizer.listen(source, timeout=5)
                user_input = recognizer.recognize_google(audio)
                print("You:", user_input)

                reply = get_openai_response(user_input)
                speak(reply)

            except sr.UnknownValueError:
                speak("Sorry, I couldn't understand that. Please try again.")
            except sr.RequestError:
                speak("There seems to be an issue with the speech recognition service.")
            except KeyboardInterrupt:
                speak("Goodbye!")
                break

if __name__ == "__main__":
    chat()
