from typing import Optional
import arcade
from time import perf_counter
from level import Level
from settings import (
    DEBUG_FONT_SIZE,
    GAME_NAME,
    GRAPH_HEIGHT,
    GRAPH_MARGIN,
    GRAPH_WIDTH,
    NUM_FRAME_SAMPLES,
    TARGET_FPS,
    WIN_SIZE,
)


class GameWindow(arcade.Window):
    def __init__(self, *args, **kwargs):
        super(GameWindow, self).__init__(
            *WIN_SIZE,
            GAME_NAME,
            update_rate=1.0 / TARGET_FPS,
            fullscreen=True,
            *args,
            **kwargs,
        )

        self.perf_graph_list: Optional[arcade.SpriteList] = None
        self.fps_text: Optional[arcade.Text] = None
        self.frame_count: int = 0

        # self.update_time_taken: float = 0.0
        self.current_level: Level = Level()

        arcade.enable_timings()

    def setup(self):
        # TODO: Get current level from file
        self.current_level.setup()

        # Create a sprite list to put the performance graphs into
        self.perf_graph_list = arcade.SpriteList()

        # Calculate position helpers for the row of 3 performance graphs
        row_y = self.height - GRAPH_HEIGHT / 2
        starting_x = GRAPH_WIDTH / 2
        step_x = GRAPH_WIDTH + GRAPH_MARGIN

        # Create the on_update graph
        graph = arcade.PerfGraph(GRAPH_WIDTH, GRAPH_HEIGHT, graph_data="on_update")
        graph.position = starting_x, row_y
        self.perf_graph_list.append(graph)

        # Create the on_draw graph
        graph = arcade.PerfGraph(GRAPH_WIDTH, GRAPH_HEIGHT, graph_data="on_draw")
        graph.position = starting_x + step_x, row_y
        self.perf_graph_list.append(graph)

        # Create the FPS performance graph
        graph = arcade.PerfGraph(GRAPH_WIDTH, GRAPH_HEIGHT, graph_data="FPS")
        graph.position = starting_x + step_x * 2, row_y
        self.perf_graph_list.append(graph)

        # Create a Text object to show the current FPS
        self.fps_text = arcade.Text(
            f"FPS: {arcade.get_fps(60):5.1f}", 10, 10, arcade.color.BLACK, 22
        )

    def on_update(self, delta_time):
        self.frame_count += 1
        if self.frame_count % NUM_FRAME_SAMPLES == 0:
            arcade.clear_timings()
            self.frame_count = 0

        self.current_level.on_update(delta_time=1.0/60.0)

    def draw_debug_info(self):
        if arcade.timings_enabled():
            self.perf_graph_list.draw()

    def on_draw(self):
        self.clear(arcade.color.WHITE)
        self.draw_debug_info()
        self.current_level.draw()
