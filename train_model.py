import pandas as pd
import matplotlib.pyplot as plt


# Load dataset
df = pd.read_csv("data/creditcard.csv")

print("Dataset Shape:", df.shape)

print("\nColumns:")
print(df.columns)

print("\nFraud Distribution:")
print(df["Class"].value_counts())

print("\nMissing Values:")
print(df.isnull().sum().sum())

print("\nDataset Info:")
print(df.info())

fraud_counts = df["Class"].value_counts()

plt.figure(figsize=(6,4))
fraud_counts.plot(kind="bar")

plt.title("Fraud vs Genuine Transactions")
plt.xlabel("Class")
plt.ylabel("Count")

plt.show()