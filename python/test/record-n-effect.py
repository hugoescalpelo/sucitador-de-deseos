from gpiozero import Button
import sounddevice as sd
from pydub import AudioSegment
import numpy as np
import io
import datetime
import random
import threading
import os
import simpleaudio as sa

# Configuración
button_pin = 4  # Cambia esto al número de pin que estés usando
fs = 44100  # Frecuencia de muestreo
gain = 0.8  # Ajuste de ganancia
bit_depth = 16  # Profundidad de bits
recordings_folder = "recordings"  # Carpeta para guardar las grabaciones
os.makedirs(recordings_folder, exist_ok=True)

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

# Función para generar el nombre del archivo
def generate_filename():
    now = datetime.datetime.now()
    return os.path.join(recordings_folder, now.strftime("%Y-%m-%d-%H-%M-%S.mp3"))

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

# Velocidades de reproducción para simular diferentes tonalidades
velocidades = [0.8, 0.9, 1.1]  # Ejemplo: 0.9x, 1.0x (normal), 1.1x

# Función para aplicar efectos de audio
def apply_audio_effects(audio_segment):
    # Elegir una velocidad aleatoria
    velocidad = random.choice(velocidades)
    return audio_segment.speedup(playback_speed=velocidad)

# Función para reproducir audios de forma aleatoria con efectos
def play_random_recordings_with_effects():
    while True:
        try:
            files = os.listdir(recordings_folder)
            if files:
                filename = random.choice(files)
                file_path = os.path.join(recordings_folder, filename)
                audio = AudioSegment.from_file(file_path)

                # Aplicar efectos de audio
                audio_with_effects = apply_audio_effects(audio)

                playback = sa.play_buffer(
                    audio_with_effects.raw_data, 
                    num_channels=audio_with_effects.channels, 
                    bytes_per_sample=audio_with_effects.sample_width, 
                    sample_rate=audio_with_effects.frame_rate
                )
                playback.wait_done()
        except Exception as e:
            print(f"Error al reproducir con efectos: {e}")

# Hilo para reproducir grabaciones
playback_thread = threading.Thread(target=play_random_recordings_with_effects, daemon=True)
playback_thread.start()

# Loop principal
print("Presione el botón para grabar.")
while True:
    button.wait_for_press()
    audio_data = record_audio()
    filename = generate_filename()
    save_audio(audio_data, filename)
