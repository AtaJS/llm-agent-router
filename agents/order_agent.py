# Import the json library to read JSON files
import json

# Import re (regular expressions) to find order IDs in text
import re


class OrderAgent:
    """
    Order Status Agent - Checks status of appointments, lab tests, and prescriptions
    This agent searches for order IDs and returns their status
    """
    
    def __init__(self, data_path="data/order_data.json"):
        """
        Initialize (set up) the Order Agent
        
        Args:
            data_path: Location of the order data file
        """
        # Store the path to our data file
        self.data_path = data_path
        
        # Load the order data when agent is created
        self.orders = self._load_data()
        
        print(f"Order Agent initialized with {len(self.orders)} orders")
    
    
    def _load_data(self):
        """
        Load order data from JSON file
        
        Returns:
            List of order dictionaries
        """
        try:
            # Open and read the JSON file
            with open(self.data_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data['orders']  # Return just the 'orders' list
        
        except FileNotFoundError:
            # If file doesn't exist, show error and return empty list
            print(f"Error: Could not find {self.data_path}")
            return []
        
        except json.JSONDecodeError:
            # If JSON file is broken, show error
            print(f"Error: Invalid JSON in {self.data_path}")
            return []
    
    
    def _extract_order_id(self, query):
        """
        Extract order ID from user's query using pattern matching
        Looks for patterns like: APT-12345, LAB-67890, RX-11223
        
        Args:
            query: The user's question (string)
        
        Returns:
            Order ID if found, None otherwise
        """
        # Pattern to match order IDs: 3+ letters, dash, 5 digits
        # Example: APT-12345, LAB-67890, RX-11223
        pattern = r'\b([A-Z]{2,3}-\d{5})\b'
        
        # Search for the pattern in the query
        match = re.search(pattern, query.upper())
        
        if match:
            return match.group(1)  # Return the matched order ID
        
        return None
    
    
    def search(self, query):
        """
        Search for order status based on user's query
        
        Args:
            query: The user's question (string)
        
        Returns:
            Order status information if found, or error message if not found
        """
        # First, try to find an order ID in the query
        order_id = self._extract_order_id(query)
        
        if not order_id:
            return ("I couldn't find an order ID in your query. "
                    "Please provide an order ID (e.g., APT-12345, LAB-67890, or RX-11223).")
        
        # Search through all orders for matching ID
        for order in self.orders:
            if order['order_id'] == order_id:
                # Found the order! Format a nice response
                return self._format_order_response(order)
        
        # If we get here, order ID was found but doesn't exist in our data
        return (f"I couldn't find any order with ID {order_id}. "
                f"Please check the order ID and try again, or contact our office at (555) 123-4567.")
    
    
    def _format_order_response(self, order):
        """
        Format order information into a nice readable response
        
        Args:
            order: Dictionary containing order information
        
        Returns:
            Formatted string with order details
        """
        # Build response based on order type
        response = f"Order {order['order_id']} - {order['order_type']}\n"
        response += f"Patient: {order['patient_name']}\n"
        response += f"Status: {order['status']}\n"
        
        # Add date/time if available
        if order['time'] != "N/A":
            response += f"Date & Time: {order['date']} at {order['time']}\n"
        else:
            response += f"Date: {order['date']}\n"
        
        # Add details
        response += f"Details: {order['details']}\n"
        
        # Add location
        response += f"Location: {order['location']}"
        
        return response
    
    
    def get_all_orders(self):
        """
        Get all order entries (useful for testing)
        
        Returns:
            List of all orders
        """
        return self.orders


# Test code - only runs if we run this file directly
if __name__ == "__main__":
    print("Testing Order Agent...\n")
    
    # Create an Order agent
    agent = OrderAgent()
    
    # Test queries
    test_queries = [
        "Where is my order APT-12345?",
        "What's the status of LAB-67890?",
        "Is my prescription RX-11223 ready?",
        "Check order APT-99999",  # This doesn't exist
        "I need my appointment info"  # No order ID
    ]
    
    # Try each test query
    for query in test_queries:
        print(f"Query: {query}")
        answer = agent.search(query)
        print(f"Answer:\n{answer}\n")
        print("-" * 60 + "\n")