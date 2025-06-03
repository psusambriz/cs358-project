# sal ambriz
# cs358

from dataclasses import dataclass

type Literal = int

type Expr = Add | Sub | Mul | Div | Neg | Lit | Let | Name | Eq | \
Lt | If | StrLit | StrConcat | StrReplace | And | Or | Not | Letfun | App | \
Assign | Seq | Show | Read | StrLen | ToLower

type Value = int | bool | str | Closure | Loc

# add
@dataclass
class Add:
    left: Expr
    right: Expr
    def __str__(self) -> str:
        return f"({self.left} + {self.right})"

# sub
@dataclass
class Sub:
    left: Expr
    right: Expr
    def __str__(self) -> str:
        return f"({self.left} - {self.right})"

# mul
@dataclass
class Mul:
    left: Expr
    right: Expr
    def __str__(self) -> str:
        return f"({self.left} * {self.right})"

# div
@dataclass
class Div:
    left: Expr
    right: Expr
    def __str__(self) -> str:
        return f"({self.left} / {self.right})"

# neg
@dataclass
class Neg:
    subexpr: Expr
    def __str__(self) -> str:
        return f"(- {self.subexpr})"
    
# lit 
@dataclass
class Lit():
    value: Literal
    def __str__(self) -> str:
        return f"{self.value}"

@dataclass
class Name:
    name:str
    def __str__(self) -> str:
        return self.name
# and
@dataclass
class And:
    left: Expr
    right: Expr
    def __str__(self) -> str:
        return f"({self.left} && {self.right})"

# or
@dataclass
class Or:
    left: Expr
    right: Expr
    def __str__(self) -> str:
        return f"({self.left} || {self.right})"

# not
@dataclass
class Not:
    operand: Expr
    def __str__(self) -> str:
        return f"(!{self.operand})"

# let
@dataclass
class Let:
    name: str
    value_expr: Expr
    body_expr: Expr
    def __str__(self) -> str:
        return f"(let {self.name} = {self.value_expr} in {self.body_expr})"

# eq
@dataclass
class Eq:
    left: Expr
    right: Expr
    def __str__(self) -> str:
        return f"({self.left} == {self.right})"

# lt
@dataclass
class Lt:
    left: Expr
    right: Expr
    def __str__(self) -> str:
        return f"({self.left} < {self.right})"

# if
@dataclass
class If:
    conditional: Expr
    then_b: Expr
    else_b: Expr
    def __str__(self) -> str:
        return f"(if {self.conditional} then {self.then_b} else {self.else_b})"

# strlit
@dataclass
class StrLit:
    value: str
    def __str__(self) -> str:
        return f'"{self.value}"'

# strconcat
@dataclass
class StrConcat:
    left: Expr
    right: Expr
    def __str__(self) -> str:
        return f"({self.left} ^ {self.right})"

# strrplace
@dataclass
class StrReplace:
    og: Expr
    target: Expr
    replacement: Expr
    def __str__(self) -> str:
        return f"({self.og} .replace({self.target}, {self.replacement}))"

@dataclass 
class StrLen:
    expr: Expr
    def __str__(self) -> str:
        return f"(length {self.expr})"

@dataclass
class ToLower:
    expr: Expr
    def __str__(self) -> str:
        return f"(tolower {self.expr})"
# letfun
@dataclass
class Letfun:
    fname: str          
    param: str          
    body: Expr          
    rest: Expr          
    def __str__(self) -> str:
        return f"(letfun {self.fname}({self.param}) = {self.body} in {self.rest}) end"

# app
@dataclass
class App:
    fexpr: Expr        
    arg: Expr           
    def __str__(self) -> str:
        return f"({self.fexpr}({self.arg}))"
    

type Binding[V] = tuple[str,V]  
type Env[V] = tuple[Binding[V], ...] 

from typing import Any
emptyEnv : Env[Any] = ()

# closure
@dataclass
class Closure:
    param: str
    body: Expr
    env: Env[Value]

@dataclass
class Loc:
    value: 'Value'

@dataclass
class Assign:
    name: str
    expr: Expr
    def __str__(self) -> str:
        return f"({self.name} := {self.expr})"
    
@dataclass
class Seq:
    first: Expr
    second: Expr
    def __str__(self) -> str:
        return f"({self.first} ; {self.second})"

@dataclass
class Show:
    expr: Expr
    def __str__(self) -> str:
        return f"(show {self.expr})"

@dataclass
class Read:
    def __str__(self) -> str:
        return "read"
    
def extendEnv[V](name: str, value: V, env:Env[V]) -> Env[V]:
    '''Return a new environment that extends the input environment env with a new binding from name to value'''
    return ((name,value),) + env

def lookupEnv[V](name: str, env: Env[V]) -> (V | None) :
    '''Return the first value bound to name in the input environment env
       (or raise an exception if there is no such binding)'''
    # exercises2b.py shows a different implementation alternative
    match env:
        case ((n,v), *rest) :
            if n == name:
                return v
            else:
                return lookupEnv(name, rest) # type:ignore
        case _ :
            return None        
        
class EvalError(Exception):
    pass

def eval(e: Expr) -> Value:
    return evalInEnv(emptyEnv,e)

