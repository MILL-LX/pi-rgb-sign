import logging
import random
import time
import os

from PIL import Image

from animations.base_animation import BaseAnimation
from display import Display
from util.image_util import load_image, display_image_from_panel_images
from util.pi_util import is_raspberry_pi


logger = logging.getLogger(__name__)


##############################################################
# Configuration Constants
##############################################################
_IMAGE_DIRECTORY_PATH = '/mnt/slot-machine-data/images' if is_raspberry_pi() else 'assets/images/ape-fest'
_PANEL_IMAGE_DIRECTORY_PATH = f'{_IMAGE_DIRECTORY_PATH}/panels'
_LOGO_IMAGE_DIRECTORY_PATH = f'{_IMAGE_DIRECTORY_PATH}/logos'

_GAME_DISPLAY_TIME = 5
_PANEL_DISPLAY_TIME = 0.1

##############################################################
# Helper Functions
##############################################################
def _select_random_images_files_from_directory(directory_path: str, num_images: int) -> list[str]:
    image_file_paths = [os.path.join(directory_path, file) for file in os.listdir(directory_path)]
    return random.choices(image_file_paths, k=num_images) 

def _load_images_for_file_paths(image_file_paths: list[str], image_size: tuple[int, int]) -> list[Image.Image]:
    return [load_image(image_file_path, image_size) for image_file_path in image_file_paths]

def _load_images_from_directory(directory_path: str, image_size: tuple[int, int] = None) -> list[Image.Image]:
    image_file_paths = [os.path.join(directory_path, file) for file in os.listdir(directory_path)]
    return _load_images_for_file_paths(image_file_paths, image_size)   

def _is_winning_turn(last_win_time: float) -> bool:
    return True

class ApeFestSlotMachine(BaseAnimation):
    def __init__(self, display: Display) -> None:
        super().__init__(display)

        self.logo_images = _load_images_from_directory(_LOGO_IMAGE_DIRECTORY_PATH, self.display.size())   
        self.panel_image_file_paths = [os.path.join(_PANEL_IMAGE_DIRECTORY_PATH, file) for file in os.listdir(_PANEL_IMAGE_DIRECTORY_PATH)]    

        self.game_display_time = _GAME_DISPLAY_TIME
        self.panel_display_time = _PANEL_DISPLAY_TIME

        self.last_win_time = time.time() # start by assuming that the game was just won

    def _show_winning_panel_animation(self):
        pass

    def _show_losing_panel_animation(self):
        pass 

    def _show_logo_images(self):
        logo_display_image = display_image_from_panel_images(random.sample(self.logo_images, self.display.num_panels))
        self.display.setImage(logo_display_image, x_offset=0, y_offset=0)

    async def run(self, **kwargs):
        self.display.clear()

        # have enough display images to fill the game display time if we display each image for the panel display time
        num_display_images = int(self.game_display_time / self.panel_display_time)
        num_panel_images = self.display.num_panels * num_display_images
        random_file_paths = [self.panel_image_file_paths[random.randint(0, len(self.panel_image_file_paths) - 1)] for _ in range(num_panel_images)]
        panel_images = _load_images_for_file_paths(random_file_paths, self.display.size())
        
        display_images = [display_image_from_panel_images(panel_images[i:i+4]) for i in range(0, len(panel_images), 4)]

        # display the game  
        turn_start_time = time.time()
        while time.time() - turn_start_time < self.game_display_time:
            display_image_index = random.randint(0, len(display_images) - 1) # sample with replacement - we're happy if the same image is displayed multiple times
            self.display.setImage(display_images[display_image_index], x_offset=0, y_offset=0)
            time.sleep(self.panel_display_time)

        if _is_winning_turn(self.last_win_time):
            self._show_winning_panel_animation()
            self.last_win_time = time.time()
        else:
            self._show_losing_panel_animation()

        self._show_logo_images()
