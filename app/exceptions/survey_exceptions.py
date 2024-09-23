"""Exeptions участка анкеты."""


class DisallowedHumanParameterError(ValueError):
    """Исключение возникает если получено неожиданное значение параметра."""
