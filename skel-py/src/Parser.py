from __future__ import annotations
from builtins import print
from typing import Type
#from src.Regex import Character, Operator
class Character:
    __match_args__ = ("chr",)    

    def __init__(self, chr: str):
        self.chr = chr
    
    def __str__(self) -> str:
        return self.chr

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
            self.importance = 4
        elif op == "+":
             self.importance = 4
        elif op == "?":
            self.importance = 4
        elif op == ".":
            self.importance = 3
        elif op == "|":
            self.importance = 2
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


class Parser:
    # This function should:
    # -> Classify input as either character(or string) or operator
    # -> Convert special inputs like [0-9] to their correct form
    # -> Convert escaped characters
    # You can use Character and Operator defined in Regex.py
    @staticmethod
    def preprocess(regex: str) -> list:
        list = []
        regex = regex.replace("[0-9]","(0|1|2|3|4|5|6|7|8|9)")
        regex = regex.replace("[a-z]","(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|r|s|t|u|v|w|x|y|z)")
        regex = regex.replace("[A-Z]","(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|R|S|T|U|V|W|X|Y|Z)")
        regex = regex.replace("\' \'","@")
        regex = regex.replace("\'","")
        #am inlocit epsilon cu un caracter pe c are nu o sa l folosesc niciodata si il schimb din nou in epsilon la final
        regex = regex.replace("eps","^")
        operations=["|", "*", "+", "?", "(", ")"]
        before = ["+", "?",")","*"]
        
        #setez operatie care nu e before prec
        
        prec = "|"
        for i in regex:
            if i in operations:
                if prec in before and i == "(":
                    list.append(Operator("."))
                if not prec in operations and i == "(":
                    list.append(Operator("."))
                
                list.append(Operator(i))
                #a=Operator(i)
                #print(a.importance)
            elif prec in before:
                list.append(Operator("."))
                list.append(Character(i))
            elif not prec in operations:
                list.append(Operator("."))
                list.append(Character(i))
            else:
                list.append(Character(i))
            prec = i
              

        print (list)
        return list

    # This function should construct a prenex expression out of a normal one.
    @staticmethod
    def toPrenex(s: str) -> str:
        list = Parser.preprocess(s)
        finalList = []
        listOfOperators = []

        while list:
            c = list.pop()
            if str(c) == ')':
                listOfOperators .append(c)
            elif str(c) == '(':
                a = listOfOperators.pop()
                while str(a) != ')':
                    finalList.append(a)
                    a = listOfOperators.pop()
                    
            elif isinstance(c, Operator):

                while listOfOperators :
                    # se compara importanta
                    a = listOfOperators.pop()
                    if  c.importance > a.importance:
                        listOfOperators.append(a)
                        break
                    finalList.append(a)
                listOfOperators.append(c)
            else:
                finalList.append(c)
        while listOfOperators:
            a = listOfOperators.pop()
            finalList.append(a)
            
        result = ""
        while finalList:
            a = finalList.pop()
            result = result + str(a)
        result = " ".join(result)
        result = result.replace("?","MAYBE")
        result = result.replace("*","STAR")
        result = result.replace("|","UNION")
        result = result.replace(".","CONCAT")
        result = result.replace("+","PLUS")
        result = result.replace("^","eps")
        print(result)
        print("-----------------")
        return result
 
    
