from __future__ import annotations
from builtins import print
from typing import Type

class Character:
    __match_args__ = ("chr",)    

    def __init__(self, chr: str):
        self.chr = chr
    
    def __str__(self) -> str:
        return f"Char {self.chr}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, Character):
            return self.chr == other.chr
        return False

class Operator:
    __match_args__ = ("op",)    

    def __init__(self, op: str):
        self.op = op
        if op == "*":
            self.importance = 5
        elif op == "+":
             self.importance = 5
        elif op == "?":
            self.importance = 5
        elif op == ".":
            self.importance = 4
        elif op == "|":
            self.importance = 3
        elif op == "(":
            self.importance = 1
        elif op == ")":
            self.importance = 1
        else:
            self.importance = 10000

    def __str__(self) -> str:
        return self.op

    def __repr__(self):
        return str(self)
    
    def __eq__(self, other):
        if isinstance(other, Operator):
            return self.op == other.op
        return False
