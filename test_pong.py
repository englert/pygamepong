"""Egységtesztek a Pong tiszta játéklogikájához."""
import pytest
from pong import wall_bounce, goal_scored, paddle_bounce


def test_ball_bounces_from_top_wall():
    assert wall_bounce(4, 9, -3, 600) == (9, 3)


def test_ball_bounces_from_bottom_wall():
    assert wall_bounce(596, 9, 3, 600) == (591, -3)


def test_ball_does_not_bounce_when_moving_away_from_wall():
    assert wall_bounce(12, 9, 3, 600) == (12, 3)


def test_goal_on_left_side_awards_right_player():
    assert goal_scored(-10, 9, 900) == "right"


def test_goal_on_right_side_awards_left_player():
    assert goal_scored(910, 9, 900) == "left"


def test_no_goal_inside_playing_field():
    assert goal_scored(450, 9, 900) is None


def test_paddle_bounce_reverses_horizontal_direction():
    vx, vy = paddle_bounce(250, 300, 100, 5, 0, -1)
    assert vx < 0
    assert vy < 0


def test_paddle_bounce_limits_extreme_hit_offset():
    vx, vy = paddle_bounce(1000, 300, 100, -5, 0, 1)
    assert vx > 0
    assert vy > 0
    assert (vx * vx + vy * vy) ** 0.5 == pytest.approx(5)
