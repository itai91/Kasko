from typing import Optional


def is_valid_israeli_id(id_number: str) -> bool:
    # Simple checksum validation for Israeli ID (9 digits)
    if not id_number.isdigit() or len(id_number) != 9:
        return False
    total = 0
    for i, ch in enumerate(id_number):
        num = int(ch) * (1 if i % 2 == 0 else 2)
        if num > 9:
            num = (num // 10) + (num % 10)
        total += num
    return total % 10 == 0


def safe_float(v: Optional[float]) -> float:
    return float(v or 0.0)

