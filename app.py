from flask import Flask, jsonify, request, abort
import uuid
import re
from math import ceil

app = Flask(__name__)

# In-memory storage for receipts
receipts = {}

# Helper function to validate total price format
def validate_total_price(total):
    return bool(re.match(r'^\d+\.\d{2}$', total))

# Helper function to validate item price format
def validate_item_price(price):
    return bool(re.match(r'^\d+\.\d{2}$', price))

# Function to calculate points for a receipt
def calculate_points(receipt):
    points = 0

    # Rule 1: 1 point for every alphanumeric character in the retailer name
    points += len(re.sub(r'[^a-zA-Z0-9]', '', receipt['retailer']))

    # Rule 2: 50 points if the total is a round dollar amount (no cents)
    if float(receipt['total']).is_integer():
        points += 50

    # Rule 3: 25 points if the total is a multiple of 0.25
    if round(float(receipt['total']) * 4) % 1 == 0:
        points += 25

    # Rule 4: 5 points for every two items
    points += (len(receipt['items']) // 2) * 5

    # Rule 5: Item description multiple of 3 characters - apply special price rule
    for item in receipt['items']:
        description = item['shortDescription'].strip()
        price = float(item['price'])

        if len(description) % 3 == 0:
            points += ceil(price * 0.2)

    # Rule 6: 6 points if the day in the purchase date is odd
    day = int(receipt['purchaseDate'].split('-')[2])
    if day % 2 != 0:
        points += 6

    # Rule 7: 10 points if the time is between 2:00 PM and 4:00 PM
    purchase_time = receipt['purchaseTime']
    hour, minute = map(int, purchase_time.split(':'))
    if 14 <= hour < 16 or (hour == 16 and minute == 0):
        points += 10

    return points

# Endpoint to process a receipt
@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Invalid input'}), 400

    # Extract fields
    retailer = data.get('retailer')
    purchase_date = data.get('purchaseDate')
    purchase_time = data.get('purchaseTime')
    items = data.get('items')
    total = data.get('total')

    # Validate required fields
    if not retailer or not purchase_date or not purchase_time or not items or not total:
        return jsonify({'error': 'Missing required fields'}), 400

    # Validate total and item prices
    if not validate_total_price(total):
        return jsonify({'error': 'Invalid total price format'}), 400

    for item in items:
        if not item.get('shortDescription') or not validate_item_price(item['price']):
            return jsonify({'error': 'Invalid item price format'}), 400

    # Generate unique receipt ID
    receipt_id = str(uuid.uuid4())
    receipt = {
        'retailer': retailer,
        'purchaseDate': purchase_date,
        'purchaseTime': purchase_time,
        'items': items,
        'total': total
    }

    # Store receipt in memory
    receipts[receipt_id] = receipt

    # Return receipt ID
    return jsonify({'id': receipt_id}), 200

# Endpoint to get points for a receipt
@app.route('/receipts/<string:id>/points', methods=['GET'])
def get_receipt_points(id):
    # Look for the receipt in memory
    receipt = receipts.get(id)

    if not receipt:
        return jsonify({'error': 'Receipt not found'}), 404

    # Calculate points
    points = calculate_points(receipt)

    # Return points
    return jsonify({'points': points}), 200

if __name__ == '__main__':
    app.run(debug=True)
