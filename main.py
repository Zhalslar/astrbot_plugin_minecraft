import json
import webbrowser
from pathlib import Path
from urllib.parse import urlsplit

from quart import jsonify, request

from astrbot.api.star import Context, Star
from astrbot.core.utils.astrbot_path import get_astrbot_plugin_data_path

PLUGIN_NAME = "astrbot_plugin_minecraft"

class MinecraftPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.context = context
        self.data_dir = Path(get_astrbot_plugin_data_path()) / PLUGIN_NAME
        self.save_file = self.data_dir / "game_save.json"

    async def initialize(self):
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/ping",
            self.page_ping,
            ["GET"],
            "Page ping",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/open-standalone",
            self.open_standalone,
            ["POST"],
            "Open standalone game page",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/save",
            self.save_game,
            ["POST"],
            "Save game state",
        )
        self.context.register_web_api(
            f"/{PLUGIN_NAME}/save",
            self.load_game,
            ["GET"],
            "Load game state",
        )

    async def page_ping(self):
        return jsonify({"message": "pong"})

    async def open_standalone(self):
        payload = await request.get_json(force=True, silent=True) or {}
        target_url = str(payload.get("url", "")).strip()
        if not target_url:
            return jsonify({"ok": False, "message": "Missing target URL"}), 400

        parsed = urlsplit(target_url)
        allowed_path_prefix = f"/api/plugin/page/content/{PLUGIN_NAME}/game/"
        if (
            parsed.scheme not in {"http", "https"}
            or parsed.netloc != request.host
            or not parsed.path.startswith(allowed_path_prefix)
        ):
            return jsonify({"ok": False, "message": "Invalid standalone URL"}), 400

        opened = webbrowser.open(target_url, new=1)
        if not opened:
            return jsonify({"ok": False, "message": "Failed to open browser"}), 500

        return jsonify({"ok": True, "message": "Standalone window opened"})

    async def load_game(self):
        if not self.save_file.exists():
            return jsonify({"ok": True, "data": None})

        try:
            save_data = json.loads(self.save_file.read_text(encoding="utf-8"))
        except Exception as exc:
            return (
                jsonify({"ok": False, "message": f"Failed to read save: {exc}"}),
                500,
            )

        return jsonify({"ok": True, "data": save_data})

    async def save_game(self):
        payload = await request.get_json(force=True, silent=True) or {}
        if not isinstance(payload, dict):
            return jsonify({"ok": False, "message": "Invalid save payload"}), 400

        try:
            self.save_file.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except Exception as exc:
            return jsonify({"ok": False, "message": f"Failed to save game: {exc}"}), 500

        return jsonify({"ok": True, "message": "Game saved"})
