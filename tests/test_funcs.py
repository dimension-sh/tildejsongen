import tildejsongen

def test_str2bool():
    assert tildejsongen.str2bool('yes') is True
    assert tildejsongen.str2bool('true') is True
    assert tildejsongen.str2bool('t') is True
    assert tildejsongen.str2bool('1') is True
    assert tildejsongen.str2bool('on') is True

    assert tildejsongen.str2bool('no') is False
    assert tildejsongen.str2bool('false') is False
    assert tildejsongen.str2bool('f') is False
    assert tildejsongen.str2bool('0') is False
    assert tildejsongen.str2bool('off') is False

    assert tildejsongen.str2bool('ys') is False
    assert tildejsongen.str2bool('truex') is False
    assert tildejsongen.str2bool('z') is False
    assert tildejsongen.str2bool('3') is False
    assert tildejsongen.str2bool('maybe') is False