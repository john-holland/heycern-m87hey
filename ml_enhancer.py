import torch
import numpy as np
from diffusers import StableDiffusionPipeline
from sklearn.preprocessing import StandardScaler
from torch import nn
import torch.nn.functional as F

class MLEnhancer:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.scaler = StandardScaler()
        self._initialize_models()

    def _initialize_models(self):
        """Initialize the machine learning models."""
        # Initialize Stable Diffusion
        self.sd_pipeline = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        ).to(self.device)

        # Initialize image enhancement network
        self.enhancement_net = ImageEnhancementNetwork().to(self.device)

    def enhance_image(self, image, spectrum_data=None):
        """
        Enhance an image using machine learning models.
        
        Args:
            image: Input image array
            spectrum_data: Optional spectrographic data
            
        Returns:
            Enhanced image
        """
        # Convert image to tensor
        image_tensor = torch.from_numpy(image).float().to(self.device)
        
        # Apply enhancement network
        enhanced = self.enhancement_net(image_tensor.unsqueeze(0))
        
        # If spectrum data is available, use it to guide the enhancement
        if spectrum_data is not None:
            enhanced = self._apply_spectrum_guidance(enhanced, spectrum_data)
        
        return enhanced.squeeze(0).cpu().numpy()

    def _apply_spectrum_guidance(self, image, spectrum):
        """Apply spectrographic data to guide image enhancement."""
        # Convert spectrum to image-compatible format
        spectrum_tensor = torch.from_numpy(spectrum['intensity']).float().to(self.device)
        spectrum_tensor = spectrum_tensor.view(1, 1, -1, 1).expand_as(image)
        
        # Combine image and spectrum information
        enhanced = image * (1 + 0.1 * spectrum_tensor)
        return enhanced

    def generate_enhanced_visualization(self, prompt, initial_image=None):
        """
        Generate an enhanced visualization using Stable Diffusion.
        
        Args:
            prompt: Text description for the image
            initial_image: Optional initial image to guide generation
            
        Returns:
            Generated image
        """
        # Prepare the prompt
        full_prompt = f"high quality astronomical visualization of {prompt}, detailed, scientific, accurate"
        
        # Generate image with Stable Diffusion
        with torch.no_grad():
            if initial_image is not None:
                # Use image-to-image generation
                result = self.sd_pipeline(
                    prompt=full_prompt,
                    image=initial_image,
                    strength=0.7
                ).images[0]
            else:
                # Use text-to-image generation
                result = self.sd_pipeline(full_prompt).images[0]
        
        return np.array(result)

class ImageEnhancementNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        
        # Define the enhancement network architecture
        self.conv1 = nn.Conv2d(1, 64, 3, padding=1)
        self.conv2 = nn.Conv2d(64, 64, 3, padding=1)
        self.conv3 = nn.Conv2d(64, 32, 3, padding=1)
        self.conv4 = nn.Conv2d(32, 1, 3, padding=1)
        
    def forward(self, x):
        # Apply enhancement layers
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = self.conv4(x)
        
        return x 