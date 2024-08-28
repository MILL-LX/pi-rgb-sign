import random

from PIL import Image, ImageDraw, ImageFont
from uniseg.graphemecluster import grapheme_clusters

from display import Display

##############################################################
# Configuration Constants
##############################################################
EMOJI_GLYPHS_PATH = 'assets/emoji_glyphs/32x32'

def _graphemes_from_message(message):
    return list(grapheme_clusters(message))

def _grapheme_to_hex(grapheme: str) -> str:
    hex_codes = [hex(ord(c)).replace('0x', '') for c in grapheme]
    return '-'.join(hex_codes)

def _image_filepath_for_grapheme(grapheme: str) -> str:
    hex_code = _grapheme_to_hex(grapheme)
    return f'{EMOJI_GLYPHS_PATH}/{hex_code}.png'

class DisplayImageGenerator:
    def __init__(self, display: Display, font_path: str) -> None:
        self.display = display

        font_size = min(self.display.panel_width(), self.display.panel_height())
        self.font = ImageFont.truetype(font_path, size=font_size)

    def _make_grapheme_panel_image(self, grapheme: str, always_draw_emoji: bool=False) -> Image:
        image_file = _image_filepath_for_grapheme(grapheme)

        try: 
            image = Image.open(image_file)
            image = image.convert('RGB')
        except FileNotFoundError as e:
            r = random.randint(0,255)
            g = random.randint(0,255)
            b = random.randint(0,255)
            text_color = (r,g,b)

            image = self._draw_panel_image(grapheme, self.font, text_color)

        return image

    def _draw_panel_image(self, character: str, font: ImageFont, text_color: tuple[int,int,int]):
        panel_width = self.display.panel_width()
        panel_height = self.display.panel_height()
        
        image = Image.new("RGB", (panel_width, panel_height))
        draw = ImageDraw.Draw(image)

        text_width = draw.textlength(character, font=font)

        text_bbox = draw.textbbox((0, 0), character, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]


        x = (panel_width - text_width) // 2
        y = (panel_height - text_height) // 2

        draw.text((x, y), character, fill=text_color, font=font)

        return image
    
    def _display_image_from_panel_images(self, panel_images):
        num_panels = len(panel_images)

        if num_panels == 0:
            raise ValueError("panel_images is empty")

        panel_width = self.display.panel_width()
        panel_height = self.display.panel_height()
        

        display_image = Image.new("RGB", (num_panels * panel_width, panel_height))

        current_x = 0

        for panel_image in panel_images:
            # All panel are scaled to the panel width, but some may need to be adjusted for height
            image_width, image_height = panel_image.size
            y = (panel_height - image_height) // 2

            display_image.paste(panel_image, (current_x, y))
            current_x += panel_width

        return display_image


    def make_panel_image_for_message(self, message: str, always_draw_emoji: bool=False):
        panel_images = [self._make_grapheme_panel_image(g, always_draw_emoji) for g in message]
        display_image = self._display_image_from_panel_images(panel_images)

        return display_image