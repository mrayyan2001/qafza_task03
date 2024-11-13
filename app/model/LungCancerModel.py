from tensorflow.keras.models import load_model  # type: ignore
import cv2
import numpy as np
from PIL import Image
import os


class LungCancerModel:
    target_shape = (128, 128)
    categories = ["Malignant cases", "Non-Malignant cases"]

    def __init__(self) -> None:
        self.model = load_model(
            os.path.join(os.path.dirname(__file__), "lung_cancer_model.h5")
        )
        self.image = None

    async def load_image(self, img_path: str):
        # Open the image using PIL and convert to grayscale
        self.image = Image.open(img_path).convert("L")

    async def preprocessing(self):
        # Check the image is not empty
        if self.image is None or self.image.size == 0:
            raise ValueError("Empty image provided for preprocessing.")
        # Convert to numpy array
        self.image = np.asarray(self.image)
        # Ensure the image is in the correct grayscale format
        if len(self.image.shape) != 2:
            raise ValueError("Expected a grayscale image.")
        # Resize the image
        self.image = cv2.resize(
            self.image, LungCancerModel.target_shape, interpolation=cv2.INTER_CUBIC
        )
        # Reshape the image
        self.image = self.image.reshape(-1, *LungCancerModel.target_shape, 1)
        # Normalize the image
        self.image = self.image / 255.0

    async def get_prediction(self):
        predict = self.model.predict(self.image)
        return f"{LungCancerModel.categories[np.round(predict.max()).astype(int)]}, {(predict.max() if predict.max() > 0.5 else 1 - predict.max()) * 100:0.3f}%"
