import torch
from diffusers import StableDiffusionPipeline
import warnings
warnings.filterwarnings('ignore')

def initialize():
    # Initialize the model
    try:
        model_id = "CompVis/stable-diffusion-v1-4"
        device = torch.device("cuda")

        pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)
        pipe = pipe.to(device)
        return {'pipe': pipe}
    except:
        return 'Failed to initialize the text-to-image model'


basic_negative_prompt = """
cropped, blurred, mutated, error, lowres, blurry, low quality, username, 
signature, watermark, text, 
"""


def generate_image(model_data, text_prompt, image_path, config):
    """
    Generate an image from the text prompt.
    """
    guide_scale = config['guidance_scale']
    negative_prompt = config['negative_prompt']
    advanced_negative_prompt = basic_negative_prompt + negative_prompt
    pipe = model_data['pipe']
    image = pipe(prompt=text_prompt,
                 negative_prompt=advanced_negative_prompt,
                 guide_scale=guide_scale,
                 num_inference_steps=30,
                 width=704, height=512
                 ).images[0]

    image.save(image_path)
