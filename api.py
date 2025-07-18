from fastapi import FastAPI, UploadFile, File, Form
import whisper, gc, torch
import os

device = "gpu" if torch.cuda.is_available() else "cpu"
print("Device em uso:", device)

app = FastAPI()

def format_timestamp(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"[{hours:02}:{minutes:02}:{secs:02}]"

def group_transcription_by_time(segments, interval=5, show_timestamps=True):
    grouped = {}
    for seg in segments:
        start_time = int(seg['start'])
        end_time = int(seg['end'])
        for t in range(start_time, end_time + 1, interval):
            key = t - (t % interval)
            grouped.setdefault(key, []).append(seg['text'])
    output = []
    for key in sorted(grouped.keys()):
        text = ' '.join(grouped[key])
        if show_timestamps:
            timestamp = format_timestamp(key)
            output.append(f"{timestamp}: {text}")
        else:
            output.append(text)
    return '\n'.join(output)

@app.post("/transcribe/audio/transcriptions")
async def transcribe_audio(
    file: UploadFile = File(...),
    language: str = Form("pt"),
    model: str = Form("small"),
    timestamps: str = Form("true")
):
    print(f"Modelo recebido: {model}")
    print(f"Idioma recebido: {language}")
    print(f"Timestamps ativados: {timestamps.lower() == 'true'}")

    file_path = f"/tmp/{file.filename}"
    with open(file_path, "wb") as buf:
        buf.write(await file.read())

    try:
        model_instance = whisper.load_model(model)
    except Exception as e:
        return {"error": f"Erro ao carregar modelo '{model}': {str(e)}"}

    result = model_instance.transcribe(
        file_path,
        language=language,
        word_timestamps=(timestamps.lower() == "true"),
        task="transcribe"
    )

    os.remove(file_path)
    model_instance.cpu()
    del model_instance
    gc.collect()
    torch.cuda.empty_cache()

    formatted = group_transcription_by_time(
        result.get("segments", []),
        interval=5,
        show_timestamps=(timestamps.lower() == "true")
    )

    return {
        "text": result["text"],
        "formatted": formatted
    }
