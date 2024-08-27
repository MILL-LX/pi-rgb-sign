import logging
import random
import time

from animations.base_animation import BaseAnimation
from display import Display
from display_image_generator import DisplayImageGenerator
from util import emoji, words

logger = logging.getLogger(__name__)


##############################################################
# Configuration Constants
##############################################################
_FONT_PATH = 'assets/fonts/MILL/Canada Type - Screener SC.ttf'

class SlotMachineV2(BaseAnimation):
    def __init__(self, display: Display, font_path=_FONT_PATH) -> None:
        super().__init__(display)

        logger.info(f'Making a SlotMachineV2 for a display with {display.num_panels} panels.')
        self.display = display
        self.font_path = font_path

        self.display_image_generator = DisplayImageGenerator(self.display, self.font_path)

        self.words = words.load_words('data/slot-machine//happy_words.txt')
        self.display_images_for_words = self.make_display_images_for_words()

        self.winning_words = words.load_words('data/slot-machine/winning_words.txt')

    def make_display_images_for_words(self):
        words = self.words[:]

        words_to_emoji_ratio = len(self.words) // (len(emoji.emoji_list) // self.display.num_panels)
        shuffled_emoji = emoji.emoji_list[:] * words_to_emoji_ratio
        random.shuffle(shuffled_emoji)
        emoji_quartets = [''.join(shuffled_emoji[i:i+4]) for i in range(0, len(shuffled_emoji), self.display.num_panels)]

        words.extend(emoji_quartets)

        random.shuffle(words)

        display_images = {}
        for word in words:
            if not display_images.get(word):
                panel_image = self.display_image_generator.make_panel_image_for_message(word)
                display_images[word] = panel_image

        return display_images

    async def run(self, **kwargs):
        self.display.clear()

        final_word_index = random.randint(0, len(self.words) - 1)
        final_word = self.words[final_word_index]
        final_display_image = self.display_images_for_words[final_word]

        display_images = list(self.display_images_for_words.values())
        random.shuffle(display_images)

        iterations = min(100, len(self.display_images_for_words))
        for display_image in display_images[:iterations]:
            self.display.setImage(display_image, x_offset=0, y_offset=0)
            time.sleep(0.1)
        self.display.setImage(final_display_image, x_offset=0, y_offset=0)

        # DEBUG - test by always adding the current word to the winning word list
        # self.winning_words.append(final_word)

        flash_delay = 0.08
        if final_word in self.winning_words:
            time.sleep(flash_delay)
            for flash_color in [(255,0,0),(0,255,0),(0,0,255),(255,255,255)] * 5:
                self.display.fill(flash_color)
                time.sleep(flash_delay)
                self.display.setImage(final_display_image, x_offset=0, y_offset=0)
                time.sleep(flash_delay)

        self.display.setImage(final_display_image, x_offset=0, y_offset=0)
