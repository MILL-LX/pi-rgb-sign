import logging
import time

from animations.animation import Animation
from display import Display
from display_image_generator import grapheme_string_prefix

logger = logging.getLogger(__name__)

def format_mmss(total_seconds: int) -> str:
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes:02d}{seconds:02d}"

class CountdownTimer(Animation):
    def __init__(self, display: Display) -> None:
        super().__init__(display)

    def run(self, duration_minutes: int="5", finish: str="over", **kwargs):

        max_time = int(duration_minutes) * 60
        current_time = max_time

        # run countdown:
        for current_time in range(max_time, -1, -1):
            time_string = format_mmss(current_time)
            display_image = self.display_image_generator.make_display_image_for_message(time_string)
            self.display.setImage(display_image, x_offset=0, y_offset=0)
            time.sleep(1)

        # show finish:
        finish_image = self.display_image_generator.make_display_image_for_message("0000")

        # finish animation:
        flash_delay = 0.08
        time.sleep(flash_delay)
        for flash_color in [(255,0,0),(0,255,0),(0,0,255),(255,255,255)] * 5:
            self.display.fill(flash_color)
            time.sleep(flash_delay)
            self.display.setImage(finish_image, x_offset=0, y_offset=0)
            time.sleep(flash_delay)
