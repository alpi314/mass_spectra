import torch
import torch.nn as nn
import torch.nn.functional as F
from skorch import NeuralNet


# Underlying neural network in pytorch
class _NN(nn.Module):
    def __init__(self, input_size, output_size, dropout=0.5):
        super().__init__()
        # First layer
        self.ln1 = nn.Linear(input_size, input_size // 2).double()
        nn.init.kaiming_uniform_(self.ln1.weight, mode='fan_in', nonlinearity='relu') # He Initialization for ReLU
        self.dropout1 = nn.Dropout(p=dropout)
        self.activation1 = nn.ReLU().double()

        # Second layer
        self.ln2 = nn.Linear(input_size // 2, output_size).double()
        nn.init.xavier_uniform_(self.ln2.weight)  # Xavier/Glorot Initialization
        self.activation2 = nn.Sigmoid().double()

    def forward(self, x):
        x = self.ln1(x)
        x = self.dropout1(x)
        x = self.activation1(x)
        x = self.ln2(x)
        x = self.activation2(x)
        return x

# Wrapper class for skorch
class NN():
    def __init__(self, input_size, output_size, criterion, max_epochs=10, batch_size=32, lr=0.1, dropout=0.5, device='cpu', iterator_train__shuffle=True):
        self.model = NeuralNet(
            module=_NN,
            module__input_size=input_size,
            module__output_size=output_size,
            module__dropout=dropout,
            criterion=criterion,
            max_epochs=max_epochs,
            lr=lr,
            batch_size=batch_size,
            iterator_train__shuffle=iterator_train__shuffle,
            device=device,
            verbose=0,
            predict_nonlinearity=None,
        )

    def fit(self, X, y):
        self.model.fit(X, y)

    def predict_proba(self, X):
        return self.model.predict_proba(X)
    
    def predict(self, X):
        return self.predict_proba(X) > 0.5