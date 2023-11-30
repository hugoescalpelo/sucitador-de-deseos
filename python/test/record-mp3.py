from gpiozero import Button
import sounddevice as sd
from pydub import AudioSegment
import numpy as np
import io

# Configuración
button_pin = 2  # Cambia esto al número de pin que estés usando
fs = 44100  # Frecuencia de muestreo

# Inicializar botón
button = Button(button_pin)

# Función para grabar audio
def record_audio():
    print("Comenzando grabación...")
    # Iniciar una grabación infinita
    with sd.InputStream(samplerate=fs, channels=1) as stream:
        audio_data = []
        while button.is_pressed:
            data, _ = stream.read(fs)
            audio_data.append(data)
        audio_data = np.concatenate(audio_data, axis=0)
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
    save_audio(audio_data)
