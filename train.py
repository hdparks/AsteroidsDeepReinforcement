def train(network, iterations):
    """ Trains a policy network for a given number of iterations """
    # Hyper parameters
    lr = 1e-3
    epochs = 20
    experience_samples = 100
    gamma = 0.9
    batch_size = 256
    epsilon = 0.2
    policy_epochs = 5

    # Init optimizer
    optim = torch.optim.Adam(network.parameters(),lr=lr)

    # Start the main loop
    asteroids_destroyed = []
    loop = tqdm(total = epochs, position = 0, leave = False)
    for epoch in range(epochs):

         memory = [] # Reset memory after each epoch

         # Begin experience loop
         for episode in range(experience_samples):

             states, actions, 
