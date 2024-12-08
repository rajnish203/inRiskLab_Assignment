from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)
products = []

def fetch_products_from_dummy_api():
    try:
        response = requests.get("https://dummyjson.com/products")
        response.raise_for_status()
        data = response.json()
        return data.get('products', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching products: {e}")
        return None

initial_products = fetch_products_from_dummy_api()
if initial_products is not None:
    products = initial_products
else:
    print("Error: Could not fetch products. Using an empty list.")
    products = []

@app.route('/')
def home():
    return render_template('index.html', products=products)

@app.route('/products', methods=['GET', 'POST'])
def manage_products():
    if request.method == 'GET':
        return jsonify(products), 200

    if request.method == 'POST':
        product_data = request.get_json()
        if not product_data or 'title' not in product_data or 'price' not in product_data or 'category' not in product_data:
            return jsonify({"error": "Product must include 'title', 'price', and 'category'."}), 400
        products.append(product_data)
        return jsonify(products), 201

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": "Internal server error. Please try again later."}), 500

@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({"error": "Bad request. Please check the data provided."}), 400

if __name__ == '__main__':
    app.run(debug=True)
