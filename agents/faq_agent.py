# Import the json library to read JSON files
import json

# Import the os library to work with file paths
import os


class FAQAgent:
    """
    FAQ Agent - Answers general questions about the clinic
    This agent loads FAQ data and searches for matching answers
    """
    
    def __init__(self, data_path="data/faq_data.json"):
        """
        Initialize (set up) the FAQ Agent
        This runs when we create a new FAQ Agent
        
        Args:
            data_path: Location of the FAQ data file
        """
        # Store the path to our data file
        self.data_path = data_path
        
        # Load the FAQ data when agent is created
        self.faqs = self._load_data()
        
        print(f"FAQ Agent initialized with {len(self.faqs)} FAQs")
    
    
    def _load_data(self):
        """
        Load FAQ data from JSON file
        The underscore _ means this is a "private" helper function
        
        Returns:
            List of FAQ dictionaries
        """
        try:
            # Open and read the JSON file
            with open(self.data_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data['faqs']  # Return just the 'faqs' list
        
        except FileNotFoundError:
            # If file doesn't exist, show error and return empty list
            print(f"Error: Could not find {self.data_path}")
            return []
        
        except json.JSONDecodeError:
            # If JSON file is broken, show error
            print(f"Error: Invalid JSON in {self.data_path}")
            return []
    
    
    def search(self, query):
        """
        Search for an answer to the user's query
        
        Args:
            query: The user's question (string)
        
        Returns:
            Answer string if found, or a default message if not found
        """
        # Convert query to lowercase for easier matching
        query_lower = query.lower()
        
        # Variables to track the best match
        best_match = None
        highest_score = 0
        
        # Loop through each FAQ entry
        for faq in self.faqs:
            score = 0
            
            # Check how many keywords from this FAQ appear in the query
            for keyword in faq['keywords']:
                if keyword.lower() in query_lower:
                    score += 1  # Increase score for each matching keyword
            
            # If this FAQ has more matching keywords than previous best
            if score > highest_score:
                highest_score = score
                best_match = faq
        
        # If we found a match (at least 1 keyword matched)
        if best_match and highest_score > 0:
            return best_match['answer']
        
        # If no match found, return a helpful default message
        return ("I couldn't find a specific answer to your question. "
                "Please contact our office at (555) 123-4567 for assistance, "
                "or rephrase your question.")
    
    
    def get_all_faqs(self):
        """
        Get all FAQ entries (useful for testing)
        
        Returns:
            List of all FAQs
        """
        return self.faqs


# Test code - only runs if we run this file directly
if __name__ == "__main__":
    print("Testing FAQ Agent...\n")
    
    # Create an FAQ agent
    agent = FAQAgent()
    
    # Test queries
    test_queries = [
        "What are your hours?",
        "Do you take insurance?",
        "Where are you located?",
        "Something random that won't match"
    ]
    
    # Try each test query
    for query in test_queries:
        print(f"Query: {query}")
        answer = agent.search(query)
        print(f"Answer: {answer}\n")