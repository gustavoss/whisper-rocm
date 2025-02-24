# Use a imagem base do PyTorch com suporte ao ROCm
FROM rocm/pytorch

# Defina a variável de ambiente para o diretório de modelos
ENV WHISPER_MODEL_DIR=/docker/whisper

# Crie o diretório para armazenar os modelos
RUN mkdir -p ${WHISPER_MODEL_DIR}

# Instale dependências necessárias
RUN apt-get update && apt-get install -y \
    ffmpeg \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Instale bibliotecas Python necessárias
RUN pip install --no-cache-dir \
    datasets \
    ipywidgets \
    transformers \
    numba \
    openai-whisper \
    fastapi \
    uvicorn \
	python-multipart

# Defina o diretório de trabalho
WORKDIR /app

# Especifica o diretório de cache do Whisper
ENV XDG_CACHE_HOME=${WHISPER_MODEL_DIR}

# Copia o script da API para o container
COPY api.py /app/api.py

# Expor a porta da API
EXPOSE 9001

# Comando padrão ao iniciar o contêiner
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "9001"]
