from pathlib import Path
import pygame
from enum import Enum
from assets import assets

ASSET_DIR = (Path(__file__).parent.parent / "assets").resolve()

ICON_SIZE = (30, 30)

class GameObject(Enum):
    """
    Game object representing obstacles, rewards, the agent, and goal.
    """
    EMPTY = ("", "white", None)
    WALL = ("🧱", "black", assets.WALL)
    TRASH = ("🗑️", "brown", assets.TRASH)
    COIN = ("💰", "gold", assets.COIN)
    AGENT = ("🤖", "blue", assets.AGENT)
    GOAL = ("🏁", "green", assets.GOAL)

    def __init__(self, emoji: str, color: str, filename: str | None):
        self._emoji = emoji
        self._color = color
        self._path = (ASSET_DIR / filename).resolve() if filename else None
        self._icon = None

    @staticmethod
    def _load_icon(path: Path) -> pygame.Surface | None:
        """
        Load icon from file.
        """
        try:
            icon = pygame.image.load(str(path)).convert_alpha()
            return pygame.transform.smoothscale(icon, ICON_SIZE)
        except Exception as e:
            print(f"Failed to load icon '{path}': {e}")
            return None

    @property
    def emoji(self) -> str:
        """
        Get enum emoji.
        """
        return self._emoji

    @property
    def color(self) -> str:
        """
        Get enum color.
        """
        return self._color

    @property
    def icon(self) -> pygame.Surface | None:
        """
        Get enum icon.
        """
        if not hasattr(self, "_icon") or self._icon is None:
            if self._path:
                self._icon = self._load_icon(self._path)
        return self._icon

    @property
    def name(self) -> str:
        """
        Get enum name.
        """
        return self._name_

    def __str__(self):
        """
        Get enum emoji.
        """
        return self.emoji
