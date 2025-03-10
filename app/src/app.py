import argparse
import asyncio
import logging
import os
import sys

# configure logging for the app
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()  # Log to the console
    ]
)

# Get our logger
logger = logging.getLogger(__name__)

# Look for modules and packages in our application directory
program_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(program_dir)

from display import Display
from animations import util
from web.web_app import WebApp


def parse_arguments():
    parser = argparse.ArgumentParser(description="Raspberry Pi Smart LED Matrix Sign")
    parser.add_argument("--test-display", action="store_true", help="Test the display panel")
    parser.add_argument("--smart-sign", action="store_true", help="Run the smart sign web app")
    parser.add_argument("--num-panels", type=int, default=4, help="number of display panels")
    return parser.parse_args()

def main():
    args = parse_arguments()

    display = Display(args.num_panels)
    animation_dir = os.path.join(program_dir, 'animations')
    animations = util.register_animations(animation_dir, display)

    startup_animation = animations['Startup']

    if args.test_display: 
        startup_animation.run()
    elif args.smart_sign:
        startup_animation.run(seconds=10, check_network=True)
        web_app = WebApp(animations)
        web_app.run()
    else:
        logger.error('No application mode specified, exiting... KThXBye')

if __name__ == "__main__":
    logger.info(f'Starting Raspberry Pi Smart LED Matrix Sign')
    main()