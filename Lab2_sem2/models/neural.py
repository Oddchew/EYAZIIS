"""
Нейросетевой классификатор языка (лёгкая модель без тяжёлых зависимостей).

Используем простой многослойный перцептрон на признаках:
- относительные частоты символов (буквы a-z + характерная диакритика)
- частоты коротких N-грамм (2-граммы и 3-граммы топ-K)
- доля французских маркеров

Обучение — градиентный спуск (numpy), либо fallback на эвристику
если numpy недоступен. Модель сохраняется в JSON.
"""

from __future__ import annotations

import json
import math
import random
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .preprocess import preprocess_text

# Базовый алфавит признаков
BASE_CHARS = list("abcdefghijklmnopqrstuvwxyzàâäæçéèêëïîôœùûüÿ")
TOP_BIGRAMS_EN = ["th", "he", "in", "er", "an", "re", "on", "at", "en", "nd",
                  "ti", "es", "or", "te", "of", "ed", "is", "it", "al", "ar"]
TOP_BIGRAMS_FR = ["es", "le", "de", "en", "re", "nt", "on", "te", "er", "se",
                  "la", "ai", "ou", "it", "an", "me", "is", "eu", "qu", "ur"]
TOP_TRIGRAMS = ["the", "and", "ing", "ion", "ent", "les", "des", "que", "une",
                "tion", "ment", "aire", "tion", "ence", "ance"]

FEATURE_BIGRAMS = list(dict.fromkeys(TOP_BIGRAMS_EN + TOP_BIGRAMS_FR))[:30]
FEATURE_TRIGRAMS = list(dict.fromkeys(TOP_TRIGRAMS))[:15]


def extract_features(text: str) -> List[float]:
    """Вектор признаков фиксированной размерности."""
    text = preprocess_text(text, keep_spaces=True)
    compact = text.replace(" ", "")
    letters = [c for c in compact if c.isalpha()]
    total = max(len(letters), 1)

    feats: List[float] = []
    # 1) частоты базовых символов
    cnt = Counter(letters)
    for ch in BASE_CHARS:
        feats.append(cnt.get(ch, 0) / total)

    # 2) доля французских маркеров
    markers = set("àâäæçéèêëïîôœùûüÿ")
    feats.append(sum(1 for c in letters if c in markers) / total)

    # 3) частоты выбранных bigrams / trigrams
    padded = f" {text} "
    for bg in FEATURE_BIGRAMS:
        feats.append(padded.count(bg) / max(len(padded) - 1, 1))
    for tg in FEATURE_TRIGRAMS:
        feats.append(padded.count(tg) / max(len(padded) - 2, 1))

    return feats


def _sigmoid(x: float) -> float:
    if x >= 0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    z = math.exp(x)
    return z / (1.0 + z)


