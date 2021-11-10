from subprocess import Popen, PIPE as l
# import logging

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
from pysimplelog import Logger

logger = Logger(__name__)
logger.set_log_file_basename('run_cmd')
logger.set_minimum_level(0)


def run_cmd(cmd:str, split=False):
    
    '''
    run_cmd in python with out Popen
    '''
    
    cmd_msg = f"""0001###
                  {cmd=}{type(cmd)=}
                  {split=}{type(split)=}"""
    logger.debug(cmd_msg)
    out, err = Popen(cmd,shell=True,stdout=l).communicate()
    logger.debug(out)
    if err:
        logger.error(err, stack_info= True)
        raise OSError(err)
    return out.decode().split('\n') if split else out.decode()