""" Pynecone Main Source Frame 
https://www.youtube.com/watch?v=PjcjkQZCXRI
"""

import pynecone as pc
import random
import asyncio

class State(pc.State):
    """The app state."""
    emoji_list: list[list] = [[i, "0%"] for i in range(36)]

    count: int = 0
    track: list = []
    score: int = 0
    result: str

    def reveal_emoji(self, emoji, emoji_type):
        index = emoji[0]
        self.emoji_list = [
            [i, "100%"] if i == index else [i, opacity] for i, opacity in self.emoji_list
        ]

        self.count += 1
        self.track.append((emoji_type, emoji))

    async def check_emoji(self):
        if self.count == 2:
            if self.track[0][0] == self.track[1][0]:
                self.score += 1
                if self.score == 8:
                    self.result = "축하합니다.! 모든 이모지 짝 맞추기를 성공했습니다."
                pass
            else:
                indicies = [e[1][0] for e in self.track]
                self.emoji_list = [
                    [i, "0%"] if i in indicies else [i, opacity] for i, opacity in self.emoji_list
                ]

            self.count = 0
            self.track = []

        await asyncio.sleep(2)



class MemoryMatchGame:
    def __init__(self):
        self.stage: int = 2
        self.emojis: list = ["😀", "😅", "😂", "😁", "🤣", "🫠", "😊", "🥰", "😍", "😗", "🤪", "🫢"]
        # main game grid
        self.game_grid = pc.vstack(spacing="15px")
        self.create_board()

    def create_board(self):
        emojis = self.emojis[: self.stage * 2] * self.stage * 2
        random.shuffle(emojis)

        count = 0
        items = []

        for _ in range(self.stage * 2):
            row = pc.hstack(spacing="15px")
            for __ in range(self.stage * 2):
                row.children.append(
                    pc.container(
                        pc.text(
                            emojis[count],
                            font_size="32px",
                            cursor="pointer",
                            transition="opacity 0.55s ease 0.35s",
                            opacity=State.emoji_list[count][1],
                            on_click=lambda: [
                                State.reveal_emoji(
                                    State.emoji_list[count],
                                    emojis[count],
                                ),
                                State.check_emoji(),
                            ]
                        ),
                        width="58px",
                        height="58px",
                        bg="#1e293b",
                        border_radius="4px",
                        justify_content="center",
                        center_content=True,
                        cursor="pointer",
                    )

                )

                count += 1
            items.append(row)
        self.game_grid.children = items
        return self.game_grid


def index() -> pc.Component:
    return pc.container(
        pc.vstack(
            pc.text(
                # "Emoji Memory Match",
                "이모지 짝 맞추기",
                font_size="55px",
                font_weight="extrabold",
                color="black"
            ),
            pc.spacer(),
            game.game_grid,
            pc.spacer(),
            pc.text(
                State.result,
                font_size="25px",
                font_weight="extrabold",
                color="black"
            ),
            spacing="25px",

        ),
        bg="#0284c7",
        height="100vh",
        max_width="auto",
        display="grid",
        position="relative",
        overlay="hidden",
        place_items="center",
    )

# instanciate the class
game = MemoryMatchGame()

# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index)
app.compile()