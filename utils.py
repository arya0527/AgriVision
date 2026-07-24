import os
from pathlib import Path

import cv2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

try:
    import keras.src.layers.preprocessing.image_preprocessing.resizing as resizing_module
except Exception:
    resizing_module = None


ROOT_DIR = Path(__file__).resolve().parent
MODEL_PATH = ROOT_DIR / "models" / "1.keras"
SAVED_MODEL_PATH = ROOT_DIR / "models" / "1"
IMAGE_SIZE = 256
DEFAULT_CLASS_NAMES = ["Potato___Early_blight", "Potato___Late_blight", "Potato___healthy"]


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
        **kwargs,
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
            **kwargs,
        )
        self.antialias = bool(antialias) if antialias is not None else False

    def get_config(self):
        config = super().get_config()
        config.update({"antialias": self.antialias})
        return config


# Patch the runtime class used by Keras so older/newer model artifacts can deserialize.
try:
    keras_module = tf.keras
    if hasattr(keras_module, "layers"):
        keras_module.layers.Resizing = CompatibleResizing
    if hasattr(tf.keras, "layers"):
        tf.keras.layers.Resizing = CompatibleResizing
except Exception:
    pass

if resizing_module is not None:
    resizing_module.Resizing = CompatibleResizing


_display_name = {
    "Potato___Early_blight": "Early Blight",
    "Potato___Late_blight": "Late Blight",
    "Potato___healthy": "Healthy",
}

_recommendations = {
    "English": {
        "Potato___Early_blight": {
            "medicine": "Mancozeb",
            "dosage": "2.5 g/L",
            "steps": [
                "Remove infected leaves.",
                "Spray Mancozeb every 7 days.",
                "Avoid overwatering.",
                "Ensure good air circulation.",
                "Monitor plants regularly.",
            ],
        },
        "Potato___Late_blight": {
            "medicine": "Metalaxyl + Mancozeb",
            "dosage": "2.5 g/L",
            "steps": [
                "Remove severely infected plants.",
                "Spray immediately.",
                "Avoid overhead irrigation.",
                "Improve field drainage.",
                "Monitor disease spread daily.",
            ],
        },
        "Potato___healthy": {
            "medicine": "None",
            "dosage": "-",
            "steps": [
                "Plant is healthy.",
                "Continue regular monitoring.",
                "Maintain proper irrigation.",
                "Inspect leaves weekly.",
            ],
        },
    },
    "Hindi": {
        "Potato___Early_blight": {
            "medicine": "मैनकोजेब",
            "dosage": "2.5 ग्राम/लीटर",
            "steps": [
                "संक्रमित पत्तियाँ हटाएँ।",
                "हर 7 दिन में स्प्रे करें।",
                "अधिक पानी देने से बचें।",
                "हवा का अच्छा प्रवाह बनाए रखें।",
                "पौधों की नियमित जांच करें।",
            ],
        },
        "Potato___Late_blight": {
            "medicine": "मेटालैक्सिल + मैनकोजेब",
            "dosage": "2.5 ग्राम/लीटर",
            "steps": [
                "संक्रमित पौधों को हटाएँ।",
                "तुरंत स्प्रे करें।",
                "ऊपर से सिंचाई न करें।",
                "जल निकासी सुधारें।",
                "प्रतिदिन निगरानी करें।",
            ],
        },
        "Potato___healthy": {
            "medicine": "कोई दवा नहीं",
            "dosage": "-",
            "steps": [
                "पौधा स्वस्थ है।",
                "नियमित निगरानी करें।",
                "संतुलित सिंचाई बनाए रखें।",
                "साप्ताहिक निरीक्षण करें।",
            ],
        },
    },
}

_model = None
_class_names = None

display_name = _display_name
recommendations = _recommendations


