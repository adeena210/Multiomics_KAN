# %%
import torch
import torch.nn as nn
import torch.nn.functional as F
from preprocessing import preprocess


# %%
class VAE(nn.Module):
    def __init__(self, input_dim, hidden_dim=400, latent_dim=20):
        super(VAE, self).__init__()

        # Encoder layers
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc21 = nn.Linear(hidden_dim, latent_dim)  # Mean of the latent space
        self.fc22 = nn.Linear(hidden_dim, latent_dim)  # Log variance of the latent space

        # Decoder layers
        self.fc3 = nn.Linear(latent_dim, hidden_dim)
        self.fc4 = nn.Linear(hidden_dim, input_dim)

    def encode(self, x):
        h1 = F.relu(self.fc1(x))
        return self.fc21(h1), self.fc22(h1)

    def reparametrize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)  # Sample from standard normal distribution
        return mu + eps * std

    def decode(self, z):
        h3 = F.relu(self.fc3(z))
        return torch.sigmoid(self.fc4(h3))

    def forward(self, x):
        mu, logvar = self.encode(x.view(-1, 784))
        z = self.reparametrize(mu, logvar)
        return self.decode(z), mu, logvar

    def loss_function(recon_x, x, mu, logvar):
        recon_loss = F.binary_cross_entropy(recon_x, x, reduction='sum')
        kl_loss = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
        return recon_loss + kl_loss


# %%
def train(model: VAE, epochs, trainloader):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    model.train()
    # training loop
    for epoch in epochs:
        train_loss = 0
        for batch_idx, (data,) in enumerate(trainloader):
            data = data.to(device)
            optimizer.zero_grad()
            recon_batch, mu, logvar = model(data)
            loss = model.loss_function(recon_batch, data, mu, logvar)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
        print(f'Epoch {epoch + 1}, Loss: {train_loss / len(trainloader.dataset):.4f}')

# %%
# Data loading
input_path = "./data/exprMatrix.tsv"
meta_path = "./data/meta.tsv"
trainloader, input_dim = preprocess(input_path, meta_path)
vae = VAE(input_dim=input_dim)

train(vae, 1, trainloader)
