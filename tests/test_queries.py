{
  "test_queries": [
    {
      "id": 1,
      "query": "What time do you open on Saturday?",
      "expected_agent": "faq",
      "reason": "General clinic information question about hours"
    },
    {
      "id": 2,
      "query": "Where is my lab result for order LAB-67890?",
      "expected_agent": "order_status",
      "reason": "Specific order status inquiry with order ID"
    },
    {
      "id": 3,
      "query": "Do you accept Blue Cross insurance?",
      "expected_agent": "faq",
      "reason": "General question about insurance acceptance"
    },
    {
      "id": 4,
      "query": "Is my appointment APT-12345 confirmed?",
      "expected_agent": "order_status",
      "reason": "Checking status of specific appointment"
    },
    {
      "id": 5,
      "query": "How can I schedule an appointment?",
      "expected_agent": "faq",
      "reason": "General question about booking process"
    },
    {
      "id": 6,
      "query": "What's the status of prescription RX-11223?",
      "expected_agent": "order_status",
      "reason": "Checking status of specific prescription order"
    },
    {
      "id": 7,
      "query": "Do you offer telehealth visits?",
      "expected_agent": "faq",
      "reason": "General service inquiry"
    },
    {
      "id": 8,
      "query": "Can you tell me about my order APT-23456?",
      "expected_agent": "order_status",
      "reason": "Requesting information about specific order"
    },
    {
      "id": 9,
      "query": "What should I bring to my first visit?",
      "expected_agent": "faq",
      "reason": "General new patient question"
    },
    {
      "id": 10,
      "query": "Has my lab test LAB-78901 been processed?",
      "expected_agent": "order_status",
      "reason": "Checking processing status of specific lab order"
    },
    {
      "id": 11,
      "query": "Where are you located?",
      "expected_agent": "faq",
      "reason": "General clinic location question"
    },
    {
      "id": 12,
      "query": "When is appointment APT-34567 scheduled for?",
      "expected_agent": "order_status",
      "reason": "Asking for date/time of specific appointment"
    },
    {
      "id": 13,
      "query": "What's your cancellation policy?",
      "expected_agent": "faq",
      "reason": "General policy question"
    },
    {
      "id": 14,
      "query": "Is prescription RX-22334 ready to pick up?",
      "expected_agent": "order_status",
      "reason": "Checking if specific prescription is ready"
    },
    {
      "id": 15,
      "query": "Do you see children?",
      "expected_agent": "faq",
      "reason": "General question about services offered (pediatrics)"
    },
    {
      "id": 16,
      "query": "Check the status of LAB-89012",
      "expected_agent": "order_status",
      "reason": "Direct status check with order ID"
    },
    {
      "id": 17,
      "query": "Is there parking at your clinic?",
      "expected_agent": "faq",
      "reason": "General facility question"
    },
    {
      "id": 18,
      "query": "My order number is APT-45678, what happened with it?",
      "expected_agent": "order_status",
      "reason": "Inquiry about specific order outcome"
    },
    {
      "id": 19,
      "query": "Can I get a prescription refilled?",
      "expected_agent": "faq",
      "reason": "General question about prescription refill process"
    },
    {
      "id": 20,
      "query": "What pharmacy is my prescription RX-33445 at?",
      "expected_agent": "order_status",
      "reason": "Asking about specific prescription location"
    },
    {
      "id": 21,
      "query": "Do you have a lab on site?",
      "expected_agent": "faq",
      "reason": "General facility/services question"
    },
    {
      "id": 22,
      "query": "I need to know about LAB-90123",
      "expected_agent": "order_status",
      "reason": "Requesting information about specific lab order"
    },
    {
      "id": 23,
      "query": "What are your office hours during the week?",
      "expected_agent": "faq",
      "reason": "General hours question"
    },
    {
      "id": 24,
      "query": "Was my appointment APT-56789 cancelled?",
      "expected_agent": "order_status",
      "reason": "Checking cancellation status of specific appointment"
    },
    {
      "id": 25,
      "query": "How do I access my test results?",
      "expected_agent": "faq",
      "reason": "General question about patient portal/results access process"
    }
  ]
}