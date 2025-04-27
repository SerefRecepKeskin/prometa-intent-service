import os
from .log import init_logging



logger = init_logging(
    'intent-service-api',
    file=False,
    stdout=True)
