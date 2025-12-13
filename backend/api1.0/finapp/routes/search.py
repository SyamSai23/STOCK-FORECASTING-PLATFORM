from flask import Blueprint, jsonify, request
from services.stock_service import get_stock_info

search_bp = Blueprint('search_bp', __name__)

@search_bp.route('/search', methods=['POST'])
def search_stock():
    try:
        data = request.json
        ticker = data.get('ticker')

        if not ticker:
            return jsonify({"error": "Ticker not provided"}), 400

        stock_info = get_stock_info(ticker)

        if 'error' in stock_info:
            return jsonify({"error": stock_info['error']}), 500

        return jsonify(stock_info)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
