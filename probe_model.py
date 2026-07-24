import tensorflow as tf
import os
from pathlib import Path

root = Path('models').resolve()
for path in [root/'1.keras', root/'1']:
    print('TRY', path)
    if path.is_dir():
        try:
            loaded = tf.saved_model.load(str(path))
            print('SAVED_MODEL_OK', loaded)
            print('SIGNATURES', list(loaded.signatures.keys()))
        except Exception as e:
            print('SAVED_MODEL_FAIL', type(e).__name__, e)
    else:
        try:
            print('LOAD_MODEL', tf.keras.models.load_model(path, compile=False))
        except Exception as e:
            print('LOAD_MODEL_FAIL', type(e).__name__, e)
