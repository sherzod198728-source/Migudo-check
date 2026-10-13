"""Oddiy kalkulyator.

Ishga tushirish:  python kalkulyator.py
Misollar:  2 + 3 * 4,  (10 - 4) / 3,  2 ** 10,  17 % 5
Chiqish uchun:  q
"""

import ast
import operator

AMALLAR = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _hisobla(tugun):
    if isinstance(tugun, ast.Constant) and isinstance(tugun.value, (int, float)):
        return tugun.value
    if isinstance(tugun, ast.BinOp) and type(tugun.op) in AMALLAR:
        chap, ong = _hisobla(tugun.left), _hisobla(tugun.right)
        if isinstance(tugun.op, ast.Pow) and abs(ong) > 1000:
            raise ValueError("daraja juda katta")
        return AMALLAR[type(tugun.op)](chap, ong)
    if isinstance(tugun, ast.UnaryOp) and type(tugun.op) in AMALLAR:
        return AMALLAR[type(tugun.op)](_hisobla(tugun.operand))
    raise ValueError("faqat sonlar va + - * / // % ** ( ) ishlatish mumkin")


def hisobla(ifoda):
    """Matndagi ifodani hisoblaydi, masalan "2 + 3 * 4" -> 14."""
    ifoda = ifoda.replace(",", ".").replace("x", "*").replace("×", "*").replace(":", "/")
    natija = _hisobla(ast.parse(ifoda, mode="eval").body)
    if isinstance(natija, float) and natija.is_integer():
        natija = int(natija)
    return natija


def main():
    print("Kalkulyator. Ifoda kiriting (masalan: 2 + 3 * 4). Chiqish: q")
    while True:
        try:
            ifoda = input(">>> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if ifoda.lower() in ("q", "chiqish", "exit"):
            break
        if not ifoda:
            continue
        try:
            print("=", hisobla(ifoda))
        except ZeroDivisionError:
            print("Xato: nolga bo'lish mumkin emas")
        except SyntaxError:
            print("Xato: ifoda noto'g'ri yozilgan")
        except (ValueError, OverflowError) as e:
            print("Xato:", e)
    print("Xayr!")


if __name__ == "__main__":
    main()
