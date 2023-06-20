import requests
import json
import time


class whisper_api():
    def __init__(self, HF_Token) -> None:
        self.API_URL = "https://api-inference.huggingface.co/models/openai/whisper-base.en"
        self.Headers = {"Authorization": f"Bearer {HF_Token}"}

    def transcribe(self, audio_file_path: str):
        print('whisper working...')
        with open(audio_file_path, 'rb') as audio:
            data = audio.read()
        res = requests.post(self.API_URL, headers=self.Headers, data=data)
        # Verificar si el modelo está cargado completamente
        while res.status_code == 503 and "estimated_time" in res.json():
            estimated_time = res.json()["estimated_time"]
            print(
                f"El modelo está cargando. Esperando {estimated_time} segundos...")
            time.sleep((estimated_time+10))
            res = requests.post(self.API_URL, headers=self.Headers, data=data)

        response_data = json.loads(res.text)
        return response_data.get('text', '')


