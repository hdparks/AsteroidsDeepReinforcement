from rollout import rollout
from visualize import visualize
from torch.utils.data import DataLoader
from rldataset import RLDataset
import torch as torch
import torch.nn as nn
from tqdm import tqdm

def train(network, iterations):
    """ Trains a policy network for a given number of iterations """
    # Hyper parameters
    lr = 1e-3
    experience_samples = 10 #10
    gamma = 0.9
    batch_size = 256
    epsilon = 0.02
    policy_epochs = 1 #5

    # Init optimizer
    optim = torch.optim.Adam(network.parameters(),lr=lr)

    # Start the main loop
    asteroids_destroyed = []
    losses = []
    framerates = []
    loop = tqdm(total = iterations, position = 0, leave = False)
    for epoch in range(iterations):
        visualize(network)
        memory = [] # Reset memory after each epoch

        # Begin experience loop
        for episode in range(experience_samples):

            roll, destroyed, playtime, fr = rollout(network)
            # Calculate returns and add episode to memory

            dsr = 0 # Discounted Sum of Rewards
            for s,a,a_dict,r in reversed(roll):
                dsr = r + gamma * dsr
                memory.append((s,a,a_dict,dsr))

            asteroids_destroyed.append(destroyed)
            framerates.append(fr)

            loop.set_description("Rollout: {}, Destryed: {}, Frame Rate: {}".format(episode,destroyed,fr))

        # Train
        dataset = RLDataset(memory)

        loader = DataLoader(dataset, batch_size = batch_size, shuffle= True)

        for _ in range(policy_epochs):
            for s, a, a_dist, r, in loader:
                optim.zero_grad()
                state = s.float().cuda()
                r = r.float().cuda().unsqueeze(-1)
                a = a.bool().cuda()
                a_dist = a_dist.float().cuda()

                p,v = network(state.unsqueeze(1))
                v_loss = nn.functional.mse_loss(v,r)
                advantage = r - v
                advantage = advantage.detach()

                c_prob = p * a + (1 - p) * ~a
                old_prob = a_dist * a + (1 - a_dist) * ~a
                ratio = c_prob / old_prob

                p_loss = -1 * torch.min(ratio * advantage, torch.clamp(ratio, 1-epsilon, 1+epsilon) * advantage)
                p_loss = p_loss.mean()

                loss = p_loss + v_loss
                losses.append(loss.item())
                loss.backward()
                optim.step()


        loop.update(1)
        loop.set_description("Epoch: {} Asteroids Destroyed: {} Frame Rate: {} Loss: {} ".format(epoch,asteroids_destroyed[-1], framerates[-1], loss.item()))

    return asteroids_destroyed, losses
