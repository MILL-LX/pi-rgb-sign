import threading
from flask import Flask, request, jsonify, render_template_string

class WebApp:
    def __init__(self, animations, host='0.0.0.0', port=80) -> None:
        self.animations = animations
        self.host = host
        self.port = port
        self.lock = threading.Lock()  # Add a lock to manage execution state

        self.app = Flask(__name__)
        self.add_routes()

    def descriptions_for_animations(self, url_prefix):
        urls = [f'{url_prefix}/animate/{animation.__class__.__name__}?arguments' for animation in self.animations.values()]
        descriptions = ''
        for url in urls:
            descriptions += f'\n<br><a href="{url}">{url}</a>'
        return descriptions

    def index(self):
        url_prefix = request.url_root.rstrip('/')
        response = f'''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Available Endpoints</title>
</head>
<body>
  <h1>Available Endpoints</h1>
  <p>{self.descriptions_for_animations(url_prefix)}</p>
</body>
</html>
'''
        return render_template_string(response)
    
    def run_animation(self, animation, args):
        animation.run(**args)
        self.lock.release()

    def animate(self, animation_name):
        animation = self.animations.get(animation_name)
        if not animation:
            return jsonify(status='error', message=f'Animation {animation_name} not found'), 404

        if not self.lock.acquire(blocking=False):
            return jsonify(status='error', message='Another animation is currently running. Please try again later.'), 429

        request_args = request.args.to_dict()
        threading.Thread(target=self.run_animation, args=(animation, request_args)).start()
        return jsonify(status='success', message=f'Animation {animation_name} started successfully')

    def add_routes(self):
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/animate/<animation_name>', 'animate', self.animate)

    def run(self):
        self.app.run(host=self.host, port=self.port)

