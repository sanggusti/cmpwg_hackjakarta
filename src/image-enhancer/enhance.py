import os
from transformers import pipeline
import torch
from dotenv import load_dotenv
from PIL import Image
from IPython.display import display
from diffusers import StableDiffusionImg2ImgPipeline

load_dotenv()

MODEL = os.getenv("DIFFUSION_MODEL")
IMG_PATH = os.getenv("IMG_PATH")

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
pipe = pipeline(task="image-to-image", model=MODEL, device=device)

def enhance_image(image_path):
    image_path = IMG_PATH
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(MODEL, torch_dtype=torch.float16)
    cuda = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    pipe = pipe.to(cuda)

    init_image = Image.open(image_path).convert("RGB").resize((768, 512))

    display(init_image)

    prompt = "increase the food image quality, sharpness, bluriness, pixel, increase the contrast, saturation and brightness"

    images = pipe(prompt=prompt, image=init_image, strength=.2, guidance_scale=7.5).images

    return images

