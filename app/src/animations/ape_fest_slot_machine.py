import logging
import random
import time
import os

from PIL import Image, ImageOps

from animations.base_animation import BaseAnimation
from display import Display
from util.image_util import load_image, display_image_from_panel_images
from util.pi_util import is_raspberry_pi
# from util.print_util import print_file


logger = logging.getLogger(__name__)


##############################################################
# Configuration Constants
##############################################################
_IMAGE_DIRECTORY_PATH = '/mnt/slot-machine-data/images/ape-fest' if is_raspberry_pi() else 'assets/images/ape-fest'
_PANEL_IMAGE_DIRECTORY_PATH = f'{_IMAGE_DIRECTORY_PATH}/panels'
_LOGO_IMAGE_DIRECTORY_PATH = f'{_IMAGE_DIRECTORY_PATH}/logos'

_GAME_DISPLAY_SECONDS = 5
_PANEL_DISPLAY_SECONDS = 0.1
_WINNING_PANEL_ANIMATION_DISPLAY_SECONDS = 5
_LOSER_MESSAGE_DISPLAY_SECONDS = 5
_LOGO_DISPLAY_SECONDS = 3

##############################################################
# Helper Functions
##############################################################
def _image_file_paths_from_directory(directory_path: str) -> list[str]:
    excluded_filenames = {'.DS_Store'}
    return [
        os.path.join(root, file)
        for root, _, files in os.walk(directory_path)
        for file in files
        if not file.startswith('.') and file not in excluded_filenames
    ]

def _select_random_image_files_from_directory(directory_path: str, num_images: int) -> list[str]:
    image_file_paths = _image_file_paths_from_directory(directory_path)
    return random.choices(image_file_paths, k=num_images) 

def _load_images_for_file_paths(image_file_paths: list[str], image_size: tuple[int, int]) -> list[Image.Image]:
    return [load_image(image_file_path, image_size) for image_file_path in image_file_paths]

def _load_images_from_directory(directory_path: str, image_size: tuple[int, int] = None) -> list[Image.Image]:
    image_file_paths = _image_file_paths_from_directory(directory_path)
    return _load_images_for_file_paths(image_file_paths, image_size)   

class ApeFestSlotMachine(BaseAnimation):
    def __init__(self, display: Display) -> None:
        super().__init__(display)

        self.logo_images = _load_images_from_directory(_LOGO_IMAGE_DIRECTORY_PATH, self.display.size())   
        self.panel_image_file_paths = _image_file_paths_from_directory(_PANEL_IMAGE_DIRECTORY_PATH)    

        self.game_display_seconds = _GAME_DISPLAY_SECONDS
        self.panel_display_seconds = _PANEL_DISPLAY_SECONDS
        self.winning_panel_animation_display_seconds = _WINNING_PANEL_ANIMATION_DISPLAY_SECONDS
        self.logo_display_seconds = _LOGO_DISPLAY_SECONDS
        self.loser_message_display_seconds = _LOSER_MESSAGE_DISPLAY_SECONDS

        self.last_win_time = time.time() # start by assuming that the game was just won


    def _is_winning_turn(self) -> bool:
        win_probability = 0.2
        max_win_probability = 0.75
        win_probability_double_seconds = 60

        # double the win probability every win_probability_double_seconds since the last win, up to max_win_probability
        time_since_last_win = time.time() - self.last_win_time  
        win_probability *= 2 ** int(time_since_last_win / win_probability_double_seconds) # 60 seconds = 1 minute
        win_probability = min(win_probability, max_win_probability) # cap at max_win_probability

        win = random.random() < win_probability

        if win:
            self.last_win_time = time.time()

        return win

    def _show_winning_panel_animation(self, winning_panel_image: Image.Image):
        # Show an alternating pattern of the winning panel image and its inverse
        inverse_winning_panel_image = ImageOps.invert(winning_panel_image)
        start_time = time.time()
        i = 0
        while time.time() - start_time < self.winning_panel_animation_display_seconds:
            self.display.setImage(winning_panel_image if i % 2 == 0 else inverse_winning_panel_image, x_offset=0, y_offset=0)
            time.sleep(self.panel_display_seconds) 
            i += 1

    def _show_losing_panel_animation(self):
        display_image = self.display_image_generator.make_display_image_for_message('awaiting goop')
        display_image_width, display_image_height = display_image.size
        for repetitions in range(1):
            x = self.display.width()
            while x > -display_image_width + self.display.width(): 
                x -= self.display.panel_width() // 8
                self.display.setImage(display_image, x_offset=x, y_offset=0)
                time.sleep(0.05)


        possible_loser_messages = ['LUSR', 'HODL', 'FOMO', 'FORK']
        loser_message = random.choice(possible_loser_messages)
        loser_image = self.display_image_generator.make_display_image_for_message(loser_message, alternating_monochrome=True)
        self.display.setImage(loser_image, x_offset=0, y_offset=0)
        time.sleep(self.loser_message_display_seconds)

    def _show_logo_images(self, display_image: Image.Image):
        logo_display_image = display_image_from_panel_images(random.sample(self.logo_images, self.display.num_panels))
        self.display.setImage(logo_display_image, x_offset=0, y_offset=0)

        time.sleep(self.logo_display_seconds)

        self.display.setImage(display_image, x_offset=0, y_offset=0)

    async def run(self, **kwargs):
        self.display.clear()

        # have enough display images to fill the game display time if we display each image for the panel display time
        num_display_images = int(self.game_display_seconds / self.panel_display_seconds)
        num_panel_images = self.display.num_panels * num_display_images
        random_file_paths = [self.panel_image_file_paths[random.randint(0, len(self.panel_image_file_paths) - 1)] for _ in range(num_panel_images)]
        panel_images = _load_images_for_file_paths(random_file_paths, self.display.size())
        
        display_images = [display_image_from_panel_images(panel_images[i:i+4]) for i in range(0, len(panel_images), 4)]

        # display the game  
        display_image = None
        turn_start_time = time.time()
        while time.time() - turn_start_time < self.game_display_seconds:
            display_image_index = random.randint(0, len(display_images) - 1) # sample with replacement - we're happy if the same image is displayed multiple times
            display_image = display_images[display_image_index]
            self.display.setImage(display_image, x_offset=0, y_offset=0)
            time.sleep(self.panel_display_seconds)

        if self._is_winning_turn():
            self._show_winning_panel_animation(display_image)
        else:
            self._show_losing_panel_animation()

        self._show_logo_images(display_image)
