import os
import numpy as np
from bark import SAMPLE_RATE, generate_audio, preload_models
import soundfile as sf

class TTS():
    def __init__(self, path, USE_SMALL_MODELS):
        os.environ["SUNO_OFFLOAD_CPU"] = str(USE_SMALL_MODELS)
        os.environ["SUNO_USE_SMALL_MODELS"] = str(USE_SMALL_MODELS)
        preload_models()
        self.audio_path = path

    def to_audio(self, text_prompt: str, SPEAKER: str = 'v2/en_speaker_9' , format: str = 'ogg'):
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
                final = generate_audio(text_prompt, history_prompt=SPEAKER)

            with open(f'{self.audio_path}tts.{format}', 'wb') as file:
                sf.write(file, final, SAMPLE_RATE)
        except Exception as err:
            print(err)
