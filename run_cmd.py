from subprocess import Popen, PIPE as l
def run_cmd(cmd:str, split=True):
    '''
    run_cmd in python with out Popen
    '''
    out, err = Popen(cmd,shell=True,stdout=l).communicate()
    if err: raise OSError(err)
    return out.decode().split('\n') if split else out.decode()