import random

from PIL import Image, ImageDraw, ImageFont
from uniseg.graphemecluster import grapheme_clusters

from display import Display
import util.emoji

##############################################################
# Configuration Constants
##############################################################
EMOJI_GLYPHS_PATH = 'assets/emoji_glyphs/32x32'

def grapheme_string_prefix(string, prefix_length):
    return ''.join(_graphemes_from_message(string)[:prefix_length])

def _graphemes_from_message(message):
    return list(grapheme_clusters(message))

def _grapheme_to_hex(grapheme: str) -> str:
    hex_codes = [hex(ord(c)).replace('0x', '') for c in grapheme]
    return '-'.join(hex_codes)

def _image_filepath_for_grapheme(grapheme: str) -> str:
    hex_code = _grapheme_to_hex(grapheme)
    return f'{EMOJI_GLYPHS_PATH}/{hex_code}.png'

class DisplayImageGenerator:
    def __init__(self, display: Display, word_font_path: str, emoji_font_path: str) -> None:
        self.display = display

        font_size = min(self.display.panel_width(), self.display.panel_height())
        self.word_font = ImageFont.truetype(word_font_path, size=font_size)
        self.emoji_font = ImageFont.truetype(emoji_font_path, size=font_size)

    def _make_grapheme_panel_image(self, grapheme: str, always_draw_emoji: bool=False, text_color: tuple[int,int,int]=None, background_color: tuple[int,int,int]=None) -> Image:
        try_using_glyph = not always_draw_emoji

        grapheme_panel_image = None
        if try_using_glyph and util.emoji.is_glyph_emoji(grapheme):
            try: 
                glyph_file_path = _image_filepath_for_grapheme(grapheme)
                glyph_image = Image.open(glyph_file_path)
                grapheme_panel_image = glyph_image.convert('RGB')
            except FileNotFoundError as e:
                grapheme_panel_image = None

        if not grapheme_panel_image:
            if not text_color:
                r = random.randint(128,255)
                g = random.randint(128,255)
                b = random.randint(128,255)
                text_color = (r,g,b)

            if not background_color:
                background_color = (0,0,0)

            grapheme_is_emoji = util.emoji.is_emoji(grapheme)
            grapheme_font = self.emoji_font if grapheme_is_emoji else self.word_font

            grapheme = grapheme[0] # multi-character emoji sometimes don't render correctly
            grapheme_panel_image = self._draw_panel_image(grapheme, grapheme_font, text_color, background_color)

        return grapheme_panel_image

    def _draw_panel_image(self, grapheme: str, font: ImageFont, text_color: tuple[int,int,int], background_color: tuple[int,int,int]):
        panel_width = self.display.panel_width()
        panel_height = self.display.panel_height()
        
        image = Image.new("RGB", (panel_width, panel_height), background_color)
        draw = ImageDraw.Draw(image)

        text_bbox = draw.textbbox((0, 0), grapheme, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]


        x = (panel_width - text_width) // 2
        y = (panel_height - text_height) // 2

        draw.text((x, y), grapheme, fill=text_color, font=font)

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


    def make_display_image_for_message(self, message: str, always_draw_emoji: bool=False, alternating_monochrome: bool=False):
        panel_images = []
        for i, g in enumerate(_graphemes_from_message(message)):
            if alternating_monochrome:
                background_color = (0, 0, 0) if i % 2 == 0 else (255, 255, 255)
                text_color = (255, 255, 255) if i % 2 == 0 else (0, 0, 0)
            else:
                background_color = None
                text_color = None

            panel_image = self._make_grapheme_panel_image(g, always_draw_emoji, text_color, background_color)
            panel_images.append(panel_image)

        display_image = self._display_image_from_panel_images(panel_images)

        return display_image