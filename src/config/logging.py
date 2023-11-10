import logging
from pathlib import Path

import structlog




structlog.configure(
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.add_log_level,
        structlog.processors.EventRenamer("message"),
        structlog.processors.CallsiteParameterAdder(
            [structlog.processors.CallsiteParameter.FUNC_NAME]
        ),
        structlog.processors.dict_tracebacks,
        # structlog.dev.ConsoleRenderer(),
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.WriteLoggerFactory(
        file=Path("app.log").open("at")
    ),
)


logger = structlog.get_logger()
