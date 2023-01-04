from project import arc_color_update, completion, timer_update


def main():
    test_arc_color_update()
    test_completion()
    test_timer_update()


def test_arc_color_update():
    assert arc_color_update(0) == '#00ff00'
    assert arc_color_update(45) == '#3fc000'
    assert arc_color_update(90) == '#7f8000'
    assert arc_color_update(120) == '#aa5500'
    assert arc_color_update(180) == '#ff0000'


def test_completion():
    assert completion(0, 0) == 0
    assert completion(0, 20) == 0
    assert completion(60, 0) == 0
    assert completion(180, 5) == 60
    assert completion(600, 120) == 8
    assert completion(2700, 180) == 25


def test_timer_update():
    assert timer_update(0) == '00:00'
    assert timer_update(30) == '00:30'
    assert timer_update(60) == '01:00'
    assert timer_update(600) == '10:00'
    assert timer_update(1225) == '20:25'
    assert timer_update(2477) == '41:17'
    assert timer_update(3599) == '59:59'


if __name__ == "__main__":
    main()
