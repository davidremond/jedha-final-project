import base64
import mlflow.keras
import tensorflow as tf
import numpy as np
import os
import cv2
from fastapi import APIRouter, File, UploadFile
from routes.detected_zones_models import DetectedZonesResult

mlops_server_uri = os.environ.get('MLOPS_SERVER_URI')
model_path_multi = os.environ.get('MODEL_PATH_MULTI7')

mlflow.set_tracking_uri(mlops_server_uri)
keras_model = mlflow.keras.load_model(model_path_multi)

# Extract Base Model (if needed)
def initialize_submodel(keras_model, submodel_index=1):
    """
    Initialize the sub-model if the main model is wrapped in multiple layers.
    """
    base_model = keras_model.layers[submodel_index]  # Extract the sub-model

    # Ensure the model is built by passing a dummy input
    input_shape = base_model.input_shape[1:]  # Remove batch dimension
    dummy_input = np.random.random((1, *input_shape)).astype(np.float32)
    _ = base_model(dummy_input)  # Call model to initialize
    return base_model

# Compute Grad-CAM Heatmap
def get_gradcam_heatmap(keras_model, img_array, layer_name):
    """
    Generate Grad-CAM heatmap for an image using a specific model layer.
    """
    # Ensure input shape is correct
    img_array = np.expand_dims(img_array, axis=0) if img_array.ndim == 3 else img_array

    # Extract the convolutional layer and model output
    conv_layer = keras_model.get_layer(layer_name).output  # (None, 2, 2, 2048)
    model_output_layer = keras_model.output  # (None, 7)

    # Create a new model that outputs both feature maps and predictions
    grad_model = tf.keras.models.Model(inputs=keras_model.input, outputs=[conv_layer, model_output_layer])

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array)

        # Select the class with highest probability
        pred_index = tf.argmax(predictions[0])
        loss = tf.gather(predictions[0], pred_index)  # Ensures correct shape

    # Compute gradients
    grads = tape.gradient(loss, conv_outputs)

    # Global Average Pooling of gradients
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    # Multiply the gradients with the feature maps
    conv_outputs = conv_outputs[0]  # Remove batch dimension
    heatmap = tf.reduce_sum(tf.multiply(pooled_grads, conv_outputs), axis=-1)

    # Normalize the heatmap
    heatmap = tf.maximum(heatmap, 0)
    heatmap /= tf.reduce_max(heatmap)  # Normalize between 0-1

    return heatmap.numpy()

# Apply Grad-CAM to Image
def apply_gradcam(byte_array, keras_model, layer_name):
    """
    Applies Grad-CAM on an image and overlays the heatmap on the original image.
    """
    # Load the image
    nparr = np.frombuffer(byte_array, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    img = cv2.resize(img, (224, 224))  # Resize to match model input
    img_array = img.astype(np.float32) / 255.0  # Normalize pixel values

    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension (1, 224, 224, 3)

    # Generate Grad-CAM heatmap
    heatmap = get_gradcam_heatmap(keras_model, img_array, layer_name)

    # Resize heatmap to match original image size
    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
    heatmap = np.uint8(255 * heatmap)  # Convert to uint8 (0-255)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)  # Apply colormap

    # Superimpose heatmap on original image
    superimposed_img = cv2.addWeighted(img, 0.6, heatmap, 0.4, 0)

    _, buffer = cv2.imencode('.jpg', superimposed_img)
    return buffer.tobytes()

router = APIRouter()

@router.post("/detected_zones", 
            response_model=DetectedZonesResult, 
            tags=["Predictions"],
            description="Detect zones in the X-ray image.")
async def detected_zones(
    file: UploadFile = File(..., 
                            description="Upload the X-ray image file here.", 
                            title="X-ray Image File", 
                            include_in_schema=False)
    ):
    """Compute detected zones in the X-ray image with gradcam algorithm.

    Args:
        file: X-ray image file.

    Returns:
        DetectedZonesResult: Result of the detection
    """
    base_model = initialize_submodel(keras_model, submodel_index=1)
    last_conv_layer_name = "mixed8"
    byte_array = await file.read()
    img = apply_gradcam(byte_array, base_model, last_conv_layer_name)
    return DetectedZonesResult(image_with_detected_zones=base64.b64encode(img).decode('utf-8'))
