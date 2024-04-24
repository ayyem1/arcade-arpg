from typing import Any
import arcade


class Player(arcade.Sprite):
    def __init__(
        self,
        path_or_texture: str | arcade.Path | bytes | arcade.Texture | None = None,
        scale: float = 1,
        center_x: float = 0,
        center_y: float = 0,
        angle: float = 0,
        **kwargs: Any,
    ):
        super(Player, self).__init__(path_or_texture, scale, center_x, center_y, angle, **kwargs)
    
    def on_update(self, delta_time: float = 1 / 60) -> None:
        super().on_update(delta_time)
    