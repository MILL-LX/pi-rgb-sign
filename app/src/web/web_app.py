import asyncio
import inspect

from aiohttp import web

class WebApp:
    def __init__(self, animations, host='0.0.0.0', port=80) -> None:
        self.animations = animations
        self.host = host
        self.port = port

        self.app = web.Application()
        self.add_routes()

    def descriptions_for_animations(self):
        return {name for name, animation in self.animations.items()}

    async def index(self, request):
        
        response =f'''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>A simple webpage</title>
</head>
<body>
  <h1>Simple HTML webpage</h1>
  <p>{self.descriptions_for_animations()}</p>
</body>
</html>
'''
        return web.Response(text=response, content_type='text/html')
    
    # TODO: Remove this when the client has been updated to use the animate endpoint
    async def legacy_trigger(self, request):
        return await self.trigger(request, 'SlotMachine')

    async def trigger(self, request, animation_name=None):
        if not animation_name:
            animation_name = request.match_info['animation']
        animation = self.animations[animation_name]
        asyncio.create_task(animation.run(**request.query))
        return web.json_response(status=200, data={'status': 'success', 'message': f'Animation {animation_name} queued successfully'})
        
    def add_routes(self):
        self.app.router.add_get('/', self.index)
        self.app.router.add_get('/kick', self.legacy_trigger) # TODO: Remove this when the client has been updated to use the animate endpoint
        self.app.router.add_get('/animate/{animation}', self.trigger)

    def run(self):
        web.run_app(self.app, host=self.host, port=self.port)
