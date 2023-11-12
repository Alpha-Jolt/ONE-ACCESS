import numpy as np
from random import randint

def generate_vault(secret, num_points):
    # Generate a random set of points as the vault
    vault = [(randint(0, 1000000), randint(0, 1000000)) for _ in range(num_points)]

    # Encrypt the secret and add it to the vault
    vault.append(secret)

    return vault

def unlock_vault(vault, biometric_sample, threshold):
    # Filter out points from the vault that are close to the biometric sample
    close_points = [point for point in vault if distance(point, biometric_sample) <= threshold]

    # Retrieve the secret if there are enough close points
    if len(close_points) >= threshold + 1:
        return close_points[-1]  # The last element is the secret
    else:
        return None

def distance(point1, point2):
    # Calculate Euclidean distance between two points
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

# Take inputs from the user
secret_key = tuple(map(int, input("Enter secret key (x, y): ").split(',')))
biometric_sample = tuple(map(int, input("Enter biometric sample (x, y): ").split(',')))
threshold_value = int(input("Enter threshold value: "))

vault = generate_vault(secret_key, (2**16))
print("Vault:", vault)

retrieved_secret = unlock_vault(vault, biometric_sample, threshold_value)

if retrieved_secret is not None:
    print("Unlock successful. Retrieved secret:", retrieved_secret)
else:
    print("Unlock failed. Biometric sample does not match.")

# Session Storage for Biometrics of user
# Part of Tag Algorithm
