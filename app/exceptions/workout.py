class NoExerciseException(BaseException):
    """Поднимается в случае отсутствия упражнений для тренировки."""


class NoWorkoutsException(BaseException):
    """
    Поднимается в случае отсутствия к.л. тренировок для пользователя под его
     параметры(цель, пол).
    """
