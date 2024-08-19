import logging
import random
import time

from PIL import Image, ImageDraw, ImageFont
from uniseg.graphemecluster import grapheme_clusters

from animations.base_animation import BaseAnimation
from display import Display
from util import image_util

logger = logging.getLogger(__name__)

EMOJI_GLYPHS_PATH = 'assets/emoji_glyphs/32x32'
FONT_PATH = 'assets/fonts/MILL/Canada Type - Screener SC.ttf'


def grapheme_to_hex(grapheme: str) -> str:
    hex_codes = [hex(ord(c)).replace('0x', '') for c in grapheme]
    return '-'.join(hex_codes)

def image_file_for_grapheme(grapheme: str) -> str:
    hex_code = grapheme_to_hex(grapheme)
    return f'{EMOJI_GLYPHS_PATH}/{hex_code}.png'


class ShowMessage(BaseAnimation):
    def __init__(self, display: Display) -> None:
        super().__init__(display)

        logger.info(f'Making a SlotMachine for a display with {display.num_panels} panels.')
        self.display = display
        self.panel_width = display.width() // display.num_panels
        self.panel_height = display.height()

        font_path = 'assets/fonts/MILL/Canada Type - Screener SC.ttf'
        font_size = min(self.panel_width, self.panel_height)
        self.word_font = ImageFont.truetype(font_path, size=font_size)

        font_path = 'assets/fonts/Noto_Emoji/static/NotoEmoji-Regular.ttf'
        font_size = min(self.panel_width * 0.8, self.panel_height)
        self.emoji_font = ImageFont.truetype(font_path, size=font_size)

    def panel_image(self, character: str, font: ImageFont, text_color: tuple[int,int,int]):
        image = Image.new("RGB", (self.panel_width, self.panel_height))
        draw = ImageDraw.Draw(image)
    
        text_width = draw.textlength(character, font=font)

        text_bbox = draw.textbbox((0, 0), character, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]


        x = (self.panel_width - text_width) // 2
        y = (self.panel_height - text_height) // 2
    
        draw.text((x, y), character, fill=text_color, font=font)

        return image

    def make_display_images_for_message(self, message):
        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)

        panel_images = [self.panel_image(c, self.word_font, (r,g,b)) for c in message]

        # MODEBUG
        panel_images.append(self.lookup_char_image('🦠'))

        display_images  = []
        display_images.append(image_util.display_image_from_panel_images(panel_images))

        return display_images
    
    def lookup_char_image(self, grapheme: str) -> Image:
        image_file = image_file_for_grapheme(grapheme)

        try: 
            image = Image.open(image_file)
            image = image.convert('RGB')
        except FileNotFoundError as e:
            image =  None if grapheme == ' ' else create_char_image(grapheme)
    
        return image

    async def run(self, message, **kwargs):
        self.display.clear()

        display_images = self.make_display_images_for_message(message)
        final_display_image = display_images[-1]
        for display_image in display_images:
            self.display.setImage(display_image, x_offset=0, y_offset=0)
            time.sleep(0.5)

        flash_delay = 0.08
        time.sleep(flash_delay)
        for flash_color in [(255,0,0),(0,255,0),(0,0,255),(255,255,255)] * 5:
            self.display.fill(flash_color)
            time.sleep(flash_delay)
            self.display.setImage(final_display_image, x_offset=0, y_offset=0)
            time.sleep(flash_delay)

###########################################################################
# TODO - switch over to the panel image strategy below
###########################################################################


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
