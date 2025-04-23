from dataclasses import dataclass

@dataclass
class Lit:
    value: any

@dataclass
class Add:
    left: any
    right: any

@dataclass
class Sub:
    left: any
    right: any

@dataclass
class Mul:
    left: any
    right: any

@dataclass
class Div:
    left: any
    right: any

@dataclass
class Neg:
    opperand: any

@dataclass
class And:
    left: any
    right: any

@dataclass
class Or:
    left: any
    right: any

@dataclass
class Not:
    operand: any

@dataclass
class Let:
    name: str
    value_expr: any
    body_expr: any

@dataclass
class Name:
    name: str

@dataclass
class Eq:
    left: any
    right: any

@dataclass
class Lt:
    left: any
    right: any

@dataclass 
class If:
    conditional: any
    then_b: any
    else_b: any

# building the interpretor
def eval(expr,env={}):
    if isinstance(expr, Lit):
        return expr.value
    
    elif isinstance(expr, Add):
        l = eval(expr.left,env)
        r = eval(expr.right,env)
        if not isinstance(l,int) or not isinstance(r,int):
            raise TypeError("Add requires integer operands.")
        return l + r
    
    elif isinstance(expr,Sub):
        l = eval(expr.left,env)
        r = eval(expr.right,env)
        if not isinstance(l,int) or not isinstance(r,int):
            raise TypeError("Sub requires integer operands.")
        return l - r
    
    elif isinstance(expr,Mul):
        l = eval(expr.left,env)
        r = eval(expr.right,env)
        if not isinstance(l,int) or not isinstance(r,int):
            raise TypeError("Mul requires integer operands.")
        return l * r
    
    elif isinstance(expr,Eq):
        l = eval(expr.left,env)
        r = eval(expr.right,env)
        return l == r
    
    elif isinstance(expr,Lt):
        l - eval(expr.left,env)
        r = eval(expr.left,env)
        if not isinstance(l,int) or not isinstance(r,int):
            raise TypeError("Lt requires integer operands")