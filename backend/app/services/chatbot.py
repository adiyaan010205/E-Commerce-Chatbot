import re
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from ..models.product import Product
from ..services.product_search import ProductSearchService

class ChatbotService:
    def __init__(self, db: Session):
        self.db = db
        self.product_service = ProductSearchService(db)
        self.intents = {
            'greeting': [
                r'\b(hi|hello|hey|good morning|good afternoon|good evening)\b',
                r'\bhow are you\b',
                r'\bwhat\'s up\b'
            ],
            'product_search': [
                r'\b(find|search|look for|show me|i want|i need)\b.*\b(product|item|thing)\b',
                r'\b(laptop|phone|shirt|book|electronics|clothing)\b',
                r'\bprice\b.*\b(under|below|less than|cheaper)\b',
                r'^\s*[a-zA-Z\s]+\s*$'  # Simple product name
            ],
            'category_browse': [
                r'\b(browse|show|list|what)\b.*\b(categories|types|kinds)\b',
                r'\bcategory\b',
                r'\bwhat do you have\b'
            ],
            'price_inquiry': [
                r'\b(price|cost|how much|expensive|cheap)\b',
                r'\$\d+',
                r'\bbudget\b'
            ],
            'help': [
                r'\b(help|assist|support|guide)\b',
                r'\bwhat can you do\b',
                r'\bhow does this work\b'
            ],
            'goodbye': [
                r'\b(bye|goodbye|see you|later|exit|quit)\b',
                r'\bthank you\b.*\bbye\b'
            ]
        }

    def process_message(self, message: str, user_id: int) -> Dict[str, Any]:
        """Process user message and return appropriate response"""
        message_lower = message.lower().strip()
        intent = self._detect_intent(message_lower)
        
        if intent == 'greeting':
            return self._handle_greeting()
        elif intent == 'product_search':
            return self._handle_product_search(message)
        elif intent == 'category_browse':
            return self._handle_category_browse()
        elif intent == 'price_inquiry':
            return self._handle_price_inquiry(message)
        elif intent == 'help':
            return self._handle_help()
        elif intent == 'goodbye':
            return self._handle_goodbye()
        else:
            return self._handle_default(message)

    def _detect_intent(self, message: str) -> str:
        """Detect user intent from message"""
        for intent, patterns in self.intents.items():
            for pattern in patterns:
                if re.search(pattern, message, re.IGNORECASE):
                    return intent
        return 'default'

    def _handle_greeting(self) -> Dict[str, Any]:
        """Handle greeting messages"""
        responses = [
            "Hello! Welcome to our store! How can I help you find the perfect product today?",
            "Hi there! I'm here to help you discover amazing products. What are you looking for?",
            "Hey! Ready to find something awesome? Tell me what you need!"
        ]
        return {
            'message': responses[0],
            'products': [],
            'suggestions': [
                "Browse electronics",
                "Show me laptops",
                "Find smartphones",
                "What's on sale?"
            ]
        }

    def _handle_product_search(self, message: str) -> Dict[str, Any]:
        """Handle product search queries"""
        # Extract search terms and filters
        search_params = self._extract_search_params(message)
        products = self.product_service.search_products(**search_params)
        
        if products:
            product_list = [product.to_dict() for product in products[:6]]
            response = f"I found {len(products)} products for you! Here are some great options:"
            
            if search_params.get('category'):
                response = f"Here are some {search_params['category']} products I found:"
        else:
            product_list = []
            response = "I couldn't find any products matching your search. Try being more specific or browse our categories!"
            
        return {
            'message': response,
            'products': product_list,
            'suggestions': self._get_search_suggestions()
        }

    def _handle_category_browse(self) -> Dict[str, Any]:
        """Handle category browsing requests"""
        categories = self.product_service.get_categories()
        category_list = ", ".join(categories[:8])
        
        return {
            'message': f"We have products in these categories: {category_list}. Which one interests you?",
            'products': [],
            'suggestions': categories[:4]
        }

    def _handle_price_inquiry(self, message: str) -> Dict[str, Any]:
        """Handle price-related queries"""
        price_match = re.search(r'\$?(\d+)', message)
        if price_match:
            price = float(price_match.group(1))
            products = self.product_service.search_products(max_price=price, limit=6)
            product_list = [product.to_dict() for product in products]
            
            return {
                'message': f"Here are products under ${price}:",
                'products': product_list,
                'suggestions': ["Show cheaper options", "Browse by category"]
            }
        
        return {
            'message': "What's your budget? I can help you find products within your price range!",
            'products': [],
            'suggestions': ["Under $50", "Under $100", "Under $500"]
        }

    def _handle_help(self) -> Dict[str, Any]:
        """Handle help requests"""
        return {
            'message': """I can help you with:
            
• **Product Search**: Tell me what you're looking for
• **Browse Categories**: Ask to see product categories  
• **Price Filtering**: Set your budget and I'll find options
• **Product Details**: Ask about specific products
• **Recommendations**: Get personalized suggestions

Just type naturally - for example: "show me laptops under $800" or "I need a birthday gift"!""",
            'products': [],
            'suggestions': [
                "Show me categories",
                "Find laptops",
                "What's popular?",
                "Products under $100"
            ]
        }

    def _handle_goodbye(self) -> Dict[str, Any]:
        """Handle goodbye messages"""
        return {
            'message': "Thanks for shopping with us! Feel free to come back anytime. Have a great day! 👋",
            'products': [],
            'suggestions': []
        }

    def _handle_default(self, message: str) -> Dict[str, Any]:
        """Handle unrecognized messages"""
        # Try to search for products anyway
        products = self.product_service.search_products(query=message, limit=4)
        
        if products:
            product_list = [product.to_dict() for product in products]
            return {
                'message': f"I found some products that might match '{message}':",
                'products': product_list,
                'suggestions': ["Show more like this", "Browse categories"]
            }
        
        return {
            'message': """I'm a chatbot designed to help you with product search and information. Here are some things you can ask me:

•   "Show me laptops"
•   "What products are in the electronics category?"
•   "Find smartphones under $500"
•   "What's the price of a specific product?"

How can I assist you today?""",
            'products': [],
            'suggestions': [
                "Show me categories",
                "What's on sale?",
                "Find a gift"
            ]
        }

    def _extract_search_params(self, message: str) -> Dict[str, Any]:
        """Extract search parameters from user message"""
        params = {'limit': 10}
        
        # Extract price range
        price_match = re.search(r'under\s+\$?(\d+)', message, re.IGNORECASE)
        if price_match:
            params['max_price'] = float(price_match.group(1))
        
        # Extract category hints
        categories = ['electronics', 'clothing', 'books', 'home', 'sports', 'beauty']
        for category in categories:
            if category in message.lower():
                params['category'] = category
                break
        
        # Extract brand hints
        brands = ['apple', 'samsung', 'nike', 'adidas', 'sony', 'lg']
        for brand in brands:
            if brand in message.lower():
                params['brand'] = brand
                break
        
        # Use the full message as search query
        params['query'] = message
        
        return params

    def _get_search_suggestions(self) -> List[str]:
        """Get relevant search suggestions"""
        return [
            "Show me more",
            "Filter by price",
            "Browse categories",
            "Popular products"
        ]
