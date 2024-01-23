from magic_cmd.script import Script
from magic_cmd.run_cmd import SSH_Shell, SSH_Connection
from typing import Optional

def test_script():
    '''
    test run script
    '''
    test = Script('echo howdy')
    test += 'echo you'
    assert test() == [['howdy'], ['you']]


def test_add():
    '''
    test
    script +str
    script + script
    script + script with  other engine needs to fail
    '''
    dummy_ssh:SSH_Connection = SSH_Connection('','','')
    ssh_shell:SSH_Shell = SSH_Shell(dummy_ssh)
    ssh:Script = Script('echo dummy',engine=ssh_shell)
    test:Script = Script('echo foo')
    other:Script = Script('echo other')
    test_str:str = 'echo str'
    test_script_str:Script = test + test_str
    test_scripts:Script = test + test_script_str
    error:Optional[str] = None
    try: test+ssh
    except Exception as e: error = e
    assert error

def test_clean():
    '''
    test the clean function
    '''
    test:Script = Script('''
                            echo foo
                                echo bar
                            ''')
    res = '''echo foo
    echo bar
'''
    print(test)
    print(res)
    assert test == res