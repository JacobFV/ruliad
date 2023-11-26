from abc import abstractmethod
from functools import cached_property
import re
from pydantic import BaseModel
import nltk


class Rule(BaseModel):
    @abstractmethod
    def replace(self, symbol: str, graph: str) -> list[str]:
        pass

class RegexRule(Rule):
    regex_str: str
    replacements: list[str]

    @cached_property
    def regex(self):
        return re.compile(self.regex_str)

    def replace(self, symbol: str, graph: str) -> list[str]:
        return [self.regex.sub(replacement, graph) for replacement in self.replacements]



class CFGRule(Rule):
    cfg_str: str
    
    @cached_property
    def cfg(self):
        return nltk.CFG.fromstring(self.cfg_str)
    
    def replace(self, symbol: str, graph: str) -> list[str]:
        
