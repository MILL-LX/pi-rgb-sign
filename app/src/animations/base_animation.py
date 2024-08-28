import logging

logger = logging.getLogger(__name__)

class BaseAnimation:
    def __init__(self, display) -> None:
        self.display = display
        self.animation_name = self.__class__.__name__
        logger.info(f'Making a {self.animation_name} animation for a display with {display.num_panels} panels.')

    def run(self):
        raise NotImplementedError("Subclasses must implement 'run' method")
