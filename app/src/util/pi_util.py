import logging
import subprocess

logger = logging.getLogger(__name__)

def is_raspberry_pi():
    try:
        with open('/sys/firmware/devicetree/base/model', 'r') as f:
            model = f.read()
            if 'Raspberry Pi' in model:
                logger.info(f'We are running on a Raspbery Pi {model}')
                return True
    except FileNotFoundError:
        pass

    return False

def has_active_network_interface():
    if not is_raspberry_pi():
        return True
    
    try:
        # Run 'ip' command to list network interfaces
        result = subprocess.run(['ip', 'link', 'show'], capture_output=True, text=True)

        # Check if the command succeeded and if there's any network interface listed
        return result.returncode == 0 and len(result.stdout.strip()) > 0
    except Exception as e:
        logger.error(f'Error checking for active network interface: {e}')
        return False