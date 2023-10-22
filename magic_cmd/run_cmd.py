from typing import Union, Callable, Any 
from subprocess import Popen, PIPE as l
from pysimplelog import Logger
from inspect import getframeinfo, currentframe
from pathlib import Path
from paramiko import SSHClient, AutoAddPolicy
from dataclasses import dataclass
logger = Logger(__name__)
logger.set_log_file_basename('run_cmd')
logger.set_minimum_level(logger.logLevels['info'])

def run_ssh_cmd(ssh_cmd: SSH_Cmd) -> tuple[str, str]:
    (ip, key_file, username), cmd = ssh_cmd
    client = SSHClient()
    client.load_host_keys(know_host.as_posix())
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(ip,username=username, key_filename=key_file)
    _, stdout, stderr = client.exec_command(cmd)
    return stdout.read().decode(), stderr.read().decode()

def run_cmd(cmd:str, split:bool=False) -> Union[list[str],str]:
    """
    A simple wrapper for Popon to run shell commands from python
    
    Args:
        cmd str: The comanda you want to run
        example: ls
    Raises:
        OSError: If the command throws an error this  captures it. 
        example: ls /does_not_exist
    Returns:
        List[str] or str: This is output of the cmd, either as a string or
        as list which is the string spilt on endline.
    """    
    
    debug_msg = f"""########
                  {getframeinfo(currentframe())=}
                  {cmd=}{type(cmd)=}
                  {split=}{type(split)=}"""
    logger.debug(debug_msg)
    
    out, err = Popen(cmd,shell=True,stdout=l).communicate()
    debug_msg = f"""What is {out=}?
                    What is {err=}?"""
    logger.debug(debug_msg)
    
    if err:
        error_msg = f"""There was an error:
                        {err}
                        """
        logger.error(error_msg, stack_info= True)
        raise OSError(err)
    return [o for o in out.decode().split('\n') if o] if split else out.decode()

def shell(cmds:str,split=False):
        commmand_list: list[str] = cmds.split('\n')
        commmand_list = [cmd.strip() for cmd in commmand_list if cmd]
        return [run_cmd(cmd,split=split) for cmd in commmand_list]
    