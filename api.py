from fastapi import FastAPI, UploadFile, File
import whisper
import uvicorn
import os

# Configuração do Whisper
model = whisper.load_model("base")

app = FastAPI()

@app.post("/transcribe/audio/transcriptions")
async def transcribe_audio(file: UploadFile = File(...), language: str = "pt", timestamps: str = "true"):
    """Recebe um arquivo de áudio e retorna a transcrição com timestamps."""
    file_path = f"/tmp/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    # Transcrição com especificação do idioma e timestamps
    result = model.transcribe(file_path, language=language, word_timestamps=(timestamps.lower() == "true"))
    os.remove(file_path)

    return {"text": result["text"], "timestamps": result.get("words", [])}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9001)
