# Import regular expressions for pattern matching
import re

# Import our agents
import sys
import os

# Add parent directory to path so we can import agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.faq_agent import FAQAgent
from agents.order_agent import OrderAgent


class LLMRouter:
    """
    LLM Router - Decides which agent should handle each query
    
    Version 1: Simple rule-based routing (no LLM API needed)
    Version 2: Will add real LLM APIs (GPT, Claude, Gemini)
    """
    
    def __init__(self, mode="simple"):
        """
        Initialize the router
        
        Args:
            mode: "simple" for rule-based, "gpt" / "claude" / "gemini" for LLM APIs
        """
        self.mode = mode
        
        # Create both agents
        print("Initializing LLM Router...\n")
        self.faq_agent = FAQAgent()
        self.order_agent = OrderAgent()
        
        print(f"\nRouter ready in '{mode}' mode!\n")
    
    
    def route(self, query):
        """
        Route the query to the appropriate agent
        
        Args:
            query: User's question (string)
        
        Returns:
            Tuple of (agent_name, answer)
        """
        # Decide which agent based on mode
        if self.mode == "simple":
            agent_name = self._simple_route(query)
        elif self.mode == "gpt":
            agent_name = self._gpt_route(query)
        elif self.mode == "claude":
            agent_name = self._claude_route(query)
        elif self.mode == "gemini":
            agent_name = self._gemini_route(query)
        else:
            agent_name = "faq"  # Default to FAQ
        
        # Call the appropriate agent
        if agent_name == "order_status":
            answer = self.order_agent.search(query)
        else:
            answer = self.faq_agent.search(query)
        
        return agent_name, answer
    
    
    def _simple_route(self, query):
        """
        Simple rule-based routing (no LLM needed)
        
        Args:
            query: User's question
        
        Returns:
            Agent name: "faq" or "order_status"
        """
        query_lower = query.lower()
        
        # Check if query contains an order ID pattern (APT-, LAB-, RX-)
        order_id_pattern = r'\b([A-Z]{2,3}-\d{5})\b'
        if re.search(order_id_pattern, query.upper()):
            return "order_status"
        
        # Keywords that suggest order status query
        order_keywords = [
            'order', 'appointment', 'lab', 'test', 'prescription',
            'status', 'result', 'apt-', 'lab-', 'rx-',
            'scheduled', 'ready', 'pickup', 'confirmed'
        ]
        
        # Check if any order keywords are in the query
        for keyword in order_keywords:
            if keyword in query_lower:
                return "order_status"
        
        # Default to FAQ for general questions
        return "faq"
    
    
    def _gpt_route(self, query):
        """
        Route using OpenAI GPT (placeholder - will implement later)
        
        Args:
            query: User's question
        
        Returns:
            Agent name: "faq" or "order_status"
        """
        # TODO: Add GPT API call here
        print("GPT routing not yet implemented, using simple routing")
        return self._simple_route(query)
    
    
    def _claude_route(self, query):
        """
        Route using Anthropic Claude (placeholder - will implement later)
        
        Args:
            query: User's question
        
        Returns:
            Agent name: "faq" or "order_status"
        """
        # TODO: Add Claude API call here
        print("Claude routing not yet implemented, using simple routing")
        return self._simple_route(query)
    
    
    def _gemini_route(self, query):
        """
        Route using Google Gemini (placeholder - will implement later)
        
        Args:
            query: User's question
        
        Returns:
            Agent name: "faq" or "order_status"
        """
        # TODO: Add Gemini API call here
        print("Gemini routing not yet implemented, using simple routing")
        return self._simple_route(query)


# Test code - only runs if we run this file directly
if __name__ == "__main__":
    print("Testing LLM Router...\n")
    print("=" * 70 + "\n")
    
    # Create router in simple mode
    router = LLMRouter(mode="simple")
    
    # Test queries (mix of FAQ and order status)
    test_queries = [
        "What are your clinic hours?",
        "Where is my order APT-12345?",
        "Do you accept insurance?",
        "Is my lab test LAB-67890 ready?",
        "How do I book an appointment?",
        "What's the status of prescription RX-11223?",
        "Do you offer telehealth?",
        "Check my appointment status"
    ]
    
    # Try each query
    for i, query in enumerate(test_queries, 1):
        print(f"Query {i}: {query}")
        agent_name, answer = router.route(query)
        print(f"Routed to: {agent_name.upper()} Agent")
        print(f"Answer: {answer}")
        print("\n" + "=" * 70 + "\n")