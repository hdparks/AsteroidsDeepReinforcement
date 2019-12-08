import torch
import torch.nn as nn
import numpy as np

class Squeeze(nn.Module):
    def __init__(self, d):
        super().__init__()
        self.d = d

    def forward(self, x):
        return x.squeeze(self.d)

class Flatten(nn.Module):
    def forward(self, x):
        return x.view(x.shape[0],-1)

# Policy Network
class PolicyNetwork(nn.Module):
    def __init__(self):
        super().__init__()

        self.net = nn.Sequential(nn.Conv3d(1,32,(2,6,6),stride = (1,2,2),padding =(0,2,2)), # (batch, 1, 2, 200, 200)
                                 nn.ReLU(),
                                 Squeeze(2), # (batch, 32, 1, 100,100 )
                                 nn.Conv2d(32, 32,(6,6), stride=2, padding=0), # (batch,32,100,100)
                                 nn.ReLU(),
                                 nn.Conv2d(32, 32,(6,6),stride=2,padding=0), # (batch,32,48,48)
                                 nn.ReLU(),
                                 nn.Conv2d(32, 32,(6,6),stride=2, padding=0), # (batch,32,22,22)
                                 nn.ReLU(),
                                 Flatten(), #(batch,32,9,9)
                                 nn.Linear(32 * 9 * 9,512), #(batch,1,2592)
                                 nn.ReLU()) # (batch,1,512)

        self.policy_head = nn.Sequential(nn.Linear(512,4), nn.Sigmoid())
        self.value_head = nn.Sequential(nn.Linear(512,1))

    def forward(self, x):
        """Get policy from state

        Args:
            state (tensor): current state, size (batch x state_size)

        Returns:
            a (tensor): tensor of binary actions to take
            adist (tensor): probability distribution over actions (batch x action_size)
            s (tensor): cudafied state tensor
        """
        out = self.net(x)
        return self.policy_head(out), self.value_head(out)

    def get_action(self, state):
        s = torch.cuda.FloatTensor(state/255).view(1,1,2,200,200)
        adist,_ = self(s)
        adist = np.array(adist.flatten().tolist())
        a = np.random.random(4) <= adist
        return a, adist
