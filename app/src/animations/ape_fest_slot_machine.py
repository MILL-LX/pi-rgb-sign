import logging
import random
import time
import os

from PIL import Image, ImageOps

from animations.base_animation import BaseAnimation
from display import Display
from util.image_util import load_image, display_image_from_panel_images, load_animation_from_file
from util.pi_util import is_raspberry_pi
from util.print_util import print_file


logger = logging.getLogger(__name__)


##############################################################
# Configuration Constants
##############################################################
_IMAGE_DIRECTORY_PATH = '/mnt/slot-machine-data/images/apefest' if is_raspberry_pi() else 'assets/images/apefest'
_PANEL_IMAGE_DIRECTORY_PATH = f'{_IMAGE_DIRECTORY_PATH}/panels'
_LETTER_IMAGE_DIRECTORY_PATH = f'{_IMAGE_DIRECTORY_PATH}/letter_panels'
_LOGO_IMAGE_DIRECTORY_PATH = f'{_IMAGE_DIRECTORY_PATH}/logos'
_LOSING_PANEL_ANIMATION_FILE_PATH = f'{_IMAGE_DIRECTORY_PATH}/panel_animated_gifs/drip_A.gif'
_LOSING_DISPLAY_ANIMATION_DIRECTORY_PATH = f'{_IMAGE_DIRECTORY_PATH}/display_animated_gifs'
_PRINTER_IMAGE_DIRECTORY_PATH = f'{_IMAGE_DIRECTORY_PATH}/printer'
_LOSING_TICKET_IMAGES_DIRECTORY_PATH = f'{_PRINTER_IMAGE_DIRECTORY_PATH}/loser_tickets'
_WINNING_TICKET_IMAGES_DIRECTORY_PATH = f'{_PRINTER_IMAGE_DIRECTORY_PATH}/winner_tickets'
_USE_PRINTER_FLAG_FILE_PATH = f'{_PRINTER_IMAGE_DIRECTORY_PATH}/use_printer'

_GAME_DISPLAY_SECONDS = 5
_PANEL_DISPLAY_SECONDS = 0.1
_FINAL_IMAGE_DISPLAY_SECONDS = 3
_WINNING_PANEL_ANIMATION_DISPLAY_SECONDS = 5
_LOSING_PANEL_ANIMATION_DISPLAY_SECONDS = 5
_LOSER_MESSAGE_DISPLAY_SECONDS = 5
_LOGO_DISPLAY_SECONDS = 3

