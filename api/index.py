import os
import tempfile
from fastapi import FastAPI, File, UploadFile
import numpy as np
import pandas as pd
import parselmouth
from parselmouth.praat import call

app = FastAPI(title="CardioVoice API")


def voice_numbers(path, f0min=75, f0max=300):
  snd = parselmouth.Sound(path)
  snd = snd.extract_part(
      from_time=0.7, to_time=snd.duration - 0.2, preserve_times=False
  )
  pitch = call(snd, "To Pitch", 0.0, f0min, f0max)
  f0_median = call(pitch, "Get quantile", 0, 0, 0.5, "Hertz")
  pp = call(snd, "To PointProcess (periodic, cc)", f0min, f0max)
  jitter = call(pp, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3) * 100
  shimmer = (
      call([snd, pp], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6) * 100
  )
  hnr = call(
      call(snd, "To Harmonicity (cc)", 0.01, f0min, 0.1, 1.0), "Get mean", 0, 0
  )
  return {
      "f0_median_hz": round(float(f0_median), 3),
      "jitter_local_pct": round(float(jitter), 4),
      "shimmer_local_pct": round(float(shimmer), 4),
      "hnr_db": round(float(hnr), 3),
  }


@app.get("/")
def home():
  return {
      "status": "online",
      "project": "CardioVoice API",
      "usage": "Visit /docs to upload a .wav file and test voice analysis.",
  }


@app.post("/analyze")
async def analyze_audio(file: UploadFile = File(...)):
  with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
    tmp.write(await file.read())
    tmp_path = tmp.name
  try:
    metrics = voice_numbers(tmp_path)
    return {"filename": file.filename, "metrics": metrics}
  except Exception as e:
    return {"error": str(e)}
  finally:
    if os.path.exists(tmp_path):
      os.remove(tmp_path)
