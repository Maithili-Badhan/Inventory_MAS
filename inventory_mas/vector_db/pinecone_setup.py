import pinecone
import pandas as pd
import numpy as np

# Initialize Pinecone
pinecone.init(api_key="pcsk_4Jff6e_B6p5LaEL6X61gEjtx8oh1pUBLeXwjpB7B5QumhfuQhL6gtSFdyLSBfMHzFgQVsm", environment="us-east1-gcp")

# Create or connect to an index
index_name = "inventory-db"
if index_name not in pinecone.list_indexes():
    pinecone.create_index(index_name, dimension=9, metric="cosine")  # Adjust dimension based on your vectors

index = pinecone.Index(index_name)

# Load Sample Data
data = [
    {"Product ID": 4277, "Store ID": 48, "Sales Quantity": 330, "Price": 24.38, "Promotions": "No", 
     "Seasonality Factors": "Festival", "External Factors": "Competitor Pricing", "Demand Trend": "Increasing", "Customer Segments": "Regular"},
    
    {"Product ID": 5406, "Store ID": 67, "Sales Quantity": 429, "Price": 24.83, "Promotions": "No", 
     "Seasonality Factors": "Holiday", "External Factors": "Economic Indicator", "Demand Trend": "Decreasing", "Customer Segments": "Premium"},
    
    {"Product ID": 7767, "Store ID": 64, "Sales Quantity": 71, "Price": 15.8, "Promotions": "Yes", 
     "Seasonality Factors": "Festival", "External Factors": "Competitor Pricing", "Demand Trend": "Decreasing", "Customer Segments": "Regular"}
]

# Convert Categorical Variables into One-Hot Encoding
df = pd.DataFrame(data)
df = pd.get_dummies(df, columns=["Promotions", "Seasonality Factors", "External Factors", "Demand Trend", "Customer Segments"])

# Prepare Data for Pinecone
vectors = df.drop(columns=["Product ID", "Store ID"]).values.tolist()
ids = df["Product ID"].astype(str).tolist()

# Upload Vectors to Pinecone
pinecone_vectors = [{"id": ids[i], "values": vectors[i]} for i in range(len(vectors))]
index.upsert(vectors=pinecone_vectors)

print("Data Uploaded Successfully to Pinecone!")

# Function to Query Pinecone
def query_pinecone(item_id):
    response = index.fetch([item_id])
    return response