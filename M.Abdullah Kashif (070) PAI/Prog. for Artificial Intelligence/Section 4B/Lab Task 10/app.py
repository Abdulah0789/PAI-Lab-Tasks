from flask import Flask, render_template, request, jsonify
import random
from datetime import datetime

app = Flask(__name__)

restaurants = [
    {
        'name': "Gourmet Restaurant",
        'cuisine': "International",
        'location': "123 Food Street, Lahore",
        'price_range': "$$$",
        'rating': 4.5,
        'opening_hours': "11:00 AM - 10:00 PM (Mon-Sun)",
        'parking': "Valet parking available",
        'signature_dishes': ["Truffle Pasta", "Seafood Platter", "Molten Lava Cake"],
        'menu': {
            'starters': ["Bruschetta - $8", "Calamari - $12", "Soup of the Day - $7"],
            'mains': ["Grilled Salmon - $24", "Ribeye Steak - $32", "Vegetable Risotto - $18"],
            'desserts': ["Tiramisu - $9", "Chocolate Fondant - $10"]
        },
        'delivery': {
            'services': ["FoodExpress", "MealDash"],
            'contact': "042-1234567"
        }
    }
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json['message']
    response = generate_response(user_message.lower())
    return jsonify({'response': response})

def generate_response(message):
    greetings = ['hi', 'hello', 'hey', 'greetings']
    if any(word in message for word in greetings):
        return random.choice([
            "Hello! Welcome to Gourmet Restaurant Lahore. How can I help you today?",
            "Hi there! Looking for information about Gourmet Restaurant?",
            "Greetings! I'm your personal dining assistant for Gourmet Restaurant."
        ])
    
    restaurant = restaurants[0]
    
    if 'recommend' in message or 'suggest' in message or 'about' in message:
        return f"I recommend {restaurant['name']} in {restaurant['location']}. "\
               f"It serves {restaurant['cuisine']} cuisine with a rating of {restaurant['rating']}. "\
               f"Price range: {restaurant['price_range']}."
    
    if 'hours' in message or 'open' in message or 'timing' in message or 'close' in message:
        return f"Our opening hours are: {restaurant['opening_hours']}"
    
    if 'where' in message or 'location' in message or 'address' in message:
        return f"We are located at: {restaurant['location']}"
    
    if 'menu' in message or 'food' in message or 'dishes' in message or 'serve' in message:
        menu_response = f"{restaurant['name']} menu:\n"
        for category, items in restaurant['menu'].items():
            menu_response += f"\n{category.title()}:\n- " + "\n- ".join(items)
        return menu_response
    
    if 'parking' in message or 'car' in message:
        return f"Parking information: {restaurant['parking']}"
    
    if 'order' in message or 'delivery' in message or 'takeaway' in message:
        services = ", ".join(restaurant['delivery']['services'])
        return f"We offer takeaway and delivery through {services}. "\
               f"You can also call us directly at {restaurant['delivery']['contact']} to place an order."
    
    if 'thank' in message or 'thanks' in message or 'appreciate' in message:
        return random.choice([
            "You're welcome! Enjoy your dining experience!",
            "Happy to help! Bon appétit!",
            "My pleasure! Let me know if you need anything else."
        ])
    
    if 'special' in message or 'signature' in message or 'best dish' in message:
        return f"Our signature dishes are: {', '.join(restaurant['signature_dishes'])}"
    
    if 'price' in message or 'cheap' in message or 'expensive' in message or 'cost' in message:
        return f"Our price range is {restaurant['price_range']} "\
               "($ = budget, $$ = moderate, $$$ = upscale)"
    
    return "I'm your Gourmet Restaurant assistant. You can ask me about:\n"\
           "- Our menu\n- Opening hours\n- Location\n- Parking\n"\
           "- Signature dishes\n- Price range\n- Ordering options\n\n"\
           "Try asking: 'What's on the menu?' or 'What are your opening hours?'"

if __name__ == '__main__':
    app.run(debug=True)