class SavedModelWrapper:
    def __init__(self, path):
        self.path = str(path)
        self.loaded = tf.saved_model.load(self.path)
        self.signature = self.loaded.signatures["serving_default"]
        self.class_names = DEFAULT_CLASS_NAMES
        self._predict_tensor_fn = tf.function(
            lambda images: self.signature(images)["output_0"],
            input_signature=[tf.TensorSpec([None, IMAGE_SIZE, IMAGE_SIZE, 3], tf.float32)],
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
            raise FileNotFoundError(f"Model not found at {MODEL_PATH} or {SAVED_MODEL_PATH}")

        _class_names = list(getattr(_model, "class_names", []) or DEFAULT_CLASS_NAMES)
        if not _class_names:
            _class_names = DEFAULT_CLASS_NAMES
    return _model


def get_model():
    return _load_model()


def load_image(image_path):
    """Load an image from a file path or uploaded file object."""
    if hasattr(image_path, "read"):
        image_bytes = image_path.read()
        if isinstance(image_bytes, str):
            image_bytes = image_bytes.encode("utf-8")

        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Unable to read the uploaded image.")
    else:
        image_path = os.fspath(image_path)
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Unable to read the image: {image_path}")

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_rgb = cv2.resize(image_rgb, (IMAGE_SIZE, IMAGE_SIZE))
    img_array = np.expand_dims(image_rgb.astype(np.float32), axis=0)

    return image, image_rgb, img_array


def predict_image(img_array, model=None):
    """Predict the disease class and confidence for a preprocessed image array."""
    model = model or _load_model()
    predictions = model.predict(img_array, verbose=0)
    class_names = _class_names or list(getattr(model, "class_names", []) or DEFAULT_CLASS_NAMES)
    predicted_class = class_names[np.argmax(predictions[0])]
    confidence = float(round(100 * np.max(predictions[0]), 2))
    return predicted_class, confidence


def make_gradcam_heatmap(img_array, model, last_conv_layer_name=None):
    """Generate a simple gradient-based heatmap for the input image."""
    x = tf.convert_to_tensor(img_array, dtype=tf.float32)
    if x.ndim == 3:
        x = tf.expand_dims(x, axis=0)

    with tf.GradientTape() as tape:
        tape.watch(x)
        predictions = model._predict_tensor(x)
        class_idx = int(tf.argmax(predictions[0]))
        loss = predictions[:, class_idx]

    grads = tape.gradient(loss, x)
    heatmap = tf.reduce_mean(tf.abs(grads), axis=-1)[0]
    heatmap = tf.maximum(heatmap, 0.0)
    heatmap = heatmap / (tf.reduce_max(heatmap) + 1e-8)
    return heatmap.numpy()


def make_gradcam(image_rgb, img_array, model, last_conv_layer_name="conv2d_2"):
    """Generate a Grad-CAM heatmap and overlay for the input image."""
    heatmap = make_gradcam_heatmap(img_array, model, last_conv_layer_name)

    heatmap_resized = cv2.resize(heatmap, (image_rgb.shape[1], image_rgb.shape[0]))
    heatmap_resized = cv2.GaussianBlur(heatmap_resized, (15, 15), 0)
    heatmap_resized = (heatmap_resized - heatmap_resized.min()) / (
        heatmap_resized.max() - heatmap_resized.min() + 1e-8
    )
    heatmap_resized = np.power(heatmap_resized, 2.0)

    p95 = np.percentile(heatmap_resized, 95)
    heatmap_mask = np.where(heatmap_resized >= p95, heatmap_resized, 0.0)

    heatmap_uint8 = np.uint8(255 * heatmap_mask)
    heatmap_color = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
    heatmap_color = cv2.cvtColor(heatmap_color, cv2.COLOR_BGR2RGB)

    overlay = image_rgb.astype(np.float32) * 0.55
    overlay += heatmap_color.astype(np.float32) * 0.95 * heatmap_mask[..., None]
    overlay = np.clip(overlay, 0, 255).astype(np.uint8)

    return heatmap_resized, overlay


def estimate_severity(image_rgb):
    """Estimate disease severity from the input image using HSV thresholds."""
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

    lower = np.array([5, 40, 20])
    upper = np.array([35, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)

    disease_pixels = np.count_nonzero(mask)
    total_pixels = mask.size
    severity_percentage = round((disease_pixels / total_pixels) * 100, 2)

    if severity_percentage < 10:
        severity_level = "Healthy / Very Mild"
    elif severity_percentage < 30:
        severity_level = "Mild"
    elif severity_percentage < 60:
        severity_level = "Moderate"
    else:
        severity_level = "Severe"

    return severity_percentage, severity_level


def recommend_treatment(predicted_class, language="English"):
    """Return treatment information for a predicted disease class in the selected language."""
    treatment_dict = recommendations.get(language, recommendations["English"])

    if predicted_class in treatment_dict:
        info = treatment_dict[predicted_class]
    else:
        predicted_key = next(
            (key for key, value in display_name.items() if value == predicted_class),
            predicted_class,
        )
        info = treatment_dict[predicted_key]

    return info["medicine"], info["dosage"], info["steps"]


def display_results(
    image_rgb,
    heatmap,
    overlay,
    predicted_class,
    confidence,
    severity_percentage,
    severity_level,
    medicine,
    dosage,
    steps,
):
    """Display the original image, Grad-CAM heatmap, overlay and report details."""
    fig=plt.figure(figsize=(18, 6))

    plt.subplot(1, 3, 1)
    plt.imshow(image_rgb)
    plt.title("Original Image")
    plt.axis("off")

    plt.subplot(1, 3, 2)
    plt.imshow(heatmap, cmap="jet")
    plt.title("Grad-CAM Heatmap")
    plt.axis("off")

    plt.subplot(1, 3, 3)
    plt.imshow(overlay)
    plt.title("Grad-CAM Overlay")
    plt.axis("off")

    plt.tight_layout()
    if plt.get_backend().lower().endswith("agg"):
        plt.close(fig)
    else:
        plt.show(block=False)

    disease_name = display_name.get(predicted_class, predicted_class)

    print("=" * 50)
    print("AI Potato Disease Detection Report")
    print("=" * 50)
    print(f"Disease          : {disease_name}")
    print(f"Confidence       : {confidence:.2f}%")
    print(f"Severity         : {severity_percentage:.2f}% ({severity_level})")
    print(f"Medicine         : {medicine}")
    print(f"Dosage           : {dosage}")
    print("\nRecommended Treatment:")
    for i, step in enumerate(steps, start=1):
        print(f"{i}. {step}")
    print("=" * 50)


def predict_leaf(image_path, language="English"):
    """Run the full inference pipeline for a single leaf image."""
    model = _load_model()
    _, image_rgb, img_array = load_image(image_path)
    predicted_class, confidence = predict_image(img_array, model=model)
    heatmap, overlay = make_gradcam(image_rgb, img_array, model)
    severity_percentage, severity_level = estimate_severity(image_rgb)
    medicine, dosage, steps = recommend_treatment(predicted_class, language)


    overlay_path = ROOT_DIR / "prediction_overlay.png"
    cv2.imwrite(str(overlay_path), cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR))

    return {
        "prediction": predicted_class,
        "confidence": confidence,
        "severity": severity_percentage,
        "severity_level": severity_level,
        "medicine": medicine,
        "dosage": dosage,
        "steps": steps,
        "overlay": overlay,
        "heatmap": heatmap,
        "disease_name": display_name.get(predicted_class, predicted_class),
        "overlay_path": str(overlay_path),
    }


__all__ = [
    "IMAGE_SIZE",
    "display_name",
    "recommendations",
    "get_model",
    "load_image",
    "predict_image",
    "make_gradcam",
    "estimate_severity",
    "recommend_treatment",
    "display_results",
    "predict_leaf",
]