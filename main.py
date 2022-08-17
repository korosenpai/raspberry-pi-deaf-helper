# https://www.youtube.com/watch?v=RHg2UiM_Xgw
# TODO scaricare il modello di italiano completo

from vosk import Model, KaldiRecognizer
import json
import pyaudio

import pygame

from wrap_text import drawText


# load the model
model = Model("models/vosk-model-it-0.22")
rec = KaldiRecognizer(model, 16000)

# set up mic
p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16, channels = 1, rate = 16000, input = True, frames_per_buffer = 8000)
stream.start_stream()

# set up pygame
pygame.init()
X = 1000
Y = 300

screen = pygame.display.set_mode((X, Y))
pygame.display.set_caption("deaf_helper")

font = pygame.font.Font("font.ttf", 32)
MAX_LINES = 3
texts = []

print("ready\n")

running = True
while running:
    data = stream.read(4000, exception_on_overflow = False)
    # if not data:
    #     break



    if rec.AcceptWaveform(data):
        res = rec.Result()
        jres = json.loads(res)
        print(f"\r\nRECOGNIZED: {jres['text']}\n")

        if len(texts) > MAX_LINES:
            texts.pop(0)
        
        if jres['text']:
            texts.append(jres['text'])

    else:
        partial_result = json.loads(rec.PartialResult())
        print(f"\r{partial_result['partial']}", end = "")

        if texts:
            texts.pop()
        texts.append(partial_result['partial'])
    



    screen.fill([255, 255, 255])

    drawText(screen, texts, pygame.Rect(0, 0, 1000, 300), font)


    for event in pygame.event.get():
        # check if quit
        if event.type == pygame.QUIT:
            running = False
    

    pygame.display.update()

        
# print(rec.FinalResult())