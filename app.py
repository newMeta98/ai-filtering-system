import logging
import os
import json
from flask import Flask, request, render_template, flash
from utils.api_client import product_filterLLM

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.getenv('SECRET_KEY')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load product titles from products.txt
def load_product_titles(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:  # Specify encoding here
            print("\nproduct_titles loaded\n")
            # Read the file and split by newlines
            titles = [title.strip() for title in file.read().splitlines() if title.strip()]
            print(titles)  # Print the loaded titles for debugging
            return titles
    except Exception as e:
        logging.error(f"Failed to load product titles: {e}")
        return []

# Load all knowledge files from the knowledge directory
def load_all_knowledge(knowledge_dir):
    knowledge_files = os.listdir(knowledge_dir)
    knowledge_data = {}
    for file in knowledge_files:
        if file.endswith(".txt"):
            try:
                with open(os.path.join(knowledge_dir, file), 'r') as f:
                    knowledge_data[file] = f.read()
            except Exception as e:
                logging.error(f"Failed to load knowledge file {file}: {e}")
    print("\nall_knowledge loaded\n")
    return knowledge_data

# Function to append data to data.json
def append_to_json(data, file_path='data.json'):
    try:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    existing_data = json.load(f)
            except json.JSONDecodeError:
                # If the file is empty or contains invalid JSON, initialize with default data
                existing_data = {"product_titles": [], "restricted_products": [], "allowed_products": []}
        else:
            existing_data = {"product_titles": [], "restricted_products": [], "allowed_products": []}

        # Avoid duplicates when appending
        for key in ["product_titles", "restricted_products", "allowed_products"]:
            existing_data[key].extend([item for item in data.get(key, []) if item not in existing_data[key]])

        with open(file_path, 'w') as f:
            json.dump(existing_data, f, indent=4)
    except Exception as e:
        logging.error(f"Failed to append data to {file_path}: {e}")

# Function to load data from data.json
def load_from_json(file_path='data.json'):
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        else:
            return {"product_titles": [], "restricted_products": [], "allowed_products": []}
    except json.JSONDecodeError:
        # If the file is empty or contains invalid JSON, initialize with default data
        return {"product_titles": [], "restricted_products": [], "allowed_products": []}
    except Exception as e:
        logging.error(f"Failed to load data from {file_path}: {e}")
        return {"product_titles": [], "restricted_products": [], "allowed_products": []}

@app.route('/', methods=['GET', 'POST'])
def index():
    product_titles = []

    if request.method == 'POST':
        # Get product titles from user input
        user_input = request.form['product_titles']
        if user_input.strip():  # Check if input is not empty
            product_titles = [title.strip() for title in user_input.split('\n') if title.strip()]
        else:
            # If input is empty, load titles from products.txt
            product_titles = load_product_titles('products.txt')

        # Load all knowledge files
        knowledge_data = load_all_knowledge('knowledge')

        # Process product titles in batches of 50
        if product_titles and knowledge_data:
            print("\nloop starting\n")
            for i in range(0, len(product_titles), 50):  # Change batch size to 50
                batch = product_titles[i:i + 50]  # Change batch size to 50
                batch_restricted_titles = set()  # Track restricted titles for this batch
                batch_allowed_titles = []  # Track allowed titles for this batch

                for file, knowledge in knowledge_data.items():
                    print(f"\nfile:{file}\n")
                    # Send batch of product titles
                    message = "\n".join(batch)
                    response = product_filterLLM(message, knowledge)
                    if response and "restricted_products" in response:
                        batch_restricted_titles.update(response["restricted_products"])  # Add to set
                        print(f"\nrestricted_products:{response['restricted_products']}\n")
                    else:
                        flash(f"Failed to filter products using {file}. Please check the logs.", "error")

                # Calculate allowed products for this batch
                normalized_batch = [title.strip().lower() for title in batch]
                normalized_restricted = [title.strip().lower() for title in batch_restricted_titles]

                for title in batch:
                    normalized_title = title.strip().lower()
                    if normalized_title not in normalized_restricted:
                        batch_allowed_titles.append(title)

                # Append data to data.json for this batch
                data_to_append = {
                    "product_titles": batch,
                    "restricted_products": list(batch_restricted_titles),
                    "allowed_products": batch_allowed_titles
                }
                append_to_json(data_to_append)

        else:
            flash("Failed to load product titles or knowledge files. Please check the logs.", "error")

    # Load data from data.json for display
    json_data = load_from_json()

    return render_template('index.html', product_titles=json_data["product_titles"], restricted_titles=json_data["restricted_products"], allowed_titles=json_data["allowed_products"])
    
if __name__ == "__main__":
    app.run(port=5000, debug=True)