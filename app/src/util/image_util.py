from PIL import Image, ImageDraw

from display import Display

def test_image_for_panel(display: Display, fill_color: tuple[int, int, int]):
    panel_width = display.width() // display.num_panels
    panel_height = display.height()

    image = Image.new("RGB", (panel_width, panel_height))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, panel_width, panel_height), fill=fill_color)

    return image 

def test_panel_images_for_display(display: Display):
    # Cycle through white, red, green, blue for the number of panels
    base_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255)]
    colors = [base_colors[i % len(base_colors)] for i in range(display.num_panels)]
    panel_images = [test_image_for_panel(display, colors[panel_number]) for panel_number in range(display.num_panels)]
    return panel_images


def load_image(image_file_path: str, image_size: tuple[int, int] = None, background_color: tuple[int, int, int, int] = (127, 0, 0, 255)) -> Image.Image:
    try:
        image = Image.open(image_file_path).convert("RGBA")
        if image.mode == 'RGBA':
            red_background = Image.new("RGBA", image.size, background_color)
            image = Image.alpha_composite(red_background, image)

        image = image.convert('RGB')

        if image_size != image.size:
            sampling_filter = Image.LANCZOS if image_size > image.size else Image.BICUBIC
            image = image.resize(image_size, sampling_filter)

    except FileNotFoundError as e:
        image = None

    return image

def display_image_from_panel_images(panel_images):
    num_panels = len(panel_images)

    if num_panels == 0:
        raise ValueError("panel_images is empty")

    panel_width, panel_height = panel_images[0].size

    display_image = Image.new("RGB", (num_panels * panel_width, panel_height))

    current_x = 0

    for panel_image in panel_images:
        # All panel are scaled to the panel width, but some may need to be adjusted for height
        image_width, image_height = panel_image.size
        y = (panel_height - image_height) // 2

        display_image.paste(panel_image, (current_x, y))
        current_x += panel_width

    return display_image

def load_animation_from_file(file_path: str, image_size: tuple[int, int] = None) -> tuple[list[Image.Image], int]:
    with Image.open(file_path) as img:
        frames = []
        try:
            while True:
                image =  img.copy()

                if image.mode == 'RGBA':
                    background = Image.new("RGBA", image.size, (127, 0, 0, 255))
                    image = Image.alpha_composite(background, image)

                image = image.convert('RGB')

                if image_size != image.size:
                    sampling_filter = Image.LANCZOS if image_size > image.size else Image.BICUBIC
                    image = image.resize(image_size, sampling_filter)

                frames.append(image)

                img.seek(img.tell() + 1)
        except EOFError:
            pass  # End of frames


        # Get the frames per second (fps) from the info dictionary
        fps = img.info.get('duration', 100)  # Default to 100 ms if not available
        fps = 1000 / fps  # Convert to fps

    return frames, fps
