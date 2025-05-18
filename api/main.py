from fastapi import FastAPI, UploadFile, File
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
    

MODEL_PATH = "C:/projects/potato/saved_models/1.keras"
MODEL = tf.keras.models.load_model(MODEL_PATH)
CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]
app = FastAPI()

@app.get("/ping")
async def ping():
    return "hello i am alive"

def read_file_as_image(data)-> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    # image = image.convert("RGB")
    # image = np.array(image)
    return image
    

@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    
):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)
    prediction = MODEL.predict(img_batch)
    predicted_class = CLASS_NAMES[np.argmax(prediction)]
    confidence = np.max(prediction[0])
    return{
        "class": predicted_class,
        "confidence": float(confidence)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000) 
    