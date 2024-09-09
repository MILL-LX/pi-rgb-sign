import logging
import time

from animations.base_animation import BaseAnimation
from display import Display
from display_image_generator import grapheme_string_prefix

logger = logging.getLogger(__name__)


class ShowMessage(BaseAnimation):
    def __init__(self, display: Display) -> None:
        super().__init__(display)

    async def run(self, message: str, finish: str=None, **kwargs):
        finish = grapheme_string_prefix(message, 4) if not finish else finish

        self.display.clear()

        display_image = self.display_image_generator.make_display_image_for_message(message)
        finish_image = self.display_image_generator.make_display_image_for_message(finish)
        display_image_width, display_image_height = display_image.size

        for repetitions in range(1):
            x = self.display.width()
            while x > -display_image_width + self.display.width(): 
                x -= self.display.panel_width() // 8
                self.display.setImage(display_image, x_offset=x, y_offset=0)
                time.sleep(0.05)


        flash_delay = 0.08
        time.sleep(flash_delay)
        for flash_color in [(255,0,0),(0,255,0),(0,0,255),(255,255,255)] * 5:
            self.display.fill(flash_color)
            time.sleep(flash_delay)
            self.display.setImage(finish_image, x_offset=0, y_offset=0)
            time.sleep(flash_delay)



