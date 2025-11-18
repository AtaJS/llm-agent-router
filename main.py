"""
LLM Agent Router - Main Program
Healthcare Customer Service Bot for Nordhealth Assignment

Author: Ata Jodeiri Seyedian
Date: November 2024
"""

import sys
import os

# Import our router
from routers.llm_router import LLMRouter


def print_banner():
    """Print a welcome banner"""
    print("\n" + "=" * 70)
    print("HEALTHCARE CUSTOMER SERVICE BOT")
    print("=" * 70)
    print("Powered by LLM Agent Router")
    print("Ask about clinic hours, services, or check your order status!")
    print("=" * 70 + "\n")


def print_help():
    """Print help information"""
    print("\nHELP - Example Questions:")
    print("-" * 70)
    print("FAQ Questions:")
    print("  • What are your clinic hours?")
    print("  • Do you accept insurance?")
    print("  • How do I book an appointment?")
    print("  • Where are you located?")
    print("")
    print("Order Status Questions (use real order IDs from test data):")
    print("  • Where is my order APT-12345?")
    print("  • Is my lab test LAB-67890 ready?")
    print("  • What's the status of prescription RX-11223?")
    print("-" * 70 + "\n")


def main():
    """Main function to run the customer service bot"""
    
    # Print welcome banner
    print_banner()
    
    # Ask user which mode to use
    print("Select Router Mode:")
    print("  1. Simple (No AI)")
    print("  2. GPT-4o (OpenAI Azure)")
    print("  3. Claude(Not available at the moment)")
    print("  4. Gemini-1.5-pro (Google)")
    
    choice = input("\nEnter choice (1-4) [default: Gemini-1.5-pro]: ").strip()
    
    # Map choice to mode
    mode_map = {
        "1": "simple",
        "2": "gpt",
        "3": "claude",
        "4": "gemini",
        "": "gemini"  # Default
    }
    
    mode = mode_map.get(choice, "simple")
    
    print(f"\nStarting bot in '{mode}' mode...\n")
    
    # Initialize the router
    try:
        router = LLMRouter(mode=mode)
    except Exception as e:
        print(f"Error initializing router: {e}")
        return
    
    print("\nBot is ready! Type your questions below.")
    print("Type 'help' for examples, 'quit' to exit.\n")
    
    # Main interaction loop
    while True:
        try:
            # Get user input
            user_query = input("You: ").strip()
            
            # Check for special commands
            if user_query.lower() in ['quit', 'exit', 'q']:
                print("\n Thank you for using our service!")
                print(" We wish you a healthy day!\n")
                print("\n Goodbye!\n")
                break
            
            if user_query.lower() == 'help':
                print_help()
                continue
            
            if not user_query:
                print("Please enter a question.\n")
                continue
            
            # Route the query and get answer
            print("")  # Blank line for readability
            agent_name, answer = router.route(user_query)
            
            # Display which agent handled it
            agent_display = "FAQ Agent" if agent_name == "faq" else "Order Status Agent"
            print(f"Handled by: {agent_display}")
            print(f"Answer:\n{answer}\n")
            print("-" * 70 + "\n")
            
        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye! NordHealth team wishes you have healthy days ahead!\n")
            break
        
        except Exception as e:
            print(f"\nError: {e}\n")
            continue


def demo_mode():
    """Run automated demo with test queries"""
    print_banner()
    print("DEMO MODE - Running automated test queries...\n")
    
    # Initialize router
    router = LLMRouter(mode="simple")
    
    # Demo queries
    demo_queries = [
        "What are your clinic hours?",
        "Where is my order APT-12345?",
        "Do you accept insurance?",
        "Is my lab test LAB-67890 ready?",
        "How do I book an appointment?",
    ]
    
    for i, query in enumerate(demo_queries, 1):
        print(f"\nDemo Query {i}: {query}")
        agent_name, answer = router.route(query)
        agent_display = "FAQ Agent" if agent_name == "faq" else "Order Status Agent"
        print(f"Handled by: {agent_display}")
        print(f"Answer: {answer[:100]}...")  # Show first 100 chars
        print("-" * 70)
    
    print("\nDemo complete!\n")


if __name__ == "__main__":
    # Check if demo mode requested
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo_mode()
    else:
        main()