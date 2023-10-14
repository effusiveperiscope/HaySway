FROM nvidia/cuda:11.8.0-base-ubuntu20.04
ENV TZ=Etc/GMT
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone.
RUN apt update && apt install -y \
    git \
    gcc \
    g++ \
    python3.8-dev \
    python3.8-venv \
    python3.9-venv \
    wget \
    portaudio19-dev \
    libsndfile1 \
    ffmpeg

RUN python3.9 -m venv ~/hay_say/.venvs/hay_sway_bridge;
RUN ~/hay_say/.venvs/hay_sway_bridge/bin/pip install \
    --no-cache-dir --upgrade pip wheel
RUN ~/hay_say/.venvs/hay_sway_bridge/bin/pip install \
    Flask==2.2.3 hay-say-common==0.2.0 requests==2.31.0

EXPOSE 7802