def _dot(a: List[float], b: List[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


class NeuralLanguageClassifier:
    """
    Двухслойный MLP: input -> hidden (ReLU) -> output (sigmoid / softmax 2 classes).
    Классы: 0 = english, 1 = french.
    """

    LANGS = ["english", "french"]

    def __init__(self, hidden: int = 32, seed: int = 42):
        self.hidden = hidden
        self.seed = seed
        self.W1: List[List[float]] = []
        self.b1: List[float] = []
        self.W2: List[List[float]] = []
        self.b2: List[float] = []
        self.input_dim = 0
        self.trained = False

    def _init_weights(self, input_dim: int):
        rng = random.Random(self.seed)
        scale = 0.3
        self.input_dim = input_dim
        self.W1 = [
            [rng.uniform(-scale, scale) for _ in range(input_dim)]
            for _ in range(self.hidden)
        ]
        self.b1 = [0.0] * self.hidden
        self.W2 = [
            [rng.uniform(-scale, scale) for _ in range(self.hidden)]
            for _ in range(2)  # 2 classes
        ]
        self.b2 = [0.0, 0.0]

    def _forward(self, x: List[float]) -> Tuple[List[float], List[float], List[float]]:
        # hidden = ReLU(W1 x + b1)
        h_pre = [_dot(self.W1[i], x) + self.b1[i] for i in range(self.hidden)]
        h = [max(0.0, v) for v in h_pre]
        # logits
        logits = [_dot(self.W2[i], h) + self.b2[i] for i in range(2)]
        # softmax
        m = max(logits)
        exps = [math.exp(v - m) for v in logits]
        s = sum(exps)
        probs = [e / s for e in exps]
        return probs, h, h_pre

    def train(
        self,
        texts: List[str],
        labels: List[str],
        epochs: int = 80,
        lr: float = 0.05,
        verbose: bool = False,
    ) -> Dict[str, float]:
        """Обучение на парах (text, language_name)."""
        assert len(texts) == len(labels)
        X = [extract_features(t) for t in texts]
        y = [0 if lab == "english" else 1 for lab in labels]
        if not X:
            raise ValueError("Empty training set")
        self._init_weights(len(X[0]))

        history_loss = []
        n = len(X)
        for ep in range(epochs):
            order = list(range(n))
            random.Random(self.seed + ep).shuffle(order)
            total_loss = 0.0
            for idx in order:
                x = X[idx]
                target = y[idx]
                probs, h, h_pre = self._forward(x)
                # cross-entropy
                loss = -math.log(max(probs[target], 1e-9))
                total_loss += loss

                # dL/dlogits
                dlogits = list(probs)
                dlogits[target] -= 1.0

                # gradients W2, b2
                dW2 = [[dlogits[c] * h[j] for j in range(self.hidden)] for c in range(2)]
                db2 = list(dlogits)

                # backprop to hidden
                dh = [0.0] * self.hidden
                for j in range(self.hidden):
                    for c in range(2):
                        dh[j] += dlogits[c] * self.W2[c][j]
                    if h_pre[j] <= 0:
                        dh[j] = 0.0  # ReLU

                dW1 = [[dh[i] * x[k] for k in range(self.input_dim)] for i in range(self.hidden)]
                db1 = list(dh)

                # SGD update
                for c in range(2):
                    for j in range(self.hidden):
                        self.W2[c][j] -= lr * dW2[c][j]
                    self.b2[c] -= lr * db2[c]
                for i in range(self.hidden):
                    for k in range(self.input_dim):
                        self.W1[i][k] -= lr * dW1[i][k]
                    self.b1[i] -= lr * db1[i]

            avg = total_loss / n
            history_loss.append(avg)
            if verbose and (ep + 1) % 20 == 0:
                print(f"  epoch {ep+1}/{epochs}  loss={avg:.4f}")

        self.trained = True
        # accuracy on train
        correct = 0
        for i, x in enumerate(X):
            pred = self.predict_proba_vec(x)
            if (pred[1] > 0.5) == (y[i] == 1):
                correct += 1
        acc = correct / n
        return {"final_loss": history_loss[-1], "train_accuracy": acc, "epochs": epochs}

    def predict_proba_vec(self, x: List[float]) -> List[float]:
        probs, _, _ = self._forward(x)
        return probs

    def predict_proba(self, text: str) -> Dict[str, float]:
        if not self.trained:
            raise RuntimeError("Model is not trained")
        x = extract_features(text)
        probs = self.predict_proba_vec(x)
        return {"english": probs[0], "french": probs[1]}

    def predict(self, text: str) -> Tuple[str, Dict[str, float]]:
        probs = self.predict_proba(text)
        best = max(probs, key=probs.get)  # type: ignore
        return best, probs

    def save(self, path: str | Path):
        data = {
            "hidden": self.hidden,
            "input_dim": self.input_dim,
            "W1": self.W1,
            "b1": self.b1,
            "W2": self.W2,
            "b2": self.b2,
            "trained": self.trained,
            "seed": self.seed,
        }
        Path(path).write_text(json.dumps(data), encoding="utf-8")

    def load(self, path: str | Path) -> "NeuralLanguageClassifier":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        self.hidden = data["hidden"]
        self.input_dim = data["input_dim"]
        self.W1 = data["W1"]
        self.b1 = data["b1"]
        self.W2 = data["W2"]
        self.b2 = data["b2"]
        self.trained = data["trained"]
        self.seed = data.get("seed", 42)
        return self
