from lark import Lark, Transformer
from pathlib import Path
from interp import *
from interp import run

# load grammar
grammar = Path('expr.lark').read_text()
parser = Lark(grammar, start='start', parser='earley', ambiguity='explicit')

# transformer: coverts parse tree to ast
class ASTTransformer(Transformer):
    def number(self,n):
        return Lit(int(n[0]))
    def string(self,s):
        return StrLit(s[0][1:-1])
    def true(self,_):
        return Lit(True)
    def false(self,_):
        return Lit(False)
    def var(self,name):
        return Name(str(name[0]))
    def add(self,args):
        return Add(args[0],args[1])
    def sub(self,args):
        return Sub(args[0],args[1])
    def mul(self,args):
        return Mul(args[0],args[1])
    def div(self,args):
        return Div(args[0],args[1])
    def neg(self,args):
        return Neg(args[0])
    def and_(self,args):
        return And(args[0],args[1])
    def or_(self,args):
        return Or(args[0],args[1])
    def eq(self,args):
        return Eq(args[0],args[1])
    def lt(self,args):
        return Lt(args[0],args[1])
    def if_(self,args):
        return If(args[0],args[1],args[2])
    def let(self,args):
        return Let(args[0],args[1],args[2])
    def letfun(self,args):
        return LetFun(args[0],args[1],args[2],args[3])
    def app(self,args):
        return App(args[0],args[1])
    def strconcat(self,args):
        return StrConcat(args[0],args[1])
    def strreplace(self,args):
        return StrReplace(args[0], StrLit(args[1][1:-1]),StrLit(args[2][1:-1]))
    
# parse function
def parse(s):
    tree = parser.parse(s)
    return ASTTransformer().transform(tree)

# run function
def run_string(s):
    ast = parse(s)
    return run(ast)

run_string('5 + 2')
run_string('"hello" ++ " world"')
run_string('letfun double(x) = x + x in double(5) end')
    

