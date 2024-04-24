from typing import Iterable
import arcade

from player import Player
from settings import WIN_H, WIN_W


class Level(arcade.Scene):
    def __init__(self) -> None:
        super(Level, self).__init__()

        self.player: Player = Player(center_x= WIN_W // 2, center_y= WIN_H // 2)
    
    def setup(self):
        self.add_sprite("Player", self.player)