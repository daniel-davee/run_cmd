from __future__ import annotations
from typing import Union, Callable, Any 

class Script():
    
    '''
        Allows you write bash scripts in python code.
        script = Scripts()
        script.cmds = """
                        ls
                        echo "an"
                       """
        script()
    '''
    
    def __init__(self,
                 cmds:str='',
                 engine:Callable[[str,Any],Union[list[str],str]]=shell):
        self.cmds:str = cmds
        self.engine: Callable[[str],Union[list[str],str]] = engine

    def __add__(self,cmd: Union[Script,str])->str:
        match(cmd):
            case str():cmds:str =  '\n'.join([self.cmds,cmd])
            case Script() if self.engine!=cmd.engine:
                raise Exception(f'{self.engine.__name__} do not match {cmd.engine.__name__}')
            case Script():cmds:str = '\n'.join([self.cmds,cmd.cmd])
        return Script(cmds)
    
    def __iadd__(self,cmd: Union[Script,str])->Script:
        self = self + cmd
        return self
    
    def __repr__(self) -> str:
        return self.cmds
    
    def __str__(self) -> str:
        return self.cmds
     
    def __call__(self,*args,**kwargs) -> list[str]:
        return self.engine(self.cmds,*args,**kwargs) 

    def append(self,cmd:Union[Script,str])->None:
        self.cmds += cmd
        
    def writefile(self,name:str='shell.sh') -> Path:
        (file_:=Path(name)).write_text(self.cmds)
        return file_
        