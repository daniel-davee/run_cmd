from subprocess import Popen, PIPE as l
def run_cmd(cmd:str, split=True):
    out, err = Popen(cmd,shell=True,stdout=l).communicate()
    if err: raise OSError(err)
    return out.decode().split('\n') if split else out.decode()