import logging
import time

from app.src.animations.animation import Animation
from util.image_util import test_panel_images_for_display, display_image_from_panel_images
from util import pi_util


logger =  logging.getLogger(__name__)

class Startup(Animation):
    def __init__(self, display) -> None:
        super().__init__(display)

    async def run(self, seconds:int=0, check_network:bool=False, **kwargs):
        panel_images = test_panel_images_for_display(self.display)

        logger.info(f'Running startup animation for {seconds} seconds, check_network={check_network}')
        start_time = time.time()
        while True:
            display_image = display_image_from_panel_images(panel_images)
            self.display.setImage(display_image, x_offset=0, y_offset=0)

            # Rotate the array of panel images
            panel_images = panel_images[-1:] + panel_images[:-1]
            time.sleep(0.1)

            # We stop if we are checking for a network connection and we have one.
            # Otherwise, we respect the time limit and stop if the specified seconds have elapsed.
            if check_network and pi_util.has_active_network_interface():
                logger.info('Stopping because network found, or not checked when not on a Pi')
                return
            elif seconds > 0:
                elapsed = time.time() - start_time
                if elapsed > seconds:
                    if check_network:
                        logger.error(f'Failed to find an active network interface in the {seconds} seconds allotted.')
                    else:
                        logger.info('Stopping after {elapsed} of {seconds} seconds.')
                    return
