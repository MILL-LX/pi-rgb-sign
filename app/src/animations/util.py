import importlib.util
import inspect
import logging
import os

from app.src.animations.animation import Animation

logger = logging.getLogger(__name__)

def register_animations(animation_dir, display):
    logger.info('Registering animations...')
    animations = {}
    for file_name in os.listdir(animation_dir):
        if file_name.endswith('.py'):
            module_name = file_name[:-3]  # Remove '.py' extension
            spec = importlib.util.spec_from_file_location(module_name, os.path.join(animation_dir, file_name))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            for name, obj in module.__dict__.items():
                if isinstance(obj, type) and issubclass(obj, Animation) and obj is not Animation:
                    animations[name] = obj(display)
    logger.info(f'Registered animations: {", ".join(animations.keys())}')
    return animations

def describe_animation(animation ):
    class_type = type(animation)
    method_name = 'run'
    method = getattr(animation, 'run', None)
    if not method:
        raise(ValueError(f'Method "{method_name}" not found in {class_type.__name__}.'))
    
    # Get the signature of the method
    signature = inspect.signature(method)
    return f'{method_name}{signature}'

