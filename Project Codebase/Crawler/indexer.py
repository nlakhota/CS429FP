import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the JSON data from the file
with open('Crawler\data\output.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Initialize a dictionary to store product descriptions
product_descriptions = {}

# Extract product descriptions for each book
for index, book in enumerate(data):
    description = book['product description']
    product_descriptions[index] = description

# Output the dictionary to a text file
output_file = 'Crawler\\data\\product_descriptions.txt'
with open(output_file, 'w', encoding='utf-8') as f:
    for title, description in product_descriptions.items():
        f.write(f"{title}\nProduct Description: {description}\n\n")

print("Product descriptions have been saved to:", output_file)

#############################################################################################################################

# Function to tokenize documents
def tokenize_documents(documents):
    tokenized_documents = []
    for doc in documents:
        description = doc['product description']  # Extracting product description
        # Remove punctuation and special characters
        cleaned_text = re.sub(r'[^\w\s]', '', description)
        # Split the text using whitespace as a delimiter
        tokens = cleaned_text.split()
        tokenized_documents.append(tokens)
    return tokenized_documents

# Tokenize the product descriptions
tokenized_product_descriptions = tokenize_documents(data)

def inverted_ind(tokenized_data):
    inverted_index = {}
    for i in range(len(tokenized_data)):
        for tokens in tokenized_data[i]:
            if tokens not in inverted_index:
                inverted_index[tokens] = [i+1]
            elif i+1 not in inverted_index[tokens]:
                inverted_index[tokens].append(i+1)

    return inverted_index

inverted_index = inverted_ind(tokenized_product_descriptions)

file_path = 'Crawler\\data\\inverted_index.txt'

with open(file_path, 'w', encoding="utf-8") as f:
    for token, postings in inverted_index.items():
        f.write(f"{token}: {postings}\n")

#############################################################################################################################

# Convert tokenized documents to strings
document_strings = [' '.join(tokens) for tokens in tokenized_product_descriptions]

# Initialize TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer()

# Compute TF-IDF representation
tfidf_matrix = tfidf_vectorizer.fit_transform(document_strings)

# Get feature names (words)
feature_names = tfidf_vectorizer.get_feature_names_out()

# Output TF-IDF scores to a text file
tfidf_output_file = 'Crawler\\data\\tfidf_scores.txt'
with open(tfidf_output_file, 'w', encoding='utf-8') as f:
    for i, row in enumerate(tfidf_matrix):
        f.write(f"TF-IDF weights for Document {i}:\n")
        for j, weight in enumerate(row.toarray()[0]):
            if weight != 0:
                f.write(f"    {feature_names[j]}: {weight}\n")
        f.write("\n")

print("TF-IDF scores have been saved to:", tfidf_output_file)

# Prompt the user for document indices
doc1_index = int(input("Enter index of first document: "))
doc2_index = int(input("Enter index of second document: "))

# Compute cosine similarity
cosine_similarity_docs = cosine_similarity(tfidf_matrix[doc1_index], tfidf_matrix[doc2_index])
print(f"Cosine Similarity between document {doc1_index} and document {doc2_index}: {cosine_similarity_docs}")

#############################################################################################################################