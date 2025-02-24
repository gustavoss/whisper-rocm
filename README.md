# Whisper ROCm Docker Image

This Dockerfile creates a Whisper ROCm image.

## Install Instructions

### Step 1: Clone the repository
```bash
git clone https://github.com/gustavoss/whisper-rocm.git
```

### Step 2: Navigate into the repository
```bash
cd ./whisper-rocm
```

### Step 3: Navigate into the repository
```bash
docker build -t whisper-rocm .
```

### Step 4: Navigate into the repository
```bash
docker run -d \
  --name=whisper \
  --device=/dev/kfd \
  --device=/dev/dri \
  -e AMD_SERIALIZE_KERNEL=3 \
  -e TORCH_USE_HIP_DSA=1 \
  -e HSA_OVERRIDE_GFX_VERSION=10.3.0 \
  -p 9001:9001 \
  -v /docker/whisper:/docker/whisper \
  --security-opt seccomp=unconfined \
  whisper-rocm
```

### Step 5: Web interface
You can also use whisper-gui to transcribe audio via a web interface:
https://github.com/gustavoss/whisper-gui
