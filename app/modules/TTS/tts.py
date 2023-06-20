import os
import numpy as np
from bark import SAMPLE_RATE, generate_audio, preload_models
import soundfile as sf

class TTS():
    def __init__(self, path):
        os.environ["SUNO_OFFLOAD_CPU"] = "True"
        os.environ["SUNO_USE_SMALL_MODELS"] = "True"
        preload_models()
        self.audio_path = path

    def to_audio(self, text_prompt: str, SPEAKER: str, format: str):
        try:
            # dividir el texto en palabras
            words = text_prompt.replace(".", ". ").split()
            pieces = []

            if len(words) >= 24:
                for i in range(0, len(words), 24):
                    group_words = ' '.join(words[i:i+24])
                    audio_array = generate_audio(
                        f"{group_words}...", history_prompt=SPEAKER)
                    pieces.append(audio_array)
                final = np.concatenate(pieces)
            else:
                final = generate_audio(
                    f"{words}...", history_prompt=SPEAKER)

            # Utilizar el contexto 'with' para garantizar el cierre adecuado del archivo
            with open(f'{self.audio_path}tts.{format}', 'wb') as file:
                sf.write(file, final, SAMPLE_RATE)
        except Exception as err:
            print(err)
