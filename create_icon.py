from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """Create a simple icon for the screenshot application"""
    
    # Create a 256x256 image with a transparent background
    size = 256
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Draw a camera-like icon
    # Main body (rounded rectangle)
    body_color = (52, 152, 219)  # Blue
    body_bbox = [50, 80, 206, 176]
    draw.rounded_rectangle(body_bbox, radius=20, fill=body_color)
    
    # Lens
    lens_color = (44, 62, 80)  # Dark gray
    lens_center = (128, 128)
    lens_radius = 35
    draw.ellipse([lens_center[0] - lens_radius, lens_center[1] - lens_radius,
                  lens_center[0] + lens_radius, lens_center[1] + lens_radius], 
                 fill=lens_color)
    
    # Inner lens
    inner_lens_color = (149, 165, 166)  # Light gray
    inner_lens_radius = 25
    draw.ellipse([lens_center[0] - inner_lens_radius, lens_center[1] - inner_lens_radius,
                  lens_center[0] + inner_lens_radius, lens_center[1] + inner_lens_radius], 
                 fill=inner_lens_color)
    
    # Flash
    flash_color = (241, 196, 15)  # Yellow
    flash_bbox = [180, 60, 200, 80]
    draw.rounded_rectangle(flash_bbox, radius=5, fill=flash_color)
    
    # Save as ICO file
    # Convert to different sizes for ICO format
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    icon_images = []
    
    for size in sizes:
        resized = image.resize(size, Image.Resampling.LANCZOS)
        icon_images.append(resized)
    
    # Save as ICO
    icon_images[0].save('icon.ico', format='ICO', sizes=[(img.width, img.height) for img in icon_images])
    print("Icon created successfully: icon.ico")

if __name__ == "__main__":
    create_icon() 