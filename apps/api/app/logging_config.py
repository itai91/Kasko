import logging


def configure_logging() -> None:
    # Simple structured-like logging format
    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s %(levelname)s %(name)s "
            "route=%(message)s"
        ),
    )