_STARTING_WIN_PROBABILITY = 0.2

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

        self.logo_images = _load_images_from_directory(_LOGO_IMAGE_DIRECTORY_PATH, self.display.panel_size())   
        self.panel_image_file_paths = _image_file_paths_from_directory(_PANEL_IMAGE_DIRECTORY_PATH)    
        self.losing_panel_animation_images, self.losing_panel_animation_fps = load_animation_from_file(_LOSING_PANEL_ANIMATION_FILE_PATH, self.display.panel_size())

        self.losing_display_animation_images = []
        for losing_panel_animation_image in self.losing_panel_animation_images:
            self.losing_display_animation_images.append(display_image_from_panel_images([losing_panel_animation_image for _ in range(self.display.num_panels)]))

        self.game_display_seconds = _GAME_DISPLAY_SECONDS
        self.panel_display_seconds = _PANEL_DISPLAY_SECONDS
        self.winning_panel_animation_display_seconds = _WINNING_PANEL_ANIMATION_DISPLAY_SECONDS
        self.losing_panel_animation_display_seconds = _LOSING_PANEL_ANIMATION_DISPLAY_SECONDS
        self.logo_display_seconds = _LOGO_DISPLAY_SECONDS
        self.loser_message_display_seconds = _LOSER_MESSAGE_DISPLAY_SECONDS

        self.last_win_time = time.time() # start by assuming that the game was just won

        self.use_printer = os.path.exists(_USE_PRINTER_FLAG_FILE_PATH)

    def _is_winning_turn(self) -> bool:
        win_probability = _STARTING_WIN_PROBABILITY
        max_win_probability = 0.75
        win_probability_double_seconds = 90

        # double the win probability every win_probability_double_seconds since the last win, up to max_win_probability
        time_since_last_win = time.time() - self.last_win_time  
        win_probability *= 2 ** int(time_since_last_win / win_probability_double_seconds) # 60 seconds = 1 minute
        win_probability = min(win_probability, max_win_probability) # cap at max_win_probability

        win = random.random() < win_probability

        if win:
            self.last_win_time = time.time()
            win_probability = _STARTING_WIN_PROBABILITY

        return win

    def _show_winning_panel_animation(self, winning_panel_image: Image.Image, alternate_winning_panel_image: Image.Image=None):
        alternate_winning_panel_image = ImageOps.invert(winning_panel_image) if alternate_winning_panel_image is None else alternate_winning_panel_image
        
        start_time = time.time()
        i = 0
        while time.time() - start_time < self.winning_panel_animation_display_seconds:
            self.display.setImage(winning_panel_image if i % 2 == 0 else alternate_winning_panel_image, x_offset=0, y_offset=0)
            time.sleep(self.panel_display_seconds) 
            i += 1

    def _show_losing_panel_animation(self):
        start_time = time.time()
        i = 0
        while time.time() - start_time < self.losing_panel_animation_display_seconds:
            self.display.setImage(self.losing_display_animation_images[i % len(self.losing_display_animation_images)], x_offset=0, y_offset=0)
            time.sleep(1/self.losing_panel_animation_fps) 
            i += 1

        # possible_loser_messages = ['LOSR', 'HODL', 'FOMO', 'FORK']
        # loser_message = random.choice(possible_loser_messages)
        # letter_images = []
        # for letter in loser_message:
        #     letter_image_file_path = os.path.join(_LETTER_IMAGE_DIRECTORY_PATH, f'{letter}.png')
        #     background_color = (random.randint(100, 200), random.randint(100, 200), random.randint(100, 200), 255)
        #     letter_image = load_image(letter_image_file_path, self.display.panelsize(), background_color)
        #     letter_images.append(letter_image)
        # loser_image = display_image_from_panel_images(letter_images)
        try:
            random_loser_message_animation_file_path = _select_random_image_files_from_directory(_LOSING_DISPLAY_ANIMATION_DIRECTORY_PATH, 1)[0]
            loser_message_animation_frames, loser_message_animation_fps = load_animation_from_file(random_loser_message_animation_file_path, self.display.size())
            for loser_message_animation_frame in loser_message_animation_frames:
                self.display.setImage(loser_message_animation_frame, x_offset=0, y_offset=0)
                time.sleep(1/loser_message_animation_fps) 
        except Exception as e:
            logger.error(f'Error showing losing panel animation: {e}')


    def _show_logo_images(self, display_image: Image.Image):
        logo_panel_image = random.choice(self.logo_images)
        logo_display_image = display_image_from_panel_images([logo_panel_image for _ in range(self.display.num_panels)])
        self.display.setImage(logo_display_image, x_offset=0, y_offset=0)

        time.sleep(self.logo_display_seconds)

        self.display.setImage(display_image, x_offset=0, y_offset=0)

    async def run(self, **kwargs):
        self.display.clear()

        # have enough display images to fill the game display time if we display each image for the panel display time
        num_display_images = int(self.game_display_seconds / self.panel_display_seconds)
        num_panel_images = self.display.num_panels * num_display_images
        random_file_paths = [self.panel_image_file_paths[random.randint(0, len(self.panel_image_file_paths) - 1)] for _ in range(num_panel_images)]
        panel_images = _load_images_for_file_paths(random_file_paths, self.display.panel_size())
        
        display_images = [display_image_from_panel_images(panel_images[i:i+4]) for i in range(0, len(panel_images), 4)]

        # display the game  
        display_image = None
        turn_start_time = time.time()
        while time.time() - turn_start_time < self.game_display_seconds:
            display_image_index = random.randint(0, len(display_images) - 1) # sample with replacement - we're happy if the same image is displayed multiple times
            display_image = display_images[display_image_index]
            self.display.setImage(display_image, x_offset=0, y_offset=0)
            time.sleep(self.panel_display_seconds)

        win = self._is_winning_turn()

        alternate_winning_display_image = None
        if win:
            winning_panel_image_file_path = _select_random_image_files_from_directory(_PANEL_IMAGE_DIRECTORY_PATH, 1)[0]
            winning_panel_image_background_color = (127, 0, 0, 255)
            winning_panel_image = load_image(winning_panel_image_file_path, self.display.panel_size(), winning_panel_image_background_color )
            display_image = display_image_from_panel_images([winning_panel_image for _ in range(self.display.num_panels)])

            alternate_winning_panel_image = ImageOps.invert(winning_panel_image)
            alternate_winning_panel_image_background_color = (0, 0, 127, 255)
            alternate_winning_panel_image = load_image(winning_panel_image_file_path, self.display.panel_size(), alternate_winning_panel_image_background_color )
            alternate_winning_display_image = display_image_from_panel_images([alternate_winning_panel_image for _ in range(self.display.num_panels)])

            self.display.setImage(display_image, x_offset=0, y_offset=0)

        time.sleep(_FINAL_IMAGE_DISPLAY_SECONDS)


        if win:
            prize_image_file_path = _select_random_image_files_from_directory(_WINNING_TICKET_IMAGES_DIRECTORY_PATH, 1)[0]
            self._show_winning_panel_animation(display_image)
        else:
            prize_image_file_path = _select_random_image_files_from_directory(_LOSING_TICKET_IMAGES_DIRECTORY_PATH, 1)[0]
            self._show_losing_panel_animation()
            
        self._show_logo_images(display_image)

        print_file(prize_image_file_path, self.use_printer)
