from quart import jsonify

from astrbot.api.star import Context, Star

PLUGIN_NAME = "astrbot_plugin_minecraft"

class MinecraftPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.context = context

    async def initialize(self):
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/ping",
            self.page_ping,
            ["GET"],
            "Page ping",
        )

    async def page_ping(self):
        return jsonify({"message": "pong"})
