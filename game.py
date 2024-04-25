import arcade

from level import Level
from settings import GAME_NAME, GRAPH_HEIGHT, GRAPH_MARGIN, GRAPH_WIDTH, NUM_FRAME_SAMPLES, TARGET_FPS, WIN_SIZE


class GameWindow(arcade.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *WIN_SIZE,
            GAME_NAME,
            draw_rate=1.0 / TARGET_FPS,
            update_rate=1.0 / TARGET_FPS,
            fullscreen=True,
            *args,
            **kwargs,
        )

        self.perf_graph_list: arcade.SpriteList | None = None
        self.fps_text: arcade.Text | None = None
        self.frame_count: int = 0

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
        self.fps_text = arcade.Text(f"FPS: {arcade.get_fps(NUM_FRAME_SAMPLES):5.1f}", 10, 10, arcade.color.BLACK, 22)

    def on_update(self, delta_time: float):
        self.frame_count += 1
        self.fps_text.value = f"FPS: {arcade.get_fps(NUM_FRAME_SAMPLES):5.1f}"
        if self.frame_count % NUM_FRAME_SAMPLES == 0:
            arcade.clear_timings()
            self.frame_count = 0

        self.current_level.on_update(delta_time=delta_time)

    def draw_debug_info(self):
        if arcade.timings_enabled():
            self.perf_graph_list.draw()
            self.fps_text.draw()

    def on_draw(self):
        self.clear(arcade.color.WHITE)
        self.draw_debug_info()
        self.current_level.draw()
