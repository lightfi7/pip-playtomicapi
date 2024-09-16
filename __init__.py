"""A python wrapper for Playtomic API."""

import logging
from client import PlaytomicClient
from endpoints import TenantEndpoint, TournamentEndpoint


def _prepare_logging():
    """Prepare logger for module Playtomic API."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.NullHandler())


_prepare_logging()
