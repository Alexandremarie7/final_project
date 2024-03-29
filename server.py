# -*- coding: utf-8 -*-
import os
import logging
from random import randint

import dash
import dash_bootstrap_components as dbc

# For apps that use flask_sqlalchemy, the database can also be initialised here
# from models.db_config import Config


logging.basicConfig(level='WARNING')
external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    meta_tags=[
        {'name': 'viewport', 'content': 'width=device-width, initial-scale=1'},
        {'charset': 'utf-8'}
    ]
)

app.config.suppress_callback_exceptions = True

server = app.server
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))

