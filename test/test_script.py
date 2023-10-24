from magic_cmd.script import Script
def test_script():
    test = Script('echo howdy')
    test += 'echo you'
    assert test() == [['howdy'], ['you']]
