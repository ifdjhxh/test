import ast
from enum import Enum


class SignType(Enum):
    Eq = ast.Eq()
    NotEq = ast.NotEq()
    Lt = ast.Lt()
    LtE = ast.LtE()
    Gt = ast.Gt()
    GtE = ast.GtE()
