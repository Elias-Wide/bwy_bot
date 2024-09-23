"""Exeptions участка тренировок."""


class NoExerciseException(BaseException):
    """Поднимается в случае отсутствия упражнений для тренировки."""


class NoWorkoutsException(BaseException):
    """Поднимается в случае отсутствия к.л. тренировок для пользователя.

    под егопараметры(цель, пол).
    """


class NoExerciseVideo(BaseException):
    """Поднимается когда видеофайл по указанному в БД пути отсутствует."""
