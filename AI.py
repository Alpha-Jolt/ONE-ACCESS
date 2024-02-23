import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# X should be a 3D array with dimensions: (samples, time steps, features)
# y should be a binary array indicating genuine (0) or impostor (1)

''' # Example data loading (replace this with your actual data loading code)
X, y = load_data()'''

# Example data preprocessing
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert data to PyTorch tensors
X_train_tensor = torch.Tensor(X_train)
y_train_tensor = torch.Tensor(y_train)
X_test_tensor = torch.Tensor(X_test)
y_test_tensor = torch.Tensor(y_test)

# Create DataLoader
train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# Define the LSTM model
class KeystrokeLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(KeystrokeLSTM, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        _, (h_n, _) = self.lstm(x)
        output = self.fc(h_n[-1, :, :])
        output = self.sigmoid(output)
        return output

# Initialize the model
input_size = X_train.shape[2]
hidden_size = 50
output_size = 1
model = KeystrokeLSTM(input_size, hidden_size, output_size)

# Define loss function and optimizer
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training the model
num_epochs = 47
for epoch in range(num_epochs):
    for batch_X, batch_y in train_loader:
        optimizer.zero_grad()
        output = model(batch_X)
        loss = criterion(output.squeeze(), batch_y)
        loss.backward()
        optimizer.step()

# Evaluation
with torch.no_grad():
    model.eval()
    y_pred = model(X_test_tensor).squeeze().numpy()
    predictions = (y_pred > 0.5).astype(int)
    accuracy = (predictions == y_test).mean()

print(f'Test Accuracy: {accuracy}')

