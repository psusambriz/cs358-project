from dataclasses import dataclass
from typing import Union, Any

# expression type defs.
Expr = Union['Add', 'Sub', 'Mul', 'Div', 'Neg', 'Lit', 'Let', 'Name', 'Eq', 'Lt', 'If', 
             'StrLit', 'StrConcat', 'StrReplace', 'And', 'Or', 'Not', 'Letfun', 'App']

# lit 
@dataclass
class Lit: # recheck
    value: Union[int,bool,str]
    def __str__(self): return repr(self.value) if isinstance(self.value, str) else str(self.value)

# add
@dataclass
class Add: # done
    left: Expr
    right: Expr
    def __str__(self): return f"{self.left} + {self.right}"

# sub
@dataclass
class Sub: # done
    left: Expr
    right: Expr
    def __str__(self): return f"{self.left} - {self.right}"

# mul
@dataclass
class Mul: # done
    left: Expr
    right: Expr
    def __str__(self): return f"({self.left} * {self.right})"

# div
@dataclass
class Div: # done
    left: Expr
    right: Expr
    def __str__(self): return f"({self.left} / {self.right})"

# neg
@dataclass
class Neg: # done
    subexpr: Any
    def __str__(self): return f"-{self.subexpr}"

# and
@dataclass
class And: # done
    left: Expr
    right: Expr
    def __str__(self): return f"({self.left} and {self.right})"

# or
@dataclass
class Or: # done
    left: Expr
    right: Expr
    def __str__(self): return f"({self.left} or {self.right})"

# not
@dataclass
class Not: # done
    subexpr: Any
    def __str__(self): return f"(not {self.subexpr})"

# let
@dataclass
class Let: # done
    name: str
    value_expr: Any
    body_expr: Any
    def __str__(self): return f"(let {self.name} = {self.value_expr} in {self.body_expr})"

# name
@dataclass
class Name: # done
    name: str
    def __str__(self): return self.name


# eq
@dataclass
class Eq: # done
    left: Any
    right: Any
    def __str__(self): return f"({self.left} == {self.right})"

# lt
@dataclass
class Lt: # done
    left: Any
    right: Any
    def __str__(self): return f"({self.left} < {self.right})"

# if
@dataclass
class If: # done
    cond: Any
    then: Any
    else_: Any
    def __str__(self): return f"(if {self.cond} then {self.then} else {self.else_})"


# strlit
@dataclass(frozen=True)
class StrLit:
    value: str

# strconcat
class StrConcat: # done
    left: Any
    right: Any
    def __str__(self): return f"({self.left} ++ {self.right})"

# strrplace
@dataclass(frozen=True)
class StrReplace:
    name: str
    param: str
    funbody: Any
    inexpr: Any
    def __str__(self): return f"replace({self.target}, {self.old}, {self.new})"

# letfun
@dataclass
class Letfun: # done
    name: str
    param: str
    body_expr: Any
    in_expr: Any
    def __str__(self): return f"(letfun {self.name}({self.param}) = {self.body_expr} in {self.in_expr})"

@dataclass
class App: # done
    fun_expr: Any
    arg_expr: Any
    def __str__(self): return f"{self.fun_expr}({self.arg_expr})"

Env = tuple[tuple[str,Any], ...]

class EvalError(Exception):
    pass

