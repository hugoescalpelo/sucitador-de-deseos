from gpiozero import Button
import sounddevice as sd
from pydub import AudioSegment
import numpy as np
import io
import datetime

# Configuración
button_pin = 4  # Cambia esto al número de pin que estés usando
fs = 44100  # Frecuencia de muestreo
gain = 0.8  # Ajuste de ganancia
bit_depth = 16  # Profundidad de bits

# Inicializar botón
button = Button(button_pin)

# Función para ajustar la profundidad de bits
def adjust_bit_depth(audio_data, target_depth):
    max_val = 2**(target_depth - 1) - 1
    scaled_data = audio_data / np.max(np.abs(audio_data)) * max_val
    return scaled_data.astype(np.int16) if target_depth == 16 else scaled_data.astype(np.int32)

# Función para grabar audio
def record_audio():
    print("Comenzando grabación...")
    with sd.InputStream(samplerate=fs, channels=1) as stream:
        audio_data = []
        while button.is_pressed:
            data, _ = stream.read(fs)
            data = data * gain
            audio_data.append(data)
        audio_data = np.concatenate(audio_data, axis=0)
        audio_data = adjust_bit_depth(audio_data, bit_depth)
    print("Grabación finalizada")
    return audio_data

# Función para generar el nombre del archivo basado en la fecha y hora actuales
def generate_filename():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d-%H-%M-%S.mp3")

# Función para guardar el audio en formato MP3
def save_audio(audio_data, filename):
    sample_width = 2 if bit_depth == 16 else 3
    audio = AudioSegment(
        audio_data.tobytes(),
        frame_rate=fs,
        sample_width=sample_width,
        channels=1
    )
    audio.export(filename, format="mp3")
    print(f"Audio guardado como {filename}")

# Loop principal
print("Presione el botón para grabar.")
while True:
    button.wait_for_press()
    audio_data = record_audio()
    filename = generate_filename()
    save_audio(audio_data, filename)
