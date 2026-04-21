import re
import unicodedata
from dataclasses import dataclass
from typing import Iterable, List


_RE_URL = re.compile(r"\bhttps?://[^\s]+\b", re.IGNORECASE)
_RE_EMAIL = re.compile(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", re.IGNORECASE)
_RE_TOKEN = re.compile(
    r"https?://[^\s]+|[\wÀ-ÿ]+(?:['’][\wÀ-ÿ]+)?|[^\s\w]",
    re.UNICODE,
)


def normalize_text(text: str) -> str:
    text = text.strip()
    # Normalize unicode and spacing without changing meaning too much.
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"\s+", " ", text)
    return text


def strip_accents(text: str) -> str:
    return "".join(
        ch
        for ch in unicodedata.normalize("NFKD", text)
        if unicodedata.category(ch) != "Mn"
    )


def split_sentences_simple(text: str) -> List[str]:
    text = normalize_text(text)
    if not text:
        return []
    # Split on sentence-ending punctuation, keep it attached.
    parts = re.split(r"(?<=[\.\!\?])\s+", text)
    sentences = [p.strip() for p in parts if p and p.strip()]
    return sentences


def tokenize(text: str) -> List[str]:
    text = normalize_text(text)
    if not text:
        return []
    return _RE_TOKEN.findall(text)


def is_url(token: str) -> bool:
    return bool(_RE_URL.fullmatch(token))


def is_email(token: str) -> bool:
    return bool(_RE_EMAIL.fullmatch(token))


@dataclass(frozen=True)
class Token:
    text: str

    @property
    def lower_(self) -> str:
        return self.text.lower()

    @property
    def lemma_(self) -> str:
        # Very light "lemma": lowercase + remove accents.
        return strip_accents(self.text.lower())


@dataclass(frozen=True)
class Entity:
    text: str
    label: str


class Doc:
    def __init__(self, text: str):
        self.text = normalize_text(text)
        self._sentences = split_sentences_simple(self.text)
        self._tokens = [Token(t) for t in tokenize(self.text)]
        self.ents: List[Entity] = []
        self.vector = None  # filled by vectorizer when needed

    def __iter__(self) -> Iterable[Token]:
        return iter(self._tokens)

    @property
    def sents(self) -> Iterable["Span"]:
        for s in self._sentences:
            yield Span(s)


@dataclass(frozen=True)
class Span:
    text: str

