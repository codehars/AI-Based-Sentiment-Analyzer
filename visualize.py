from pymongo import MongoClient
import matplotlib.pyplot as plt

client = MongoClient("mongodb://localhost:27017/")
db = client["sentiment_db"]
collection = db["results"]

data = list(collection.find())

sentiments = {"POSITIVE": 0, "NEGATIVE": 0}

for item in data:
    sentiments[item["sentiment"]] += 1

labels = sentiments.keys()
values = sentiments.values()

plt.bar(labels, values)
plt.title("Sentiment Analysis Results")
plt.xlabel("Sentiment")
plt.ylabel("Count")
plt.show()