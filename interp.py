from dataclasses import dataclass
from typing import Union, Dict, Any

# expression type defs.
Expr = Union['Add', 'Sub', 'Mul', 'Div', 'Neg', 'Lit', 'Let', 'Name', 'Eq', 'Lt', 'If', 
             'StrLit', 'StrConcat', 'StrReplace', 'And', 'Or', 'Not']

# lit 
@dataclass(frozen=True)
class Lit:
    value: Any

# add
@dataclass(frozen=True)
class Add:
    left: Expr
    right: Expr

# sub
@dataclass(frozen=True)
class Sub:
    left: Expr
    right: Expr

# mul
@dataclass(frozen=True)
class Mul:
    left: Expr
    right: Expr

# div
@dataclass(frozen=True)
class Div:
    left: Expr
    right: Expr

# neg
@dataclass(frozen=True)
class Neg:
    operand: Expr

# and
@dataclass(frozen=True)
class And:
    left: Expr
    right: Expr

# or
@dataclass(frozen=True)
class Or:
    left: Expr
    right: Expr

# not
@dataclass(frozen=True)
class Not:
    operand: Expr

# let
@dataclass(frozen=True)
class Let:
    name: str
    value_expr: Expr
    body_expr: Expr

# name
@dataclass(frozen=True)
class Name:
    name: str

# eq
@dataclass(frozen=True)
class Eq:
    left: Expr
    right: Expr

# lt
@dataclass(frozen=True)
class Lt:
    left: Expr
    right: Expr

# if
@dataclass(frozen=True)
class If:
    conditional: Expr
    then_b: Expr
    else_b: Expr

# strlit
@dataclass(frozen=True)
class StrLit:
    value: str

# strconcat
@dataclass(frozen=True)
class StrConcat:
    left: Expr
    right: Expr

# strrplace
@dataclass(frozen=True)
class StrReplace:
    og: Expr
    target: Expr
    replacement: Expr

# eval
def eval(expr: Expr, env: Dict[str, Any] = None) -> Any:
    if env is None:
        env = {}

    if isinstance(expr, Lit):
        return expr.value

    elif isinstance(expr, Name):
        if expr.name in env:
            return env[expr.name]
        else:
            raise NameError(f"Name '{expr.name}' not found in environment.")

    elif isinstance(expr, Add):
        l = eval(expr.left, env)
        r = eval(expr.right, env)
        if type(l) is not int or type(r) is not int:
            raise TypeError("Add requires integer operands.")
        return l + r

    elif isinstance(expr, Sub):
        l = eval(expr.left, env)
        r = eval(expr.right, env)
        if type(l) is not int or type(r) is not int:
            raise TypeError("Sub requires integer operands.")
        return l - r

    elif isinstance(expr, Mul):
        l = eval(expr.left, env)
        r = eval(expr.right, env)
        if type(l) is not int or type(r) is not int:
            raise TypeError("Mul requires integer operands.")
        return l * r

    elif isinstance(expr, Div):
        l = eval(expr.left, env)
        r = eval(expr.right, env)
        if type(l) is not int or type(r) is not int:
            raise TypeError("Div requires integer operands.")
        if r == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return l // r

    elif isinstance(expr, Neg):
        val = eval(expr.operand, env)
        if type(val) is not int:
            raise TypeError("Neg requires an integer.")
        return -val

    elif isinstance(expr, Eq):
        l = eval(expr.left, env)
        r = eval(expr.right, env)
        if type(l) != type(r):
            return False
        return l == r

    elif isinstance(expr, Lt):
        l = eval(expr.left, env)
        r = eval(expr.right, env)
        if type(l) is not int or type(r) is not int:
            raise TypeError("Lt requires integer operands.")
        return l < r

    elif isinstance(expr, If):
        cond = eval(expr.conditional, env)
        if not isinstance(cond, bool):
            raise TypeError("If condition needs to be a boolean.")
        if cond:
            return eval(expr.then_b, env)
        else:
            return eval(expr.else_b, env)

    elif isinstance(expr, Let):
        val = eval(expr.value_expr, env)
        new_env = env.copy()
        new_env[expr.name] = val
        return eval(expr.body_expr, new_env)

    elif isinstance(expr, And):
        l = eval(expr.left, env)
        if not isinstance(l, bool):
            raise TypeError("And requires boolean operands.")
        if not l:
            return False
        r = eval(expr.right, env)
        if not isinstance(r, bool):
            raise TypeError("And requires boolean operands.")
        return r

    elif isinstance(expr, Or):
        l = eval(expr.left, env)
        if not isinstance(l, bool):
            raise TypeError("Or requires boolean operands.")
        if l:
            return True
        r = eval(expr.right, env)
        if not isinstance(r, bool):
            raise TypeError("Or requires boolean operands.")
        return r

    elif isinstance(expr, Not):
        val = eval(expr.operand, env)
        if not isinstance(val, bool):
            raise TypeError("Not requires a boolean operand.")
        return not val

    elif isinstance(expr, StrLit):
        return expr.value

    elif isinstance(expr, StrConcat):
        l = eval(expr.left, env)
        r = eval(expr.right, env)
        if not isinstance(l, str) or not isinstance(r, str):
            raise TypeError("StrConcat requires string operands.")
        return l + r

    elif isinstance(expr, StrReplace):
        original = eval(expr.og, env)
        target = eval(expr.target, env)
        replacement = eval(expr.replacement, env)
        if not all(isinstance(v, str) for v in [original, target, replacement]):
            raise TypeError("StrReplace requires all operands to be strings.")
        return original.replace(target, replacement, 1)

    else:
        raise NotImplementedError(f"Unknown expression type: {type(expr)}.")

# run
def run(expr: Expr) -> None:
    result = eval(expr)
    print(result)

# This interpreter supports string operations
# as part of a DSL feature set. The operations include:

# 'StrLit' : represents a string literal
# 'StrConcat' : performs string concatenation
# 'StrReplace' : replace first occurance of a substring in a string

# These extensions allow the interpreter to do simple string 
# manipulations.
# testing the domain string operations

run(StrLit("hello world!")) # prints: hello world!

run(StrConcat(StrLit("hello "),StrLit("world!"))) # prints: hello world!

run(StrReplace(StrLit("hello world!"), StrLit("world!"), StrLit("hello!"))) # prints: hello hello!