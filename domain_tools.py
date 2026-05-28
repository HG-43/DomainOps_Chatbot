# MOCK_ORDER_DATABASE represents your live enterprise ledger for Indian logistics
MOCK_ORDER_DATABASE = {
    "SWIFT-BOM-4002": {
        "destination": "Mumbai",
        "carrier": "Blue Dart Air Network",
        "status": "🚨 Delayed",
        "details": "Shipment on hold at Mumbai Hub 1 due to severe waterlogging and monsoon traffic diversions.",
        "value": 4500.0
    },
    "SWIFT-DEL-9109": {
        "destination": "Delhi / NCR",
        "carrier": "Delhivery Express",
        "status": "📦 Out for Delivery",
        "details": "Package sorted at Okhla Hub. Handed over to courier associate. Expected delivery before 6:00 PM IST.",
        "value": 1200.0
    },
    "SWIFT-BLR-5601": {
        "destination": "Bengaluru",
        "carrier": "Delhivery Surface",
        "status": "⚠️ Exception",
        "details": "Delivery agent got caught in the Silk Board traffic jam for 3 hours. Attempt rescheduled for tomorrow morning.",
        "value": 8900.0
    }
}

def lookup_mock_order(tracking_id):
    """Queries the operational database for a specific tracking profile."""
    # Ensure this function name matches line 155 in your streamlit_app.py exactly
    return MOCK_ORDER_DATABASE.get(tracking_id.strip().upper(), None)

def calculate_restocking_fee(price, is_damaged):
    """Calculates strict return financial deductions based on packaging states."""
    if is_damaged:
        return round(price * 0.15, 2)
    return 0.0

def evaluate_shipping_carrier(destination):
    """Programmatic carrier routing fallback logic for export layers."""
    dest = destination.lower()
    if "us" in dest or "america" in dest:
        return "DHL Global Export"
    elif "uk" in dest or "london" in dest:
        return "FedEx International Premium"
    return "Centralized Postal Export Hub"