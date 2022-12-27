import speech_recognition as sr
import os, sys

old_stderr = os.dup(2)
def mute_on():
    devnull = os.open(os.devnull, os.O_WRONLY)
    
    sys.stderr.flush()
    os.dup2(devnull, 2)
    os.close(devnull)

def mute_off():
    os.dup2(old_stderr, 2)
    os.close(old_stderr)


def recognize_speech_from_mic(recognizer, microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio, language = "bn-BN")
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response

def voice():

    recognizer = sr.Recognizer()
    if os.name!='nt': mute_on()
    microphone = sr.Microphone()
    if os.name!='nt': mute_off()
    print('Listening... (Press "Ctrl+C" to cancel)')
    voice_text = recognize_speech_from_mic(recognizer, microphone)
    if voice_text["transcription"]:
        print(voice_text['transcription'])
        # f = open("output.txt", "w")
        with open("output.txt", "w", encoding="utf-8") as f:
            f.write(voice_text['transcription'])
            f.close()
        return voice_text['transcription']

    if not voice_text["success"]:
        print("I didn't catch that. What did you say?\n")
    if voice_text["error"]:
        print("ERROR: {}".format(voice_text["error"]))
    
voice()