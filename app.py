from flask import Flask, jsonify, request, abort
import uuid
from math import ceil
import re

app = Flask(__name__)

receipts = {}

# Ping endpoint
@app.route('/ping', methods=['GET'])
def ping():
    return "Pong"

def validate_total_price(total):
    return bool(re.match(r'^\d+\.\d{2}$', total))

def validate_item_price(price):
    return bool(re.match(r'^\d+\.\d{2}$', price))

def is_multiple_of_quarter(amount):
    return abs(round(amount % 0.25, 2)) < 0.01

# Function to calculate points for a receipt
def calculate_points(receipt):
    points = 0

    retailer_points = len(re.sub(r'[^a-zA-Z0-9]', '', receipt['retailer']))
    points += retailer_points

    if float(receipt['total']).is_integer():
        points += 50

    if is_multiple_of_quarter(float(receipt['total'])):
        points += 25

    pair_points = (len(receipt['items']) // 2) * 5
    points += pair_points

    for item in receipt['items']:
        description = item['shortDescription'].strip()
        price = float(item['price'])

        if len(description) % 3 == 0:
            item_points = ceil(price * 0.2)
            points += item_points

    day = int(receipt['purchaseDate'].split('-')[2])
    if day % 2 != 0:
        points += 6

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

    retailer = data.get('retailer')
    purchase_date = data.get('purchaseDate')
    purchase_time = data.get('purchaseTime')
    items = data.get('items')
    total = data.get('total')


    if not retailer or not purchase_date or not purchase_time or not items or not total:
        return jsonify({'error': 'Missing required fields'}), 400

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

    receipts[receipt_id] = receipt

    return jsonify({'id': receipt_id}), 200

# Endpoint to get points for a receipt
@app.route('/receipts/<string:id>/points', methods=['GET'])
def get_receipt_points(id):

    receipt = receipts.get(id)

    if not receipt:
        return jsonify({'error': 'Receipt not found'}), 404

    # Calculate points
    points = calculate_points(receipt)

    # Return points
    return jsonify({'points': points}), 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3000)