"""Общий модуль для подключение логера."""

import logging


def get_logger(name: str) -> logging.Logger:
    """Возвращает логер."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
        '[%(asctime)s] - %(name)s - %(message)s',
    )
    return logging.getLogger(name)
