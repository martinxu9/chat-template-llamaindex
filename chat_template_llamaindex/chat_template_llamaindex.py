"""The main Chat app."""

import reflex as rx
from chat_template_llamaindex.components import chat, navbar
from chat_template_llamaindex.state import State
from traceloop.sdk import Traceloop

Traceloop.init()


def index() -> rx.Component:
    """The main app."""
    return rx.chakra.vstack(
        navbar(),
        chat.chat(),
        chat.action_bar(),
        background_color=rx.color("mauve", 1),
        color=rx.color("mauve", 12),
        min_height="100vh",
        align_items="stretch",
        spacing="0",
    )


# Add state and page to the app.
app = rx.App(
    theme=rx.theme(
        appearance="dark",
        accent_color="sky",
    ),
)
app.add_page(index, on_load=State.load_engine)  # type: ignore