def evalInEnv(env: Env[Value], e: Expr) -> Value:
    match e:
        case Lit(value):
            return value

        case Name(name):
            val = lookupEnv(name, env)
            if val is None:
                raise EvalError(f"Unbound variable '{name}'")
            if isinstance(val,Loc):
                return val.value
            return val

        case Add(left, right):
            l = evalInEnv(env, left)
            r = evalInEnv(env, right)
            if type(l) is not int or type(r) is not int:
                raise EvalError("Add requires integer operands.")
            return l + r

        case Sub(left, right):
            l = evalInEnv(env, left)
            r = evalInEnv(env, right)
            if type(l) is not int or type(r) is not int:
                raise EvalError("Sub requires integer operands.")
            return l - r

        case Mul(left, right):
            l = evalInEnv(env, left)
            r = evalInEnv(env, right)
            if type(l) is not int or type(r) is not int:
                raise EvalError("Mul requires integer operands.")
            return l * r

        case Div(left, right):
            l = evalInEnv(env, left)
            r = evalInEnv(env, right)
            if type(l) is not int or type(r) is not int:
                raise EvalError("Div requires integer operands.")
            if r == 0:
                raise EvalError("Division by zero.")
            return l // r

        case Neg(subexpr):
            val = evalInEnv(env, subexpr)
            if type(val) is not int:
                raise EvalError("Neg requires an integer.")
            return -val

        case Eq(left, right):
            l = evalInEnv(env, left)
            r = evalInEnv(env, right)
            if type(l) != type(r):
                return False
            return l == r

        case Lt(left, right):
            l = evalInEnv(env, left)
            r = evalInEnv(env, right)
            if type(l) is not int or type(r) is not int:
                raise EvalError("Lt requires integer operands.")
            return l < r

        case If(conditional, then_b, else_b):
            cond = evalInEnv(env, conditional)
            if not isinstance(cond, bool):
                raise EvalError("If condition must be boolean.")
            return evalInEnv(env, then_b if cond else else_b)

        case Let(name, value_expr, body_expr):
            val = evalInEnv(env, value_expr)
            loc = Loc(val)
            new_env = extendEnv(name,loc,env)
            return evalInEnv(new_env, body_expr)

        case And(left, right):
            l = evalInEnv(env, left)
            if not isinstance(l, bool):
                raise EvalError("And requires boolean operands.")
            if not l:
                return False  # short-circuit
            r = evalInEnv(env, right)
            if not isinstance(r, bool):
                raise EvalError("And requires boolean operands.")
            return r

        case Or(left, right):
            l = evalInEnv(env, left)
            if not isinstance(l, bool):
                raise EvalError("Or requires boolean operands.")
            if l:
                return True  # short-circuit
            r = evalInEnv(env, right)
            if not isinstance(r, bool):
                raise EvalError("Or requires boolean operands.")
            return r

        case Not(operand):
            val = evalInEnv(env, operand)
            if not isinstance(val, bool):
                raise EvalError("Not requires a boolean operand.")
            return not val

        case StrLit(value):
            return value

        case StrConcat(left, right):
            l = evalInEnv(env, left)
            r = evalInEnv(env, right)
            if not isinstance(l, str) or not isinstance(r, str):
                raise EvalError("StrConcat requires string operands.")
            return l + r

        case StrReplace(og, target, replacement):
            original = evalInEnv(env, og)
            target_val = evalInEnv(env, target)
            replacement_val = evalInEnv(env, replacement)
            if not all(isinstance(v, str) for v in [original, target_val, replacement_val]):
                raise EvalError("StrReplace requires string operands.")
            return original.replace(target_val, replacement_val, 1)
        
        case StrLen(expr):
            val = evalInEnv(env,expr)
            if not isinstance(val,str):
                raise EvalError("StrLen requires a string.")
            return len(val)
        
        case ToLower(expr):
            val = evalInEnv(env,expr)
            if not isinstance(val,str):
                raise EvalError("ToLower requires a string.")
            return val.lower()

        case Letfun(fname, param, body, rest):
            closure = Closure(param, body, None)
            loc = Loc(closure)
            new_env = extendEnv(fname,loc,env)
            closure.env = new_env
            return evalInEnv(new_env, rest)
            

        case App(fexpr, arg):
            func_val = evalInEnv(env, fexpr)
            if isinstance(func_val, Loc):
                func_val = func_val.value
            if not isinstance(func_val, Closure):
                raise EvalError(f"'{fexpr}' is not a function.")
            arg_val = evalInEnv(env, arg)
            new_env = extendEnv(func_val.param, Loc(arg_val), func_val.env)
            return evalInEnv(new_env, func_val.body)
        
        case Assign(name,expr):
            val = evalInEnv(env,expr)
            loc = lookupEnv(name,env)
            if loc is None:
                raise EvalError(f"Assignment to unbound variable '{name}'")
            if not isinstance(loc,Loc):
                raise EvalError(f"Cannot assign to non-variable '{name}'")
            if isinstance(loc.value, Closure):
                raise EvalError(f"Cannot assign to function name '{name}'")
            loc.value = val
            return val
        
        case Seq(first,second):
            evalInEnv(env,first)
            return evalInEnv(env,second)
        
        case Show(expr):
            val = evalInEnv(env,expr)
            print(val)
            return val
        
        case Read():
            user_input = input("Enter an integer: ")
            try:
                return int(user_input)
            except ValueError:
                raise EvalError("Read expects an integer input.")

        case _:
            raise EvalError(f"Unknown expression type: {e}")

def run(e: Expr) -> None:
    print(f"running {e}")
    try:
        result = eval(e)
        print(f"result: {result}")
    except EvalError as err:
        print(f"error: {err}")

# This interpreter supports string operations
# as part of a DSL feature set. The operations include:

# 'StrLit' : represents a string literal
# 'StrConcat' : performs string concatenation
# 'StrReplace' : replace first occurance of a substring in a string

# These extensions allow the interpreter to do simple string 
# manipulations.

# testing the domain string operations

if __name__ == "__main__":
    print("Demo 1: Length of input string")
    e1 = Show(StrLen(Read()))
    run(e1)

    print("\nDemo 2: Convert string to lowercase")
    e2 = Show(ToLower(StrLit("HELLO World")))
    run(e2)