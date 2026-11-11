#!/usr/bin/env bash
# One-time setup for a fresh session: voice engine + model files.
set -e
pip install --break-system-packages kokoro-onnx soundfile numpy pillow scipy faster-whisper "rembg[cpu]"
mkdir -p ../models
for f in kokoro-v1.0.onnx voices-v1.0.bin; do
  [ -s ../models/$f ] || curl -sL -o ../models/$f "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/$f"
done
cp -n voice_smooth.npy ../models/voice_smooth.npy 2>/dev/null || true
sudo apt-get install -y -q fonts-inter fonts-noto-color-emoji >/dev/null 2>&1 || true
echo "setup done"
