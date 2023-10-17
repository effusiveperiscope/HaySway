Provides an alternate local interface for Hay Say with audio recording and drag
and drop (?)

Paste this in `docker_compose.yaml`:
```
  haysway_bridge:
    image: wowitsvul/haysway-bridge:latest
    ports:
      - 7802:7802
    working_dir: /root/hay_say/hay_sway_bridge
    volumes:
      - audio_cache:/root/hay_say/audio_cache
      - models:/root/hay_say/models
      - custom_models:/root/hay_say/custom_models
```
Install python dependencies (`pip install -r requirements.txt`) and run
`main.py`.
