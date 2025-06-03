from lark import Lark, Transformer, v_args, UnexpectedInput, Tree
from interp import Expr, Add, Sub, Mul, Div, Neg, Lit, Let, Name, Eq, Lt, If, And, Or, Not, StrConcat, StrReplace, StrLit, Letfun, App, \
Assign,Seq,Show,Read

from pathlib import Path

with open("expr.lark") as f:
    grammar = f.read()
    

USE_EARLEY = False

if USE_EARLEY:
    parser = Lark(grammar, start='expr', parser='earley', ambiguity='explicit')
else:
    parser = Lark(grammar, start='expr', parser='lalr', strict=True)

@v_args(inline=True)
class ASTBuilder(Transformer):
    def number(self, n):
        return Lit(int(n.value))

    def string(self, s):
        return Lit(s.value[1:-1])

    def boolean_literal(self, value):
        return Lit(value == "true")

    def name(self, n):
        return Name(str(n.value))

    def add(self, left, right):
        return Add(left, right)

    def sub(self, left, right):
        return Sub(left, right)

    def mul(self, left, right):
        return Mul(left, right)

    def div(self, left, right):
        return Div(left, right)

    def neg(self, x):
        return Neg(x)

    def not_(self, x):
        return Not(x)

    def and_(self, left, right):
        return And(left, right)

    def or_(self, left, right):
        return Or(left, right)

    def eq(self, left, right):
        return Eq(left, right)

    def lt(self, left, right):
        return Lt(left, right)

    def if_(self, cond, then_expr, else_expr):
        return If(cond, then_expr, else_expr)

    def let(self, name_token, defexpr, bodyexpr):
        return Let(str(name_token.value), defexpr, bodyexpr)

    def letfun(self, fname_token, param_token, funbody, inexpr):
        return Letfun(str(fname_token.value), str(param_token.value), funbody, inexpr)

    def app(self, func_expr, arg_expr):
        return App(func_expr, arg_expr)

    def concat(self, left, right):
        return StrConcat(left, right)

    def replace(self, target, old, new):
        return StrReplace(target, old, new)
    
    def assign(self,name_token,expr):
        return Assign(str(name_token.value),expr)
    
    def seq(self,first,second):
        return Seq(first,second)
    
    def show(self,expr):
        return Show(expr)
    
    def read(self):
        return Read()

    def _ambig(self, options):
        for option in options:
            if isinstance(option, Seq):
                return option
        return options[0] 


def just_parse(s: str):
    try:
        tree = parser.parse(s)
        ast = ASTBuilder().transform(tree)
        return ast
    except UnexpectedInput as e:
        print(f"Parse error: {e}")
        # To help debug, you can print more context:
        # print(f"Unexpected input at line {e.line}, column {e.column}.")
        # print(f"Expected one of: {e.expected}")
        return None
    except Exception as e: # Catch other potential Lark errors (e.g., VisitError during transform)
        print(f"Transformation or other error: {e}")
        import traceback
        traceback.print_exc()
        return None