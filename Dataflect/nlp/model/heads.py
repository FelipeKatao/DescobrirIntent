import torch
import torch.nn as nn


class TokenRelevanceHead(nn.Module):
    """
    Token-level relevance scoring.
    Uses simple handcrafted features + a small MLP.
    """

    def __init__(self, in_dim: int = 6, hidden: int = 16):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, 1),
        )

        # Bias towards "not relevant" unless evidence exists.
        with torch.no_grad():
            for m in self.net:
                if isinstance(m, nn.Linear):
                    nn.init.normal_(m.weight, mean=0.0, std=0.2)
                    nn.init.constant_(m.bias, 0.0)

            self.net[0].weight[:, 0].add_(0.8)  # length_norm
            self.net[0].weight[:, 1].add_(0.4)  # is_alpha
            self.net[0].weight[:, 2].add_(0.3)  # is_title

    def forward(self, feats: torch.Tensor) -> torch.Tensor:
        """
        feats: FloatTensor [T, F]
        returns logits: FloatTensor [T]
        """
        return self.net(feats).squeeze(-1)


class SyntaxCorrectnessHead(nn.Module):
    def __init__(self, in_dim: int = 5, hidden: int = 16):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, 2),
        )
        with torch.no_grad():
            for m in self.net:
                if isinstance(m, nn.Linear):
                    nn.init.normal_(m.weight, mean=0.0, std=0.2)
                    nn.init.constant_(m.bias, 0.0)
            self.net[0].weight[:, 1].add_(0.7)  
            self.net[0].weight[:, 2].add_(0.4)  

    def forward(self, feats: torch.Tensor) -> torch.Tensor:
        return self.net(feats)

