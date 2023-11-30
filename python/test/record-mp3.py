from gpiozero import Button
import sounddevice as sd
from pydub import AudioSegment
import numpy as np
import io

# Configuración
button_pin = 2  # Cambia esto al número de pin que estés usando
fs = 44100  # Frecuencia de muestreo
duration = 10  # Duración máxima de grabación en segundos

# Inicializar botón
button = Button(button_pin)

# Función para grabar audio
def record_audio():
    print("Comenzando grabación...")
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    print("Grabación finalizada")
    return audio_data

# Función para guardar el audio en formato MP3
def save_audio(audio_data, filename="grabacion.mp3"):
    audio = AudioSegment(
        audio_data.tobytes(),
        frame_rate=fs,
        sample_width=audio_data.dtype.itemsize,
        channels=1
    )
    audio.export(filename, format="mp3")
    print(f"Audio guardado como {filename}")

# Loop principal
print("Presione el botón para grabar.")
while True:
    button.wait_for_press()
    audio_data = record_audio()
    button.wait_for_release()
    save_audio(audio_data)
