from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from gradio_client import Client, handle_file
import shutil
import os

app = FastAPI()

# Temporary folder jahan photos save hongi
os.makedirs("temp", exist_ok=True)

@app.post("/tryon")
async def tryon(person_photo: UploadFile = File(...), garment_photo: UploadFile = File(...)):
    # 1. Dono photos temporarily save karo
    person_path = f"temp/person.png"
    garment_path = f"temp/garment.png"

    with open(person_path, "wb") as f:
        shutil.copyfileobj(person_photo.file, f)

    with open(garment_path, "wb") as f:
        shutil.copyfileobj(garment_photo.file, f)

    # 2. IDM-VTON space ko call karo
    client = Client("yisol/IDM-VTON")

    result = client.predict(
        dict={"background": handle_file(person_path), "layers": [], "composite": handle_file(person_path)},
        garm_img=handle_file(garment_path),
        garment_des="a piece of clothing",
        is_checked=True,
        is_checked_crop=False,
        denoise_steps=30,
        seed=42,
        api_name="/tryon"
    )

    # 3. Result (image path) wapis Flutter ko bhejo
    output_image_path = result[0]
    return FileResponse(output_image_path)


@app.get("/")
def home():
    return {"status": "Server ready!"}