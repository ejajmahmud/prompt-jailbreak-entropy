"""Shannon entropy and symbol anomaly detection for adversarial prompt defense."""
import math
from collections import Counter
from typing import Dict, Any, Tuple


class EntropyGuard:
    def __init__(self, max_entropy: float = 4.75, max_symbol_ratio: float = 0.30):
        self.max_entropy = max_entropy
        self.max_symbol_ratio = max_symbol_ratio

    @staticmethod
    def calculate_shannon_entropy(text: str) -> float:
        if not text:
            return 0.0
        counts = Counter(text)
        length = len(text)
        entropy = 0.0
        for count in counts.values():
            p = count / length
            entropy -= p * math.log2(p)
        return round(entropy, 4)

    def evaluate(self, text: str) -> Tuple[bool, Dict[str, Any]]:
        entropy = self.calculate_shannon_entropy(text)
        total_chars = len(text)
        if total_chars == 0:
            return True, {"entropy": 0.0, "symbol_ratio": 0.0, "reason": "Empty string"}

        symbols = sum(1 for c in text if not c.isalnum() and not c.isspace())
        symbol_ratio = round(symbols / total_chars, 4)

        is_suspicious = False
        reasons = []

        if entropy > self.max_entropy and total_chars > 20:
            is_suspicious = True
            reasons.append(f"Excessive Shannon entropy ({entropy} > {self.max_entropy}) indicating cipher or base64")

        if symbol_ratio > self.max_symbol_ratio and total_chars > 15:
            is_suspicious = True
            reasons.append(f"Excessive symbol density ({symbol_ratio} > {self.max_symbol_ratio}) indicating delimiter attack")

        return not is_suspicious, {
            "is_safe": not is_suspicious,
            "entropy": entropy,
            "symbol_ratio": symbol_ratio,
            "reasons": reasons
        }
