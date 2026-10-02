import os
from pathlib import Path

import cv2
import numpy as np
import tensorflow as tf


ROOT_DIR = Path(__file__).resolve().parent
MODEL_PATH = ROOT_DIR / "models" / "1.keras"
SAVED_MODEL_PATH = ROOT_DIR / "models" / "1"

IMAGE_SIZE = 256

DEFAULT_CLASS_NAMES = [
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy"
]

display_name = {
    "Potato___Early_blight": "Early Blight",
    "Potato___Late_blight": "Late Blight",
    "Potato___healthy": "Healthy"
}


# Keras compatibility for older model artifacts
try:
    import keras.src.layers.preprocessing.image_preprocessing.resizing as resizing_module
except Exception:
    resizing_module = None


class CompatibleResizing(tf.keras.layers.Resizing):

    def __init__(
        self,
        height,
        width,
        interpolation="bilinear",
        crop_to_aspect_ratio=False,
        pad_to_aspect_ratio=False,
        fill_mode="constant",
        fill_value=0.0,
        data_format=None,
        antialias=None,
        **kwargs
    ):
        super().__init__(
            height,
            width,
            interpolation=interpolation,
            crop_to_aspect_ratio=crop_to_aspect_ratio,
            pad_to_aspect_ratio=pad_to_aspect_ratio,
            fill_mode=fill_mode,
            fill_value=fill_value,
            data_format=data_format,
            **kwargs
        )
        self.antialias = bool(antialias) if antialias is not None else False

    def get_config(self):
        config = super().get_config()
        config.update({"antialias": self.antialias})
        return config


try:
    tf.keras.layers.Resizing = CompatibleResizing
except Exception:
    pass

if resizing_module is not None:
    resizing_module.Resizing = CompatibleResizing


_model = None
_class_names = None


class SavedModelWrapper:

    def __init__(self, path):
        self.path = str(path)
        self.loaded = tf.saved_model.load(self.path)
        self.signature = self.loaded.signatures["serving_default"]
        self.class_names = DEFAULT_CLASS_NAMES

        self._predict_tensor_fn = tf.function(
            lambda images: self.signature(images)["output_0"],
            input_signature=[
                tf.TensorSpec(
                    [None, IMAGE_SIZE, IMAGE_SIZE, 3],
                    tf.float32
                )
            ]
        )

    def _predict_tensor(self, images):
        images = tf.convert_to_tensor(images, dtype=tf.float32)
        return self._predict_tensor_fn(images)

    def predict(self, images, verbose=0):
        return self._predict_tensor(images).numpy()


def _load_model():

    global _model, _class_names

    if _model is None:

        if SAVED_MODEL_PATH.exists():
            _model = SavedModelWrapper(SAVED_MODEL_PATH)

        elif MODEL_PATH.exists():
            _model = SavedModelWrapper(MODEL_PATH)

        else:
            raise FileNotFoundError(
                f"Model not found at {MODEL_PATH} or {SAVED_MODEL_PATH}"
            )

        _class_names = list(
            getattr(_model, "class_names", [])
            or DEFAULT_CLASS_NAMES
        )

    return _model


def get_model():
    return _load_model()


def load_image(image_path):

    if hasattr(image_path, "read"):

        image_bytes = image_path.read()

        if isinstance(image_bytes, str):
            image_bytes = image_bytes.encode("utf-8")

        image = cv2.imdecode(
            np.frombuffer(image_bytes, np.uint8),
            cv2.IMREAD_COLOR
        )

        if image is None:
            raise ValueError("Unable to read the uploaded image.")

    else:

        image_path = os.fspath(image_path)

        if not os.path.exists(image_path):
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        image = cv2.imread(image_path)

        if image is None:
            raise ValueError(
                f"Unable to read the image: {image_path}"
            )

    image_rgb = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    image_rgb = cv2.resize(
        image_rgb,
        (IMAGE_SIZE, IMAGE_SIZE)
    )

    img_array = np.expand_dims(
        image_rgb.astype(np.float32),
        axis=0
    )

    return image, image_rgb, img_array


def predict_image(img_array, model=None):

    model = model or _load_model()

    predictions = model.predict(
        img_array,
        verbose=0
    )

    class_names = (
        _class_names
        or getattr(model, "class_names", DEFAULT_CLASS_NAMES)
    )

    predicted_class = class_names[
        np.argmax(predictions[0])
    ]

    confidence = round(
        100 * np.max(predictions[0]),
        2
    )

    return predicted_class, float(confidence)


