from lark import Lark, Transformer, Tree, UnexpectedInput, v_args
from lark.visitors import VisitError
from pathlib import Path
from interp import Expr, Lit, Add, Sub, Mul, Div, Neg, And, Or, Not, \
    Let, Name, Eq, Lt, If, Letfun, App, StrConcat, StrLit, StrReplace
from interp import run as interp_run

# load grammar
grammar = Path('expr.lark').read_text()
parser = Lark(grammar, start='expr', parser='lalr')

@v_args(inline=True)
class ASTTransformer(Transformer):
    def number(self, n):
        return Lit(int(n.value)) # Access token value

    def string(self, s):
        return Lit(s.value[1:-1]) # Access token value and strip quotes

    def boolean_true(self):
        return Lit(True)

    def boolean_false(self):
        return Lit(False)

    def name(self, n):
        return Name(str(n.value)) # Access token value

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

    def not_(self, x): # Method name matches 'not_' in grammar
        return Not(x)

    def and_(self, left, right): # Method name matches 'and_' in grammar
        return And(left, right)

    def or_(self, left, right): # Method name matches 'or_' in grammar
        return Or(left, right)

    def eq(self, left, right):
        return Eq(left, right)

    def lt(self, left, right):
        return Lt(left, right)

    def if_(self, cond, then_expr, else_expr): # Ensure names don't clash with keywords
        return If(cond, then_expr, else_expr)

    def let(self, name_token, defexpr, bodyexpr):
        return Let(str(name_token.value), defexpr, bodyexpr) # Access token value

    def letfun(self, fname_token, param_token, funbody, inexpr):
        return Letfun(str(fname_token.value), str(param_token.value), funbody, inexpr) # Access token values

    def app(self, func_expr, arg_expr):
        # With a left-recursive grammar for 'app', 'func_expr' and 'arg_expr'
        # will already be transformed AST nodes.
        return App(func_expr, arg_expr)

def just_parse(s: str):
    try:
        tree = parser.parse(s)
        ast = ASTTransformer().transform(tree)
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
