import logging

from display import Display
from display_image_generator import DisplayImageGenerator

logger = logging.getLogger(__name__)

##############################################################
# Configuration Constants
##############################################################
_WORD_FONT_PATH = 'assets/fonts/MILL/Canada Type - Screener SC.ttf'
_EMOJI_FONT_PATH = 'assets/fonts/Noto_Emoji/static/NotoEmoji-Medium.ttf'
#_EMOJI_FONT_PATH = 'assets/fonts/TwitterColorEmoji-SVGinOT-14.0.2/TwitterColorEmoji-SVGinOT.ttf'

class BaseAnimation:
    def __init__(self, display, word_font_path=_WORD_FONT_PATH, emoji_font_path=_EMOJI_FONT_PATH) -> None:
        self.display = display
        self.animation_name = self.__class__.__name__
        logger.info(f'Making a {self.animation_name} animation for a display with {display.num_panels} panels.')


        self.word_font_path = word_font_path
        self.emoji_font_path = emoji_font_path
        self.display_image_generator = DisplayImageGenerator(self.display, self.word_font_path, self.emoji_font_path)

    def run(self):
        raise NotImplementedError("Subclasses must implement 'run' method")
