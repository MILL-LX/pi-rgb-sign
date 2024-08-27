import logging
import time

from animations.base_animation import BaseAnimation
from display import Display
from display_image_generator import DisplayImageGenerator

logger = logging.getLogger(__name__)

##############################################################
# Configuration Constants
##############################################################
_FONT_PATH = 'assets/fonts/MILL/Canada Type - Screener SC.ttf'

class ShowMessage(BaseAnimation):
    def __init__(self, display: Display, font_path=_FONT_PATH) -> None:
        super().__init__(display)

        logger.info(f'Making a ShowMessage animation for a display with {display.num_panels} panels.')
        self.display = display
        self.font_path = font_path

        self.display_image_generator = DisplayImageGenerator(self.display, self.font_path)

    
    async def run(self, message, **kwargs):
        self.display.clear()

        display_image = self.display_image_generator.make_panel_image_for_message(message)
        self.display.setImage(display_image, x_offset=0, y_offset=0)
        time.sleep(0.5)

        flash_delay = 0.08
        time.sleep(flash_delay)
        for flash_color in [(255,0,0),(0,255,0),(0,0,255),(255,255,255)] * 5:
            self.display.fill(flash_color)
            time.sleep(flash_delay)
            self.display.setImage(display_image, x_offset=0, y_offset=0)
            time.sleep(flash_delay)



