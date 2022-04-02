import time
import pytest

from countdown_timer import countdown_timer

acceptable_error = 1 / 3600  # 1 second per 1 hour
time_data = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 30, 60}


@pytest.mark.parametrize("seconds", time_data)
def test_countdown_timer(seconds):
    time_control = time.time()
    countdown_timer(seconds)
    time_control = time.time() - time_control - seconds

    assert time_control < acceptable_error
