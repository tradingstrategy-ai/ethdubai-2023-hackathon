import logging

import coloredlogs


def setup_logging(
        log_level: str | int=logging.INFO,
        in_memory_buffer=False) -> logging.Logger:
    """Setup root logger and quiet some levels.

    :param in_memory_buffer:
        Setup in-memory log buffer used to fetch log messages to the frontend.
    """

    if log_level == "disabled":
        # Special unit test marker, don't mess with loggers
        return logging.getLogger()

    if isinstance(log_level, str):
        log_level = log_level.upper()

    logger = logging.getLogger()

    # Set log format to dislay the logger name to hunt down verbose logging modules
    fmt = "%(asctime)s %(name)-50s %(levelname)-8s %(message)s"

    # Use colored logging output for console
    coloredlogs.install(level=log_level, fmt=fmt, logger=logger)

    # Disable logging of JSON-RPC requests and reploes
    logging.getLogger("web3.RequestManager").setLevel(logging.WARNING)
    logging.getLogger("web3.providers.HTTPProvider").setLevel(logging.WARNING)
    # logging.getLogger("web3.RequestManager").propagate = False

    # Disable all internal debug logging of requests and urllib3
    # E.g. HTTP traffic
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    # IPython notebook internal
    logging.getLogger("asyncio").setLevel(logging.WARNING)

    # Maplotlib puke
    logging.getLogger("matplotlib").setLevel(logging.WARNING)

    # Disable warnings on startup
    logging.getLogger("pyramid_openapi3").setLevel(logging.ERROR)

    # Datadog tracer agent
    # https://ddtrace.readthedocs.io/en/stable/basic_usage.html
    logging.getLogger("ddtrace").setLevel(logging.INFO)

    return logger