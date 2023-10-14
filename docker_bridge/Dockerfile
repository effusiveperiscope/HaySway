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

# Download bridge code
RUN mkdir -p ~/hay_say/hay_sway_bridge
RUN wget \
    https://raw.githubusercontent.com/effusiveperiscope/HaySway/main/docker_bridge/main.py \
    -P ~/hay_say/hay_sway_bridge

# Run Hay Sway bridge
CMD ["/bin/sh", "-c", "/root/hay_say/.venvs/hay_sway_bridge/bin/python /root/hay_say/hay_sway_bridge/main.py"]
