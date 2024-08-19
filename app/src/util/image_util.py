from PIL import Image, ImageDraw

from display import Display

def test_image_for_panel(display: Display, fill_color: tuple[int, int, int]):
    panel_width = display.width() // display.num_panels
    panel_height = display.height()

    image = Image.new("RGB", (panel_width, panel_height))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, panel_width, panel_height), fill=fill_color)

    return image 

def test_images_for_display(display: Display):
    colors = [(255,0,0), (0,255,0),(0,0,255),(255,255,255)] # TODO - dynamically generate base on num_panels
    panel_images = [test_image_for_panel(display, colors[panel_number]) for panel_number in range(display.num_panels)]
    return panel_images

def display_image_from_panel_images(panel_images):
    num_panels = len(panel_images)

    if num_panels == 0:
        raise ValueError("panel_images is empty")

    panel_width, panel_height = panel_images[0].size

    display_image = Image.new("RGB", (num_panels * panel_width, panel_height))

    current_x = 0
    for panel_image in panel_images:
        display_image.paste(panel_image, (current_x, 0))
        current_x += panel_width

    return display_image

###########################################################################
# TODO - switch over to the panel image strategy below
###########################################################################

from PIL import Image, ImageDraw, ImageFont
from uniseg.graphemecluster import grapheme_clusters

EMOJI_GLYPHS_PATH = 'assets/emoji/64x64'
FONT_PATH = 'assets/fonts/MILL/Canada Type - Screener SC.ttf'

def grapheme_to_hex(grapheme: str) -> str:
    hex_codes = [hex(ord(c)).replace('0x', '') for c in grapheme]
    return '-'.join(hex_codes)

def image_file_for_grapheme(grapheme: str) -> str:
    hex_code = grapheme_to_hex(grapheme)
    return f'{EMOJI_GLYPHS_PATH}/{hex_code}.png'

def lookup_char_image(grapheme: str):
    image_file = image_file_for_grapheme(grapheme)

    try: 
        image = Image.open(image_file)
        image = image.convert('RGB')
    except FileNotFoundError as e:
        return None if grapheme == ' ' else create_char_image(grapheme)
    
    return image

def iterate_graphemes(msg):
    for grapheme in list(grapheme_clusters(msg)):
        yield grapheme

def images_for_message(msg, emoji_only=False):
    return [lookup_char_image(g) for g in iterate_graphemes(msg)]

def create_char_image(char: str, image_size=(64,64), font_path: str = FONT_PATH) -> Image.Image:
    # Image dimensions and border thickness
    img_size = image_size
    border_thickness = 2

    # Create a blank image with a black background
    image = Image.new("RGB", img_size, "black")
    draw = ImageDraw.Draw(image)

    # Load the font
    font_size = 60  # Adjust the font size
    font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default(font_size=font_size)

    # Calculate the position to center the character
    text_width = draw.textlength(char, font=font)

    text_bbox = draw.textbbox((0, 0), char, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    text_x = (img_size[0] - text_width) // 2
    text_y = (img_size[1] - text_height) // 2

    # Draw the character in white
    draw.text((text_x, text_y), char, font=font, fill="white")

    # Draw the 2-pixel black border (already the background, so this is optional)
    draw.rectangle(
        [border_thickness-1, border_thickness-1, img_size[0]-border_thickness, img_size[1]-border_thickness],
        outline="black",
        width=border_thickness
    )

    return image
