import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils import predict_leaf


def test_predict_leaf_returns_expected_keys():
    image_path = Path("training/PlantVillage/Potato___healthy/0f4ebc5a-d646-436a-919d-961342997cde___RS_HL 4183.JPG")
    if not image_path.exists():
        image_path = next(Path("training/PlantVillage").glob("**/*.JPG"))

    result = predict_leaf(str(image_path), language="English")

    assert set(result.keys()) >= {"prediction", "confidence", "severity", "severity_level", "medicine", "dosage", "steps", "overlay", "heatmap", "disease_name"}
    assert isinstance(result["confidence"], (int, float))
    assert isinstance(result["steps"], list)
    assert isinstance(result["overlay"], np.ndarray)
    assert isinstance(result["heatmap"], np.ndarray)
