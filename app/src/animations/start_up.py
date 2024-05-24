import logging
import time

from animations.base_animation import BaseAnimation
from util import image_util, pi_util


logger =  logging.getLogger(__name__)

class Startup(BaseAnimation):
    def __init__(self, display) -> None:
        super().__init__(display)
        self.animation_name = self.__class__
        self.display = display

    async def run(self, seconds:int=0, check_network:bool=False, **kwargs):
        panel_images = image_util.test_images_for_display(self.display) # TODO - replace with a call to generate panels for each animation frame      


        logger.info(f'Running startup animation for {seconds} seconds, check_network={check_network}')
        start_time = time.time()
        while True:
            display_image = image_util.display_image_from_panel_images(panel_images)
            self.display.setImage(display_image, x_offset=0, y_offset=0)

            # Rotate the array of panel images
            panel_images = panel_images[-1:] + panel_images[:-1]
            time.sleep(0.1)

            # We stop if we are checking for a network connection and we have one.
            # Otherwise, we respect the time limit and stop if the specified seconds have elapsed.
            if check_network and pi_util.has_active_network_interface():
                logger.info('Stopping becasue network found, or not checked when not on a Pi')
                return
            elif seconds > 0:
                elapsed = time.time() - start_time
                if elapsed > seconds:
                    if check_network:
                        logger.error(f'Failed to find an active network interface in the {seconds} seconds allotted.')
                    else:
                        logger.info('Stopping after {elapsed} of {seconds} seconds.')
                    return