# eval
def eval(expr: Any, env: Env = None) -> Any:
    env = env or {}
    match expr:
        case Add(l,r):
            lv,rv = eval(l,env), eval(r,env)
            if type(lv) == int and type(rv) == int: return lv + rv
            raise EvalError("add requires integers")
        case Sub(l,r):
            lv,rv = eval(l,env), eval(r,env)
            if type(lv) == int and type(rv) == int: return lv - rv
            raise EvalError("sub requires integers")
        case Mul(l,r):
            lv, rv = eval(l, env), eval(r, env)
            if type(lv) == int and type(rv) == int: return lv * rv
            raise EvalError("mul requires integers")
        case Div(l, r):
            lv, rv = eval(l, env), eval(r, env)
            if not (type(lv) == int and type(rv) == int):
                raise EvalError("div requires integers")
            if rv == 0: raise EvalError("division by zero")
            return lv // rv
        case Neg(e):
            ev = eval(e, env)
            if type(ev) == int: return -ev
            raise EvalError("neg requires integer")
        case Lit(v): return v
        case Let(name, de, body):
            val = eval(de, env)
            new_env = ((name, val),) + env
            return eval(body, new_env)
        case Name(n):
            for var, val in env:
                if var == n: return val
            raise EvalError(f"unbound variable {n}")
        case Eq(l, r):
            lv, rv = eval(l, env), eval(r, env)
            # For Milestone 1, if types are different, they are unequal.
            # Eq handles string comparison naturally if both are strings.
            if type(lv) != type(rv): return False
            return lv == rv
        case Lt(l, r):
            lv, rv = eval(l, env), eval(r, env)
            if type(lv) == int and type(rv) == int: return lv < rv
            raise EvalError("lt requires integers")
        case If(c, t, e):
            cv = eval(c, env)
            if not isinstance(cv, bool): raise EvalError("the If condition must be boolean")
            return eval(t, env) if cv else eval(e, env)
        case And(l, r):
            lv = eval(l, env)
            if not isinstance(lv, bool): raise EvalError("and requires booleans")
            if not lv: return False # Short-circuiting
            rv = eval(r, env)
            if not isinstance(rv, bool): raise EvalError("and requires booleans")
            return rv
        case Or(l, r):
            lv = eval(l, env)
            if not isinstance(lv, bool): raise EvalError("or requires booleans")
            if lv: return True # Short-circuiting
            rv = eval(r, env)
            if not isinstance(rv, bool): raise EvalError("or requires booleans")
            return rv
        case Not(e):
            ev = eval(e, env)
            if isinstance(ev, bool): return not ev
            raise EvalError("not requires boolean")
        case StrConcat(l, r):
            lv, rv = eval(l, env), eval(r, env)
            if isinstance(lv, str) and isinstance(rv, str): return lv + rv
            raise EvalError("concat requires strings")
        case StrReplace(t, o, n):
            tv, ov, nv = eval(t, env), eval(o, env), eval(n, env)
            if not all(isinstance(x, str) for x in (tv, ov, nv)):
                raise EvalError("replace requires strings")
            return tv.replace(ov, nv, 1) 
        case Letfun(fname, param, funbody, inexpr):
            closure_val = ("recursive_closure", param, funbody, env, fname)
            env_for_inexpr = ((fname, closure_val),) + env
            return eval(inexpr, env_for_inexpr)
        case App(funexpr, actual):
            fun_val = eval(funexpr, env) # Evaluate the function expression in the current environment

            if isinstance(fun_val, tuple) and fun_val[0] == "recursive_closure":
                _, param_name, body_expr, captured_def_env, fun_name_for_recursion = fun_val
                actual_val = eval(actual, env) # Evaluate actual argument in current (call-site) environment

                env_for_body = ((param_name, actual_val), (fun_name_for_recursion, fun_val),) + captured_def_env
                return eval(body_expr, env_for_body)
            elif isinstance(fun_val, tuple) and fun_val[0] == "closure": 
                _, param_name, body_expr, captured_def_env = fun_val
                actual_val = eval(actual, env)
                env_for_body = ((param_name, actual_val),) + captured_def_env
                return eval(body_expr, env_for_body)
            else:
                raise EvalError(f"App requires a function, got {fun_val}")
        case _:
            raise EvalError(f"Unknown expression: {expr}")
        
# run
def run(expr: Any) -> None:
    try:
        result = eval(expr)
        if isinstance(result, str):
            print(f'Result: "{result}"') # Explicit quotes for strings
        elif isinstance(result, bool):
            print(f"Result: {str(result).lower()}") # true/false
        else:
            print(f"Result: {result}")
    except EvalError as e:
        print(f"Error: {e}")
    except Exception as e: # Catch any other unexpected errors during eval/run
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()

# This interpreter supports string operations
# as part of a DSL feature set. The operations include:

# 'StrLit' : represents a string literal
# 'StrConcat' : performs string concatenation
# 'StrReplace' : replace first occurance of a substring in a string

# These extensions allow the interpreter to do simple string 
# manipulations.

# testing the domain string operations