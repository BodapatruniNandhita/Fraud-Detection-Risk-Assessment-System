import pandas as pd

# Load dataset
df = pd.read_csv("data/creditcard.csv")

print("Dataset Shape:", df.shape)

print("\nColumns:")
print(df.columns)

