import torch
import torch.nn as nn


class SemanticValidator(nn.Module):

    def __init__(self):

        super().__init__()

        self.network = nn.Sequential(

            nn.Linear(
                300,
                128
            ),

            nn.ReLU(),

            nn.Linear(
                128,
                2
            )

        )

    def forward(self, x):

        return self.network(x)