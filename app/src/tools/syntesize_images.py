import sys
from PIL import Image, ImageEnhance
import os
import random

def create_image_variants(image_path, num_variants):
    # Load the original image
    original_image = Image.open(image_path)
    base_name, ext = os.path.splitext(image_path)
    
    for i in range(num_variants):
        # Create a color variant
        enhancer = ImageEnhance.Color(original_image)
        factor = 0.1 + (i / num_variants) * 1.9  # Vary the color factor between 0.1 and 2.0
        variant_image = enhancer.enhance(factor)
        
        # Randomly reassign the red value
        variant_image = variant_image.convert("RGB")
        data = variant_image.getdata()
        new_data = [(random.randint(0, 255), g, b) for r, g, b in data]
        variant_image.putdata(new_data)
        
        # Save the variant image
        variant_filename = f"{base_name}-var{i:04d}{ext}"
        variant_image.save(variant_filename)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python syntesize_images.py <image_path> [num_variants]")
        sys.exit(1)
    
    image_path = sys.argv[1]
    num_variants = int(sys.argv[2]) if len(sys.argv) > 2 else 10  # Default to 10 variants if not provided

    create_image_variants(image_path, num_variants)
