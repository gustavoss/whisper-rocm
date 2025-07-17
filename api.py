from fastapi import FastAPI, UploadFile, File
import whisper, gc, torch
import os

device = "gpu" if torch.cuda.is_available() else "cpu"
print("Device em uso:", device)

app = FastAPI()

@app.post("/transcribe/audio/transcriptions")
async def transcribe_audio(file: UploadFile = File(...), language: str = "pt", timestamps: str = "true"):
    # salva temporário
    file_path = f"/tmp/{file.filename}"
    with open(file_path, "wb") as buf:
        buf.write(await file.read())

    # carrega o modelo na GPU
    model = whisper.load_model("small")
    result = model.transcribe(file_path, language=language, word_timestamps=(timestamps.lower() == "true"))

    # libera tudo após uso
    os.remove(file_path)
    model.cpu()               # devolve os pesos para a CPU
    del model                 # remove referência
    gc.collect()              # coleta limpeza de Python
    torch.cuda.empty_cache()  # libera cache de VRAM ROCm

    return {"text": result["text"], "timestamps": result.get("words", [])}
