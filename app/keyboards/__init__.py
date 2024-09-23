"""This is the keyboards package."""

from .calories_kb import get_calories_btns
from .common_kb import get_oops_kb
from .mode_kb import MenuCallBack, get_main_menu_btns
from .settings_kb import get_settings_btns
from .sleep_kb import (
    get_sleep_back_btns,
    get_sleep_back_btns_duration,
    get_sleep_exist_btns,
    get_sleep_select_btns,
)
from .survey_kb import create_survey_kb
from .workout_kb import (
    get_exercise_btns,
    get_workout_btns,
    get_workout_select_btns,
)
