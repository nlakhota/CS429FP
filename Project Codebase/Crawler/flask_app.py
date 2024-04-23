# Flask application code (flask_app.py)
from flask import Flask, request, jsonify
import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load the JSON data from the file
with open('Crawler\\data\\output.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Function to tokenize documents
def tokenize_documents(documents):
    tokenized_documents = []
    for doc in documents:
        description = doc['product description']
        cleaned_text = re.sub(r'[^\w\s]', '', description)
        tokens = cleaned_text.split()
        tokenized_documents.append(tokens)
    return tokenized_documents

# Tokenize the product descriptions
tokenized_product_descriptions = tokenize_documents(data)

# Initialize TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform([' '.join(tokens) for tokens in tokenized_product_descriptions])

k1 = None  # Initialize k1

# Prompt user for input only if k1 is not set
if k1 is None:
    k1 = int(input("k? : "))

# Function to process queries
def process_query(query, k=k1):
    # Tokenize query
    query_tokens = re.sub(r'[^\w\s]', '', query).split()
    # Compute TF-IDF representation of the query
    query_tfidf = tfidf_vectorizer.transform([query])

    # Compute cosine similarity between query and documents
    similarities = cosine_similarity(query_tfidf, tfidf_matrix)[0]

    # Get indices of top-K similar documents
    top_indices = similarities.argsort()[-k:][::-1]

    # Get top-K results
    results = [{'title': data[i]['title'], 'description': data[i]['product description']} for i in top_indices]

    return results

@app.route('/query', methods=['POST'])
def handle_query():
    query_data = request.get_json()
    if 'query' not in query_data:
        return jsonify({'error': 'Query not found in request'}), 400

    query = query_data['query']
    if not query:
        return jsonify({'error': 'Empty query'}), 400

    # Process the query
    results = process_query(query)

    # Write the results to a JSON file
    write_results_to_json(results, 'query_results')

    return jsonify({'results': results})

def write_results_to_json(results, filename):
    """
    Write the results to a JSON file.
    
    Args:
    - results (list): List of dictionaries containing the results.
    - filename (str): Name of the JSON file to write.
    """
    filepath = f'Crawler\\data\\{filename}.json'  # Path to the JSON file
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(results, file, indent=4)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
