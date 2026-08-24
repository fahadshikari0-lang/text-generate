import torch

from diffusers import StableDiffusionPipeline

from transformers import (
    BlipProcessor,
    BlipForConditionalGeneration
)


class ImageGenerator:

    def __init__(self):

        # ==========================================
        # DEVICE
        # ==========================================

        self.device = (
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )

        print("================================")
        print("Device:", self.device)
        print("================================")


        # ==========================================
        # TEXT → IMAGE
        # TINY-SD
        # ==========================================

        self.image_model_id = "segmind/tiny-sd"

        print("Loading Tiny-SD...")

        if self.device == "cuda":
            image_dtype = torch.float16
        else:
            image_dtype = torch.float32

        self.pipe = StableDiffusionPipeline.from_pretrained(
            self.image_model_id,
            torch_dtype=image_dtype
        )

        self.pipe = self.pipe.to(
            self.device
        )

        print("Tiny-SD loaded successfully!")


        # ==========================================
        # IMAGE → TEXT
        # BLIP
        # ==========================================

        self.text_model_id = (
            "Salesforce/blip-image-captioning-base"
        )

        print("Loading BLIP...")

        self.blip_processor = (
            BlipProcessor.from_pretrained(
                self.text_model_id
            )
        )

        self.blip_model = (
            BlipForConditionalGeneration.from_pretrained(
                self.text_model_id
            )
        )

        self.blip_model = self.blip_model.to(
            self.device
        )

        self.blip_model.eval()

        print("BLIP loaded successfully!")

        print("================================")
        print("Both models loaded successfully!")
        print("================================")


    # ==========================================
    # TEXT → IMAGE
    # ==========================================

    def generate_image(self, prompt):

        image = self.pipe(
            prompt=prompt,
            height=512,
            width=512,
            num_inference_steps=20,
            guidance_scale=7.5
        ).images[0]

        return image


    # ==========================================
    # IMAGE → TEXT
    # ==========================================

    def generate_text(self, image):

        # Convert image to RGB

        image = image.convert("RGB")

        # Prepare image

        inputs = self.blip_processor(
            images=image,
            return_tensors="pt"
        )

        # Move tensors to CPU/GPU

        inputs = {
            key: value.to(self.device)
            for key, value in inputs.items()
        }

        # Generate caption

        with torch.no_grad():

            output = self.blip_model.generate(
                **inputs,
                max_new_tokens=50,
                num_beams=3
            )

        # Convert tokens to text

        text = self.blip_processor.decode(
            output[0],
            skip_special_tokens=True
        )

        return text