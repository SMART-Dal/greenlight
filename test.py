import os
from pathlib import Path

script = "/home/saurabh/method-energy-dataset/projects/tensorflow_docs_patched/site/en/tutorials/audio/transfer_learning_audio_method-level.py"
base_path = os.path.basename(Path(script)).replace("_method-level.py","")
# base_path, ext = os.path.splitext(Path(script))
print(base_path)