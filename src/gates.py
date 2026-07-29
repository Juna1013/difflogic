from __future__ import annotations
import torch

__all__ = [
    "N_GATES", "GATE_NAMES", "TRUTH_TABLES",
    "truth_table", "gate_deps", "basic_terms", "sort_gates", "verilog_expr",
    "GATE_IDENITIY_A", "GATE_FALES", "GATE_TRUE",
]

N_GATES = 16
GATE_NAMES = [
    "FALSE", # 0b0000
    "AND", # 0b0001
    "A_AND_NOTB", # 0b0010
    "A", # 0b0011
    "NOTA_AND_B", # 0b0100
    "B", # 0b0101
    "XOR", # 0b0110
    "OR", # 0b0111
    "NOR", # 0b1000
    "XNOR", # 0b1001
    "NOTB", # 0b1010
    "A_OR_NOTB", # 0b1011
    "NOTA", # 0b1100
    "NOTA_OR_B", # 0b1101
    "NAND", # 0b1110
    "TRUE", # 0b1111
]

# よく参照するゲート
GATE_FALSE = 0
GATE_IDENITIY_A = 3 # 恒等ゲート、df/da = 1 なので勾配を素通しする
GATE_TEUR = 15

def truth_table(i: int) -> tuple[int, int, int, int]:
    # ゲート番号 -> (T00, T01, T10, T11)
    return tuple((i >> b) & 1 for b in (3, 2, 1, 0))

def gate_deps(i: int) -> tuple[bool, bool]:
    t00, t01, t10, t11 = truth_table(i)
    return ((t00, t01) != (t10, t11), (t00, t10) != (t01, t11))

# [16, 4] の真理値表テーブル
TRUTH_TABLES = torch.tensor(
    [truth_table(i) for i in range(N_GATES)], dtype=torch.float32
)

def basis_terms(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
    return torch.stack([
        (1 - a) * (1 - b),
        (1 - a) * b,
        a * (1 - b),
        a * b,
    ], dim=-1)

def soft_gates(a: torch.Tensorm, b: torch.Tensor) -> torch.Tensor:
    basis = basis_terms(a, b) # [B, N, 4]
    table = TRUTH_TABLES.to(basis.device, basis.dtype)
    return basis @ table.T # [B, N, 16]

# Verilog 出力用
_VERILOG_TEMPLATES = [
    "1'b0", "({a} & {b})", "({a} & ~{b})", "{a}",
    "(~{a} & {b})", "{b}", "({a} ^ {b})", "({a} | {b})",
    "~({a} | {b})", "~({a} ^ {b})", "~{b}", "({a} | ~{b})",
    "~{a}", "(~{a} | {b})", "~({a} & {b})", "1'b1",
]

def verilog_expr(gate: int, a: str, b:str) -> str:
    # ゲート番号と入力信号名から Verilog 式をつくる
    return _VERILOG_TEMPLATES[gate].format(a=a, b=b)
