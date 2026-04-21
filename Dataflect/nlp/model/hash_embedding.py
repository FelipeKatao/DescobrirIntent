import torch
import torch.nn as nn


class HashEmbedding(nn.Module):
    """
    Torch-only text embedding using a hashing trick.

    - Maps token strings -> bucket ids (stable hash) -> embedding vectors.
    - Deterministic initialization via a fixed seed.
    """

    def __init__(self, num_buckets: int = 50000, dim: int = 300, seed: int = 42):
        super().__init__()
        self.num_buckets = int(num_buckets)
        self.dim = int(dim)
        self.seed = int(seed)

        g = torch.Generator()
        g.manual_seed(self.seed)
        weight = torch.randn(self.num_buckets, self.dim, generator=g) * 0.02
        self.embedding = nn.Embedding(self.num_buckets, self.dim)
        with torch.no_grad():
            self.embedding.weight.copy_(weight)

    @staticmethod
    def _stable_hash(s: str) -> int:
        # FNV-1a 32-bit
        h = 2166136261
        for b in s.encode("utf-8", errors="ignore"):
            h ^= b
            h = (h * 16777619) & 0xFFFFFFFF
        return h

    def token_to_id(self, token: str) -> int:
        return self._stable_hash(token) % self.num_buckets

    def forward(self, token_ids: torch.Tensor) -> torch.Tensor:
        """
        token_ids: LongTensor [T] or [B,T]
        returns: FloatTensor [T,D] or [B,T,D]
        """
        return self.embedding(token_ids)

