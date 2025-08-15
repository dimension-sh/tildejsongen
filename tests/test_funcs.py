from tildejsongen import str2bool


def test_str2bool():
    assert str2bool('yes') is True
    assert str2bool('true') is True
    assert str2bool('t') is True
    assert str2bool('1') is True
    assert str2bool('on') is True

    assert str2bool('no') is False
    assert str2bool('false') is False
    assert str2bool('f') is False
    assert str2bool('0') is False
    assert str2bool('off') is False

    assert str2bool('ys') is False
    assert str2bool('truex') is False
    assert str2bool('z') is False
    assert str2bool('3') is False
    assert str2bool('maybe') is False