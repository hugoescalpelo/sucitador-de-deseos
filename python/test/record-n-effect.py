from gpiozero import Button
import sounddevice as sd
from pydub import AudioSegment
import numpy as np
import datetime
import random
import threading
import os
import subprocess

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

# Función para cambiar la tonalidad usando ffmpeg
def change_pitch(filename, semitones):
    output_file = f"pitch_changed_{filename}"
    subprocess.run(["ffmpeg", "-i", filename, "-filter_complex", f"rubberband=pitch={semitones}", output_file])
    return output_file

# Función para reproducir audios de forma aleatoria con cambio de tonalidad
def play_random_recordings_with_pitch_change():
    while True:
        try:
            files = os.listdir(recordings_folder)
            if files:
                filename = random.choice(files)
                file_path = os.path.join(recordings_folder, filename)

                # Cambiar la tonalidad
                semitones = random.choice([-4, -2, 2, 4])
                changed_file = change_pitch(file_path, semitones)

                # Reproducir el archivo con tonalidad cambiada
                audio = AudioSegment.from_file(changed_file)
                playback = audio.export(format="wav")
                os.system(f"aplay {playback.name}")
        except Exception as e:
            print(f"Error al reproducir con cambio de tonalidad: {e}")

# Iniciar el hilo de reproducción con cambio de tonalidad
playback_thread = threading.Thread(target=play_random_recordings_with_pitch_change, daemon=True)
playback_thread.start()

# Loop principal
print("Presione el botón para grabar.")
while True:
    button.wait_for_press()
    audio_data = record_audio()
    filename = generate_filename()
    save_audio(audio_data, filename)
