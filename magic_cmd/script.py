from __future__ import annotations
from typing import (
                    Union, 
                    Callable, 
)
from pathlib import Path
from magic_cmd.engine import Engine 
from magic_cmd.run_cmd import Shell


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
                 name:str= 'script',
                 engine:Engine=Shell(),
                 clean_on_append:bool=False,
                ):
        self.engine:Engine = engine
        self.cmds:str = self.engine.clean(cmds)
        self.name:str = name
        self.clean_on_append = clean_on_append

    def __add__(self,cmd: Union[Script,str])->str:
        match(cmd):
            case str() if self.clean_on_append:#if clean on append clean cmd 
                cmd = self.engine.clean(cmd)
            case str():# if not do nothing
                ...
            case Script() if self.engine.__class__!=cmd.engine.__class__:#engines don't match 
                raise Exception(f'{cmd.engine.__class__} does not match{self.engine.__class__}')
            case Script(): # combine two scripts
                cmd = cmd.cmds
        return Script('\n'.join([self.cmds,cmd]))
    
    def __iadd__(self,cmd: Union[Script,str])->Script:
        return (self:=self + cmd)
    
    def __repr__(self) -> str:
        return self.cmds
    
    def __str__(self) -> str:
        return self.cmds
     
    def __call__(self,
                 lazy:bool=False,
                 name:str='lazy',
                 split:bool='False',
                 *args,**kwargs) -> Union[Path,list[str]]:
        if lazy:
            return self.engine.write(self.cmds,name=name)
        return self.engine.run(self.cmds,split=split)
    
    def __eq__(self, __value: object) -> bool:
        return str(self) == __value 

    def append(self,cmd:Union[Script,str])->None:
        self.cmds += cmd
        