def make_gradcam_heatmap(img_array, model):

    x = tf.convert_to_tensor(
        img_array,
        dtype=tf.float32
    )

    if x.ndim == 3:
        x = tf.expand_dims(x, axis=0)

    with tf.GradientTape() as tape:

        tape.watch(x)

        predictions = model._predict_tensor(x)

        class_idx = int(
            tf.argmax(predictions[0])
        )

        loss = predictions[:, class_idx]

    grads = tape.gradient(loss, x)

    heatmap = tf.reduce_mean(
        tf.abs(grads),
        axis=-1
    )[0]

    heatmap = tf.maximum(
        heatmap,
        0.0
    )

    heatmap = heatmap / (
        tf.reduce_max(heatmap) + 1e-8
    )

    return heatmap.numpy()


def make_gradcam(image_rgb, img_array, model):

    heatmap = make_gradcam_heatmap(
        img_array,
        model
    )

    heatmap_resized = cv2.resize(
        heatmap,
        (
            image_rgb.shape[1],
            image_rgb.shape[0]
        )
    )

    heatmap_resized = cv2.GaussianBlur(
        heatmap_resized,
        (15, 15),
        0
    )

    heatmap_resized = (
        heatmap_resized - heatmap_resized.min()
    ) / (
        heatmap_resized.max()
        - heatmap_resized.min()
        + 1e-8
    )

    heatmap_resized = np.power(
        heatmap_resized,
        2.0
    )

    p95 = np.percentile(
        heatmap_resized,
        95
    )

    mask = np.where(
        heatmap_resized >= p95,
        heatmap_resized,
        0.0
    )

    heatmap_color = cv2.applyColorMap(
        np.uint8(255 * mask),
        cv2.COLORMAP_JET
    )

    heatmap_color = cv2.cvtColor(
        heatmap_color,
        cv2.COLOR_BGR2RGB
    )

    overlay = (
        image_rgb.astype(np.float32) * 0.55
        + heatmap_color.astype(np.float32)
        * 0.95
        * mask[..., None]
    )

    overlay = np.clip(
        overlay,
        0,
        255
    ).astype(np.uint8)

    return heatmap_resized, overlay


def estimate_severity(image_rgb):

    image_bgr = cv2.cvtColor(
        image_rgb,
        cv2.COLOR_RGB2BGR
    )

    hsv = cv2.cvtColor(
        image_bgr,
        cv2.COLOR_BGR2HSV
    )

    lower = np.array([5, 40, 20])
    upper = np.array([35, 255, 255])

    mask = cv2.inRange(
        hsv,
        lower,
        upper
    )

    severity_percentage = round(
        (
            np.count_nonzero(mask)
            / mask.size
        ) * 100,
        2
    )

    if severity_percentage < 10:
        severity_level = "Healthy / Very Mild"
    elif severity_percentage < 30:
        severity_level = "Mild"
    elif severity_percentage < 60:
        severity_level = "Moderate"
    else:
        severity_level = "Severe"

    return severity_percentage, severity_level


def predict_leaf(image_path):

    model = _load_model()

    _, image_rgb, img_array = load_image(
        image_path
    )

    predicted_class, confidence = predict_image(
        img_array,
        model
    )

    heatmap, overlay = make_gradcam(
        image_rgb,
        img_array,
        model
    )

    severity, severity_level = estimate_severity(
        image_rgb
    )

    overlay_path = (
        ROOT_DIR / "prediction_overlay.png"
    )

    cv2.imwrite(
        str(overlay_path),
        cv2.cvtColor(
            overlay,
            cv2.COLOR_RGB2BGR
        )
    )

    return {
        "prediction": predicted_class,
        "confidence": confidence,
        "severity": severity,
        "severity_level": severity_level,
        "heatmap": heatmap,
        "overlay": overlay,
        "disease_name": display_name.get(
            predicted_class,
            predicted_class
        ),
        "overlay_path": str(overlay_path)
    }


__all__ = [
    "IMAGE_SIZE",
    "display_name",
    "get_model",
    "load_image",
    "predict_image",
    "make_gradcam",
    "estimate_severity",
    "predict_leaf"
]