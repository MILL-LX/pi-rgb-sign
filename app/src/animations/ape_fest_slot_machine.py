import logging
import random
import time

from animations.base_animation import BaseAnimation
from display import Display
import util.emoji
import util.words


logger = logging.getLogger(__name__)


##############################################################
# Configuration Constants
##############################################################
_HAPPY_WORDS_PATH = 'data/slot-machine/happy_words.txt'
_WINNING_WORDS_PATH = 'data/slot-machine/winning_words.txt'

class ApeFestSlotMachine(BaseAnimation):
    def __init__(self, display: Display) -> None:
        super().__init__(display)

        self.words = util.words.load_words(_HAPPY_WORDS_PATH)
        self.display_images_for_words = self.make_display_images_for_words(self.words)

        self.winning_words = util.words.load_words(_WINNING_WORDS_PATH)

    def make_display_images_for_words(self, words: list[str], always_draw_emoji: bool=False):
        display_images = {}
        for word in words:
            if not display_images.get(word):
                panel_image = self.display_image_generator.make_panel_image_for_message(word, always_draw_emoji)
                display_images[word] = panel_image

        return display_images

    async def run(self, iterations: int=20, always_draw_emoji: bool=False, **kwargs):
        self.display.clear()

        always_draw_emoji = isinstance(always_draw_emoji, str) and 'true' == always_draw_emoji.lower()
        iterations = int(iterations)

        num_emoji_quartets = iterations // 2
        num_words_for_turn = iterations - num_emoji_quartets

        turn_words = random.sample(self.words, num_words_for_turn)
        final_word = turn_words[-1]

        emoji_quartets = util.emoji.make_random_quartets(num_emoji_quartets)
        turn_words.extend(emoji_quartets)    

        random.shuffle(turn_words)

        turn_display_images = self.make_display_images_for_words(turn_words, always_draw_emoji)
        final_display_image = turn_display_images[final_word]
        
        for display_image in turn_display_images.values():
            self.display.setImage(display_image, x_offset=0, y_offset=0)
            time.sleep(0.1)

        self.display.setImage(final_display_image, x_offset=0, y_offset=0)

        flash_delay = 0.08
        if final_word in self.winning_words:
            time.sleep(flash_delay)
            for flash_color in [(255,0,0),(0,255,0),(0,0,255),(255,255,255)] * 5:
                self.display.fill(flash_color)
                time.sleep(flash_delay)
                self.display.setImage(final_display_image, x_offset=0, y_offset=0)
                time.sleep(flash_delay)

