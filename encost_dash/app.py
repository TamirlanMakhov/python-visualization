from dash_extensions.enrich import (DashProxy,
                                    ServersideOutputTransform,
                                    MultiplexerTransform)

from .callbacks import register_callbacks
from .layout import get_layout


class EncostDash(DashProxy):
    def __init__(self, **kwargs):
        self.app_container = None
        super().__init__(transforms=[ServersideOutputTransform(),
                                     MultiplexerTransform()], **kwargs)


def create_app():
    app = EncostDash(name=__name__)
    app.layout = get_layout()
    register_callbacks(app)
    return app
