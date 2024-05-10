import importlib.util
import os

from animations.base_animation import BaseAnimation

def register_animations(animation_dir, display):
    animations = {}
    for file_name in os.listdir(animation_dir):
        if file_name.endswith('.py'):
            module_name = file_name[:-3]  # Remove '.py' extension
            spec = importlib.util.spec_from_file_location(module_name, os.path.join(animation_dir, file_name))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            for name, obj in module.__dict__.items():
                if isinstance(obj, type) and issubclass(obj, BaseAnimation) and obj is not BaseAnimation:
                    animations[name] = obj(display)
    return animations
