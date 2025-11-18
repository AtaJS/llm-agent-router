# Import regular expressions for pattern matching
import re
import sys
import os

# Add parent directory to path so we can import agents and config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.faq_agent import FAQAgent
from agents.order_agent import OrderAgent

# Import API libraries
try:
    import google.generativeai as genai
    from openai import AzureOpenAI
    from anthropic import Anthropic
    import config
    APIS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import API libraries: {e}")
    APIS_AVAILABLE = False


class LLMRouter:
    """
    LLM Router - Decides which agent should handle each query
    
    Supports multiple routing modes:
    - simple: Rule-based routing (no API needed)
    - gpt: Azure OpenAI GPT-4
    - claude: Anthropic Claude
    - gemini: Google Gemini
    """
    
    def __init__(self, mode="simple"):
        """
        Initialize the router
        
        Args:
            mode: "simple", "gpt", "claude", or "gemini"
        """
        self.mode = mode
        
        # Create both agents
        print("Initializing LLM Router...\n")
        self.faq_agent = FAQAgent()
        self.order_agent = OrderAgent()
        
        # Initialize API clients if needed
        if mode != "simple" and APIS_AVAILABLE:
            self._init_api_clients()
        
        print(f"\nRouter ready in '{mode}' mode!\n")
    
    
    def _init_api_clients(self):
        """Initialize API clients based on mode"""
        try:
            if self.mode == "gemini":
                genai.configure(api_key=config.GEMINI_API_KEY)
                self.gemini_model = genai.GenerativeModel('models/gemini-2.5-pro')
                print("Gemini API initialized")
            
            elif self.mode == "gpt":
                self.gpt_client = AzureOpenAI(
                    api_key=config.AZURE_OPENAI_KEY,
                    api_version="2024-02-15-preview",
                    azure_endpoint=config.AZURE_OPENAI_ENDPOINT
                )
                print("Azure OpenAI (GPT-4) API initialized")
            
            elif self.mode == "claude":
                self.claude_client = Anthropic(api_key=config.CLAUDE_API_KEY)
                print("Claude API initialized")
                
        except Exception as e:
            print(f"Warning: Could not initialize {self.mode} API: {e}")
            print("Falling back to simple routing...")
            self.mode = "simple"
    
    
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
        Route using Azure OpenAI GPT-4
        
        Args:
            query: User's question
        
        Returns:
            Agent name: "faq" or "order_status"
        """
        try:
            # Create the prompt for GPT
            system_prompt = """You are a routing assistant for a healthcare customer service system.
Your job is to classify user queries into one of two categories:

1. "faq" - General questions about clinic hours, services, insurance, location, policies, etc.
2. "order_status" - Questions about specific appointments, lab tests, or prescriptions (usually includes order IDs like APT-12345, LAB-67890, RX-11223)

Respond with ONLY one word: either "faq" or "order_status". Nothing else."""

            # Call GPT-4
            response = self.gpt_client.chat.completions.create(
                model=config.AZURE_OPENAI_DEPLOYMENT,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                temperature=0,
                max_tokens=10
            )
            
            # Get the response
            result = response.choices[0].message.content.strip().lower()
            
            # Validate response
            if "order" in result or "status" in result:
                return "order_status"
            else:
                return "faq"
                
        except Exception as e:
            print(f"GPT routing error: {e}")
            print("Falling back to simple routing...")
            return self._simple_route(query)
    
    
    def _claude_route(self, query):
        """
        Route using Anthropic Claude
        
        Args:
            query: User's question
        
        Returns:
            Agent name: "faq" or "order_status"
        """
        try:
            # Create the prompt for Claude
            prompt = f"""You are a routing assistant for a healthcare customer service system.

Classify this user query into one of two categories:

1. "faq" - General questions about clinic hours, services, insurance, location, policies, etc.
2. "order_status" - Questions about specific appointments, lab tests, or prescriptions (usually includes order IDs like APT-12345, LAB-67890, RX-11223)

User query: "{query}"

Respond with ONLY one word: either "faq" or "order_status". Nothing else."""

            # Call Claude
            message = self.claude_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=10,
                temperature=0,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Get the response
            result = message.content[0].text.strip().lower()
            
            # Validate response
            if "order" in result or "status" in result:
                return "order_status"
            else:
                return "faq"
                
        except Exception as e:
            print(f"Claude routing error: {e}")
            print("Falling back to simple routing...")
            return self._simple_route(query)
    
    
    def _gemini_route(self, query):
        """
        Route using Google Gemini
        
        Args:
            query: User's question
        
        Returns:
            Agent name: "faq" or "order_status"
        """
        try:
            # Create the prompt for Gemini
            prompt = f"""You are a routing assistant for a healthcare customer service system.

Classify this user query into one of two categories:

1. "faq" - General questions about clinic hours, services, insurance, location, policies, etc.
2. "order_status" - Questions about specific appointments, lab tests, or prescriptions (usually includes order IDs like APT-12345, LAB-67890, RX-11223)

User query: "{query}"

Respond with ONLY one word: either "faq" or "order_status". Nothing else."""

            # Call Gemini
            response = self.gemini_model.generate_content(prompt)
            
            # Get the response
            result = response.text.strip().lower()
            
            # Validate response
            if "order" in result or "status" in result:
                return "order_status"
            else:
                return "faq"
                
        except Exception as e:
            print(f"Gemini routing error: {e}")
            print("Falling back to simple routing...")
            return self._simple_route(query)


# Test code
if __name__ == "__main__":
    print("Testing LLM Router with all modes...\n")
    print("=" * 70 + "\n")
    
    # Test queries
    test_queries = [
        "What are your clinic hours?",
        "Where is my order APT-12345?",
        "How do I book an appointment?",
    ]
    
    # Test each mode
    for mode in ["simple", "gemini", "gpt"]:
        print(f"\n{'='*70}")
        print(f"Testing {mode.upper()} mode:")
        print('='*70 + "\n")
        
        router = LLMRouter(mode=mode)
        
        for query in test_queries:
            print(f"Query: {query}")
            agent_name, answer = router.route(query)
            print(f"Routed to: {agent_name.upper()}")
            print(f"Answer: {answer[:80]}...")
            print()