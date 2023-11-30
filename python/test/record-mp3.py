from gpiozero import Button
import sounddevice as sd
from pydub import AudioSegment
import numpy as np
import io

# Configuración
button_pin = 4  # Cambia esto al número de pin que estés usando
fs = 44100  # Frecuencia de muestreo
gain = 0.8  # Ajuste de ganancia (menor que 1 disminuye, mayor que 1 aumenta)
bit_depth = 16  # Profundidad de bits (16 o 24 usualmente)

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
    # Iniciar una grabación infinita
    with sd.InputStream(samplerate=fs, channels=1) as stream:
        audio_data = []
        while button.is_pressed:
            data, _ = stream.read(fs)
            # Aplicar ajuste de ganancia
            data = data * gain
            audio_data.append(data)
        audio_data = np.concatenate(audio_data, axis=0)
        # Ajustar profundidad de bits
        audio_data = adjust_bit_depth(audio_data, bit_depth)
    print("Grabación finalizada")
    return audio_data

# Función para guardar el audio en formato MP3
def save_audio(audio_data, filename="grabacion.mp3"):
    sample_width = 2 if bit_depth == 16 else 3  # 2 bytes para 16 bits, 3 para 24 bits
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
    save_audio(audio_data)

