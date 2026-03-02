'''
Docstring for restaurant.frontend.complete_app
'''
import streamlit as st
import time
import random
import pytz
import os
from datetime import datetime
import requests

# Backend URL
BACKEND_URL = "http://localhost:8000"

def check_backend():
    try:
        response = requests.get(f"{BACKEND_URL}/", timeout=2)
        if response.status_code == 200:
            data = response.json()
            is_db_connected = "connected to Atlas" in data.get("database", "")
            return True, is_db_connected
        return True, False
    except Exception:
        return False, False

backend_available, db_connected = check_backend()

# Helper to get current meal time
def get_current_meal_time():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    hour = now.hour

    if 6 <= hour < 12:
        return "Morning (Breakfast)"
    elif 12 <= hour < 16:
        return "Afternoon (Lunch)"
    elif 16 <= hour < 19:
        return "Evening (Snacks)"
    else:
        return "Night (Dinner)"

def send_order_to_backend(order_data):
    """Send order data to backend for MongoDB storage"""
    try:
        response = requests.post(f"{BACKEND_URL}/order/place", json=order_data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            return True, result.get("order_id", "unknown")
        else:
            print(f"Backend error: {response.status_code} - {response.text}")
            return False, None
    except Exception as e:
        print(f"Failed to connect to backend: {str(e)}")
        return False, None

# --- Configuration ---
st.set_page_config(page_title="Foodie Hub | Premium Dining", page_icon="🍽️", layout="wide")

# Custom CSS for beautiful, attractive and creative design
st.markdown("""
<style>
/* Import beautiful fonts */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500;600&display=swap');

/* Global styles */
.stApp {
    background: url('https://images.unsplash.com/photo-1512621776951-a57141f2eefd?ixlib=rb-4.0.3&auto=format&fit=crop&w=1950&q=80') center/cover no-repeat fixed;
    background-size: cover;
    font-family: 'Inter', sans-serif;
}

.stApp::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, rgba(0, 150, 136, 0.5) 0%, rgba(77, 182, 172, 0.4) 50%, rgba(38, 166, 154, 0.5) 100%);
    z-index: -1;
}

/* Main content container */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* Title styling */
h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: 3.5rem !important;
    font-weight: 700 !important;
    color: white !important;
    text-align: center !important;
    text-shadow: 2px 4px 8px rgba(0,0,0,0.8) !important;
    margin-bottom: 0.5rem !important;
}

/* Subtitle styling */
h3 {
    font-family: 'Inter', sans-serif !important;
    font-size: 1.3rem !important;
    font-weight: 400 !important;
    color: white !important;
    text-align: center !important;
    margin-bottom: 2rem !important;
}

/* Section headers */
h2 {
    font-family: 'Playfair Display', serif !important;
    font-size: 2rem !important;
    font-weight: 600 !important;
    color: white !important;
    margin-bottom: 1.5rem !important;
    padding-bottom: 0.5rem !important;
    border-bottom: 3px solid #FF6B6B !important;
    display: inline-block !important;
}

/* Card styling for sections */
[data-testid="stVerticalBlock"] > div[style*="flex-direction: column"] > div[style*="border-radius"] {
    background: rgba(255, 255, 255, 0.95) !important;
    backdrop-filter: blur(10px) !important;
    border-radius: 20px !important;
    padding: 2rem !important;
    margin: 1rem 0 !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    color: white !important;
}

/* Make all text white for better contrast */
.stMarkdown, .stText, p, span, div, label {
    color: white !important;
}

/* Button styling */
.stButton > button {
    background: linear-gradient(45deg, #FF6B6B, #4ECDC4) !important;
    color: white !important;
    border: none !important;
    border-radius: 25px !important;
    padding: 12px 28px !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4) !important;
    background: linear-gradient(45deg, #FF5252, #26A69A) !important;
}

/* Primary button styling */
.stButton > button[type="primary"] {
    background: linear-gradient(45deg, #4ECDC4, #45B7D1) !important;
    box-shadow: 0 4px 15px rgba(78, 205, 196, 0.3) !important;
}

.stButton > button[type="primary"]:hover {
    background: linear-gradient(45deg, #26A69A, #2196F3) !important;
    box-shadow: 0 8px 25px rgba(78, 205, 196, 0.4) !important;
}

/* Input field styling */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    border-radius: 12px !important;
    border: 2px solid #E0E0E0 !important;
    padding: 14px 16px !important;
    font-size: 16px !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.3s ease !important;
    background: rgba(255, 255, 255, 0.9) !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #4ECDC4 !important;
    box-shadow: 0 0 0 3px rgba(78, 205, 196, 0.1) !important;
    background: white !important;
}

/* Number input styling */
.stNumberInput > div > div > input {
    border-radius: 12px !important;
    border: 2px solid #E0E0E0 !important;
    padding: 14px 16px !important;
    font-size: 16px !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.3s ease !important;
    background: rgba(255, 255, 255, 0.9) !important;
}

/* Radio button styling */
.stRadio > div {
    background: rgba(255, 255, 255, 0.9) !important;
    border-radius: 12px !important;
    padding: 20px !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
}

/* Success message styling */
.stSuccess {
    background: linear-gradient(45deg, #4ECDC4, #45B7D1) !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
    color: white !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
}

/* Error message styling */
.stError {
    background: linear-gradient(45deg, #FF6B6B, #FF8E53) !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
    color: white !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
}

/* Warning message styling */
.stWarning {
    background: linear-gradient(45deg, #FFA726, #FB8C00) !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
    color: white !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
}

/* Chat message styling */
.stChatMessage {
    border-radius: 18px !important;
    margin: 12px 0 !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
    backdrop-filter: blur(10px) !important;
}

/* Chat input styling */
.stChatInput > div > div > textarea {
    border-radius: 25px !important;
    border: 2px solid rgba(255, 255, 255, 0.3) !important;
    padding: 14px 20px !important;
    font-size: 16px !important;
    font-family: 'Inter', sans-serif !important;
    background: rgba(255, 255, 255, 0.95) !important;
}

/* Column styling for better layout */
.stColumn {
    padding: 0 8px !important;
}

/* Divider styling */
hr {
    border: none !important;
    height: 2px !important;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent) !important;
    margin: 2rem 0 !important;
}

/* Markdown content styling */
.stMarkdown {
    font-family: 'Inter', sans-serif !important;
}

/* Price and amount styling */
.markdown-text-container strong {
    color: white !important;
    font-weight: 600 !important;
}

/* Order summary styling */
.stMarkdown > div > div > p {
    background: rgba(255, 255, 255, 0.1) !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
    margin: 4px 0 !important;
}

/* Form section headers */
.stMarkdown > div > div > h4 {
    color: white !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 1.3rem !important;
    font-weight: 600 !important;
    margin-bottom: 1rem !important;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
    h1 {
        font-size: 2.5rem !important;
    }
    
    .stButton > button {
        padding: 10px 20px !important;
        font-size: 14px !important;
    }
    
    .stColumn {
        padding: 0 4px !important;
    }
}

/* Animated background elements */
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

.floating-element {
    animation: float 6s ease-in-out infinite;
}
</style>
""", unsafe_allow_html=True)

if "step" not in st.session_state:
    st.session_state.step = "GREETING"
if "order_details" not in st.session_state:
    st.session_state.order_details = {
        "people": 4,
        "appetite": None,
        "preference": None,
        "cart": {}
    }
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "prepared" not in st.session_state:
    st.session_state.prepared = False
if "message_added" not in st.session_state:
    st.session_state.message_added = False
if "backend_order_id" not in st.session_state:
    st.session_state.backend_order_id = None

# --- Helper Functions ---
def add_message(role, content):
    st.session_state.chat_history.append({"role": role, "content": content})

# --- Menu Data ---
MENU = {
    "Morning (Breakfast)": {
        "Veg": [
            {"name": "Masala Dosa", "price": 120, "image": "https://images.unsplash.com/photo-1587899899017-21858dc0623f?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"},
            {"name": "Idli Vada", "price": 80, "image": "https://images.unsplash.com/photo-1586200858069-5d01b4d5e4b8?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"},
            {"name": "Poha", "price": 60, "image": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"},
            {"name": "Chole bhature", "price": 100, "image": "https://images.unsplash.com/photo-1565958011703-44f9829ba56f?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"},
            {"name": "Bonda", "price": 70, "image": "https://images.unsplash.com/photo-1604503434322-12e1d3a6f52e?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"}
        ],
        "Non-Veg": [
            {"name": "Bread Omelette", "price": 80, "image": "https://images.unsplash.com/photo-1586190848861-99aa4a171e90?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"},
            {"name": "Chicken Keema Paratha", "price": 180, "image": "https://images.unsplash.com/photo-1563379091339-03246964d5c2?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"},
            {"name": "Egg Bhurji", "price": 90, "image": "https://images.unsplash.com/photo-1586200858069-5d01b4d5e4b8?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"},
            {"name": "Chicken sausages", "price": 70, "image": "https://insanelygoodrecipes.com/wp-content/uploads/2021/12/Homemade-Fried-Chicken-Sausage-with-Garlic-Butter-Sauce-and-Lemons.jpg"},
            {"name": "Chicken cutlet", "price": 90, "image": "https://therecipemaster.com/wp-content/uploads/2024/09/Chicken-Cutlet-Recipe-Card.webp"}
        ]
    },
    "Afternoon (Lunch)": {
        
        "Veg": [
            {"name": "Veg Biryani", "price": 280, "image": "https://img.freepik.com/premium-photo/traditional-indian-veg-biryani-banana-leaf_1179130-190160.jpg?w=2000"},
            {"name": "Palak Paneer with chapthi", "price": 220, "image": "https://img.freepik.com/premium-photo/indian-palak-paneer-with-spinach-cottage-cheese_1072167-2540.jpg?w=2000"},
            {"name": "North Indian Thali", "price": 350, "image": "https://i.pinimg.com/originals/e1/da/d5/e1dad5315972c8a9db86fb01d69c7ecb.jpg"},
            {"name": "South Indian Thali", "price": 320, "image": "https://wp.scoopwhoop.com/wp-content/uploads/2014/09/567731556e510a6f3a759a4d_south.jpg"},
            {"name": "Pallav", "price": 70, "image": "https://1.bp.blogspot.com/-Yf00fooZes8/WrMJKwxMVOI/AAAAAAAAgtg/32-H3Ym2iDk-enkac6zUIuRGneGk3vyoQCEwYBhgL/w1200-h630-p-k-no-nu/226.jpg"}
        ],
        "Non-Veg": [
           {"name": "Chicken Biryani", "price": 300, "image": "https://static.vecteezy.com/system/resources/previews/040/703/949/non_2x/ai-generated-royal-feast-master-the-art-of-chicken-biryani-at-home-generative-ai-photo.jpg"},
           {"name": "Mutton Curry", "price": 450, "image": "https://uploads-ssl.webflow.com/5c481361c604e53624138c2f/60f2eb0d5d007bd81723ebe2_Mutton%20curry_1500%20x%201200.jpg"},
           {"name": "Fish Curry", "price": 380, "image": "https://paattiskitchen.com/wp-content/uploads/2023/01/kmc_20230110_191241-1.jpg"},
           {"name": "Egg Curry", "price": 210, "image": "https://static.vecteezy.com/system/resources/previews/050/436/451/large_2x/spicy-indian-egg-curry-served-parathas-garnished-with-fresh-coriander-and-a-side-of-raita-photo.jpg"},
           {"name": "Chicken Fried Rice", "price": 100, "image": "https://houseofnasheats.com/wp-content/uploads/2023/01/Chicken-Fried-Rice-Recipe-10-680x1018.jpg"}
        ]
    },
    "Evening (Snacks)": {
        "Veg": [
            {"name": "Paneer Tikka", "price": 290, "image": "https://img.freepik.com/premium-photo/photography-tasty-indian-paneer-tikka_1288657-46631.jpg"},
            {"name": "Samosa (3 pcs)", "price": 50, "image": "https://thehimalayantreasure.pl/wp-content/uploads/2018/09/chicken-samosa.jpg"},
            {"name": "Veg Puff", "price": 40, "image": "https://i.pinimg.com/736x/df/31/74/df3174666a44cd060e1eb6d59938d76c--puffs-spicy.jpg"},
            {"name": "French Fries", "price": 120, "image": "https://wallpapers.com/images/hd/french-fries-960-x-960-picture-317878ocb9hyulx0.jpg"}
        ],
        "Non-Veg": [
            {"name": "Chicken Nuggets", "price": 200, "image": "http://www.proofdc.com/wp-content/uploads/media/02/58716144-crispy-baked-chicken-nuggets-recipe-proofdc.jpg"},
            {"name": "Chicken Popcorn", "price": 220, "image": "https://wallpaperaccess.com/full/12256759.jpg"},
            {"name": "Egg Puff", "price": 50, "image": "https://nodashofgluten.com/wp-content/uploads/2025/02/Egg-Puff-Recipe-Kerala-Style-3.png.webp"},
            {"name": "Grilled Chicken Wings", "price": 280, "image": "https://recipeslily.com/wp-content/uploads/2024/07/grilled-wings-recipe.jpg"}
        ]
    },
    "Night (Dinner)": {
        "Veg": [
            {"name": "Butter Naan & Paneer", "price": 350, "image": "https://media-cdn.tripadvisor.com/media/photo-m/1280/1a/54/fd/77/paneer-butter-masala.jpg"},
            {"name": "Veg Fried Rice", "price": 240, "image": "https://thedelishrecipe.com/wp-content/uploads/2024/05/vegetable-fried-rice.jpg"},
            {"name": "Malai Kofta", "price": 330, "image": "https://www.mrishtanna.com/wp-content/uploads/2023/11/malai-kofta-curry-recipe.jpg"},
            {"name": "Mushroom Masala", "price": 310, "image": "https://www.cookingcarnival.com/wp-content/uploads/2018/09/Mushroom-masala.webp"}
        ],
        "Non-Veg": [
            {"name": "Tandoori Chicken", "price": 280, "image": "https://img.freepik.com/premium-photo/indian-spices-barbecue-murgh-tandoori-tandoori-chicken-with-raita-lime-chapati-onion-rings-served-dish-isolated-dark-background-top-view-food_689047-1446.jpg?w=1380"},
            {"name": "Chicken Curry & Roti", "price": 320, "image": "https://themayakitchen.com/wp-content/uploads/2019/06/CURRY.jpg"},
            {"name": "Prawns Masala", "price": 420, "image": "https://rumkisgoldenspoon.com/wp-content/uploads/2022/08/Prawn-masala-recipe-2.jpg"},
            {"name": "Chicken Soup", "price": 180, "image": "https://thefoodxp.com/wp-content/uploads/2022/11/Jamie-Oliver-Chicken-Soup-Recipe-1.jpg"}
        ]
    },
    "Sweets": [
        {"name": "Gulab Jamun (2 pcs)", "price": 60, "image": "https://media.chefdehome.com/740/0/0/gulab-jamun/indian-gulab-jamun-chefdehome-1.jpg"},
        {"name": "Rasgulla (2 pcs)", "price": 70, "image": "https://www.aonesamosa.com/wp-content/uploads/2023/12/Rasgulla.webp"},
        {"name": "Ice Cream (Vanilla)", "price": 50, "image": "https://wallpapers.com/images/hd/ice-cream-pictures-93ucnuf5kr7ghmhg.jpg"},
        {"name": "Chocolate Brownie", "price": 120, "image": "https://tse4.mm.bing.net/th/id/OIP.2eWvcwOeJpY7YgwNfRsJjAHaKX?rs=1&pid=ImgDetMain&o=7&rm=3"}
    ]
}

# --- Sidebar / Header ---
st.title("🍽️ Foodie Hub")
current_meal_time = get_current_meal_time()
st.markdown(f"### 🕐 {current_meal_time}")

# Backend status indicator
try:
    response = requests.get(f"{BACKEND_URL}/status", timeout=3)
    if response.status_code == 200:
        status_data = response.json()
        if status_data.get("status") == "healthy":
            st.success("🟢 Backend Connected - MongoDB Ready")
        else:
            st.warning("🟡 Backend Partial Connection")
    else:
        st.error("🔴 Backend Connection Error")
except:
    st.warning("🟡 Backend Offline - Using Local Mode")

st.markdown("---")

# --- Chat Display ---
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- State Machine Logic ---

# 1. GREETING
if st.session_state.step == "GREETING":
    if not st.session_state.chat_history:
        with st.chat_message("assistant"):
            text = "👋 Welcome to Foodie Hub! I'll help you place your order quickly 😊 Before we start, I need a few details. 👉 **How many people are dining today?**"
            add_message("assistant", text)
            st.markdown(text)
    
    people = st.chat_input("Enter number of people...")
    if people:
        add_message("user", people)
        with st.chat_message("user"):
            st.markdown(people)
        
        try:
            st.session_state.order_details["people"] = int(people)
            st.session_state.step = "ASK_APPETITE"
            st.rerun()
        except ValueError:
            st.error("Please enter a valid number.")

# 2. ASK APPETITE
elif st.session_state.step == "ASK_APPETITE":
    if len(st.session_state.chat_history) < 3:
        msg = f"Great! 👨👩👧👦 for {st.session_state.order_details['people']} people. 👉 **What is your eating capacity?**"
        add_message("assistant", msg)
        st.rerun()

    st.write("Please choose your eating style:")
    col1, col2, col3 = st.columns(3)
    if col1.button("🥗 **Low** (Light eaters 🧒)"):
        st.session_state.order_details["appetite"] = "Low"
        add_message("user", "Low - Light eaters 🧒")
        st.session_state.step = "ASK_PREFERENCE"
        st.rerun()
    if col2.button("🍱 **Medium** (Standard Foodie 🧔)"):
        st.session_state.order_details["appetite"] = "Medium"
        add_message("user", "Medium - Standard Foodie 🧔")
        st.session_state.step = "ASK_PREFERENCE"
        st.rerun()
    if col3.button("🍖 **Large** (Hungry Kings 🤴)"):
        st.session_state.order_details["appetite"] = "Large"
        add_message("user", "Large - Hungry Kings 🤴")
        st.session_state.step = "ASK_PREFERENCE"
        st.rerun()

# 3. ASK PREFERENCE
elif st.session_state.step == "ASK_PREFERENCE":
    if len(st.session_state.chat_history) < 5:
        msg = "Perfect 🍽️ 👉 **Please choose your food preference:**"
        add_message("assistant", msg)
        st.rerun()

    col1, col2 = st.columns(2)
    if col1.button("🥦 Veg"):
        st.session_state.order_details["preference"] = "Veg"
        st.session_state.order_details["timing"] = get_current_meal_time()
        add_message("user", "Veg")
        st.session_state.step = "CHECKOUT"
        st.rerun()
    if col2.button("🍗 Non-Veg"):
        st.session_state.order_details["preference"] = "Non-Veg"
        st.session_state.order_details["timing"] = get_current_meal_time()
        add_message("user", "Non-Veg")
        st.session_state.step = "CHECKOUT"
        st.rerun()

# 4. CHECKOUT
elif st.session_state.step == "CHECKOUT":
    pref = st.session_state.order_details.get("preference", "Veg")
    timing = st.session_state.order_details.get("timing", "Dinner")
    num_people = st.session_state.order_details.get("people", 1)
    
    last_msg = st.session_state.chat_history[-1]["content"] if st.session_state.chat_history else ""
    if last_msg in ["Veg", "Non-Veg"]:
        msg = f"🍽️ Perfect! I've prepared a **{timing}** package for {num_people} people. ✨"
        add_message("assistant", msg)

    # --- Bundle Calculation ---
    if not st.session_state.prepared:
        available_items = MENU[timing][pref]
        used_items = []
        
        appetite = st.session_state.order_details.get("appetite", "Medium")
        if "Low" in appetite:
            portion_factor = 0.7
        elif "Large" in appetite:
            portion_factor = 1.3
        else:
            portion_factor = 1.0

        def get_unique_items(keywords, count):
            selected = []
            for item in available_items:
                if any(k.lower() in item["name"].lower() for k in keywords) and item["name"] not in [i["name"] for i in used_items]:
                    selected.append(item); used_items.append(item)
                    if len(selected) == count: return selected
            for item in available_items:
                if item["name"] not in [i["name"] for i in used_items]:
                    selected.append(item); used_items.append(item)
                    if len(selected) == count: return selected
            return selected

        # Get categorized items - more comprehensive keyword matching
        roti_list = get_unique_items(["Roti", "Naan", "Dosa", "Paratha", "Bhature", "Chapathi", "Chapthi"], 1)
        # Give fewer varieties of curries/rice to avoid overwhelming the order
        curry_list = get_unique_items(["Curry", "Paneer", "Kofta", "Masala", "Tikka", "Mushroom", "Malai"], 2 if num_people >= 6 else 1)
        rice_list = get_unique_items(["Rice", "Biryani", "Pallav", "Poha", "Fried Rice"], 1)
        # Try to get thali items specifically
        thali_list = get_unique_items(["Thali"], 1)
        # Get other specialty items
        special_list = get_unique_items(["Bonda", "Chole", "Idli", "Vada"], 1)
        sweet_list = [next((item for item in MENU["Sweets"] if "Jamun" in item["name"]), MENU["Sweets"][0])]

        # Build final bundle for cart with improved portion logic
        bundle = []
        
        # Roti/Bread: 1 per person adjusted by appetite
        if roti_list:
            bundle.append({"item": roti_list[0], "qty": max(1, round(num_people * portion_factor))})
        
        # Curries: 1 bowl per 2-3 people
        if curry_list:
            total_curry_qty = max(1, round((num_people * portion_factor) / 2.5))
            qty_per_curry = max(1, total_curry_qty // len(curry_list))
            for c in curry_list:
                bundle.append({"item": c, "qty": qty_per_curry})

        # Rice: 1 plate per 3 people if roti is present, else 1 per person
        if rice_list:
            rice_div = 3.0 if roti_list else 1.2
            bundle.append({"item": rice_list[0], "qty": max(1, round((num_people * portion_factor) / rice_div))})

        # Thali: 1 per 2-3 people (complete meal)
        if thali_list:
            bundle.append({"item": thali_list[0], "qty": max(1, round((num_people * portion_factor) / 2.5))})

        # Special items: 1 per 3-4 people
        if special_list:
            bundle.append({"item": special_list[0], "qty": max(1, round((num_people * portion_factor) / 3.5))})

        # Sweets: 1 per person
        if sweet_list:
            bundle.append({"item": sweet_list[0], "qty": max(1, round(num_people * portion_factor))})

        # Auto-fill the cart
        st.session_state.order_details["cart"] = {}
        for rec in bundle:
            item_data = rec["item"].copy()
            item_data["quantity"] = rec["qty"]
            st.session_state.order_details["cart"][item_data["name"]] = item_data
        st.session_state.prepared = True

    # --- UI: Cart Display with WORKING buttons ---
    current_meal = get_current_meal_time()
    st.markdown(f"### 🍱 Recommended Package for {num_people} People")
    st.markdown(f"#### 🕐 {current_meal}")

    total_price = 0
    cart = st.session_state.order_details["cart"]

    if not cart:
        st.write("Your cart is empty.")
    else:
        # Collect actions
        actions = []

        for item_name, item_data in list(cart.items()):
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([1, 3, 1, 1, 1])

                with col1:
                    st.image(item_data["image"], width=70)

                with col2:
                    st.markdown(f"#### {item_data['name']}")

                with col3:
                    # Minus button
                    if st.button("➖", key=f"minus_{item_name}"):
                        actions.append(("minus", item_name))

                with col4:
                    st.markdown(f"**{st.session_state.order_details['cart'][item_name]['quantity']}**")

                with col5:
                    # Plus button
                    if st.button("➕", key=f"plus_{item_name}"):
                        actions.append(("plus", item_name))

                # Delete button
                if st.button("🗑️ Delete", key=f"delete_{item_name}"):
                    actions.append(("delete", item_name))

                # Price display
                st.markdown(f"**₹{item_data['price'] * st.session_state.order_details['cart'][item_name]['quantity']}**")

                total_price += item_data["price"] * st.session_state.order_details['cart'][item_name]['quantity']

        # Process actions
        if actions:
            for action, item_name in actions:
                if action == "minus":
                    if st.session_state.order_details["cart"][item_name]["quantity"] > 1:
                        st.session_state.order_details["cart"][item_name]["quantity"] -= 1
                elif action == "plus":
                    st.session_state.order_details["cart"][item_name]["quantity"] += 1
                elif action == "delete":
                    if item_name in st.session_state.order_details["cart"]:
                        del st.session_state.order_details["cart"][item_name]
            st.rerun()

    st.markdown(f"### Total Amount: ₹{total_price}")
    st.markdown("---")

    # Order modification and completion options
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Modify Order", key="modify_order"):
            st.session_state.step = "MODIFY_ORDER"
            st.rerun()
    
    with col2:
        if st.button("✅ Complete Order", key="complete_order"):
            if cart:
                st.session_state.step = "CUSTOMER_VERIFICATION"
                st.rerun()
            else:
                st.error("Your cart is empty! Please add items to complete the order.")

# 5. MODIFY ORDER
elif st.session_state.step == "MODIFY_ORDER":
    st.markdown("### 🔄 Modify Your Order")
    
    # Add more items section first
    st.markdown("### 🍽️ Add More Items")
    
    current_meal = get_current_meal_time()
    pref = st.session_state.order_details.get("preference", "Veg")
    
    # Show available items not in cart
    available_items = MENU[current_meal][pref]
    cart_items = list(st.session_state.order_details["cart"].keys())
    
    items_to_add = [item for item in available_items if item["name"] not in cart_items]
    
    if items_to_add:
        for item in items_to_add:
            col1, col2, col3 = st.columns([1, 3, 1])
            
            with col1:
                st.image(item["image"], width=60)
            
            with col2:
                st.markdown(f"**{item['name']}** - ₹{item['price']}")
            
            with col3:
                if st.button("Add", key=f"add_{item['name']}"):
                    item_data = item.copy()
                    item_data["quantity"] = 1
                    st.session_state.order_details["cart"][item_data["name"]] = item_data
                    st.rerun()
    else:
        st.write("All items from this category are already in your cart!")
    
    st.markdown("---")
    
    # Show current cart (now includes newly added items)
    st.markdown("### 🛒 Your Current Cart")
    
    cart = st.session_state.order_details["cart"]
    total_price = 0
    
    if not cart:
        st.write("Your cart is empty.")
    else:
        for item_name, item_data in list(cart.items()):
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([1, 3, 1, 1, 1])
                
                with col1:
                    st.image(item_data["image"], width=70)
                
                with col2:
                    st.markdown(f"#### {item_data['name']}")
                
                with col3:
                    if st.button("➖", key=f"modify_minus_{item_name}"):
                        if st.session_state.order_details["cart"][item_name]["quantity"] > 1:
                            st.session_state.order_details["cart"][item_name]["quantity"] -= 1
                        st.rerun()
                
                with col4:
                    st.markdown(f"**{st.session_state.order_details['cart'][item_name]['quantity']}**")
                
                with col5:
                    if st.button("➕", key=f"modify_plus_{item_name}"):
                        st.session_state.order_details["cart"][item_name]["quantity"] += 1
                        st.rerun()
                
                # Delete button
                if st.button("🗑️ Delete", key=f"modify_delete_{item_name}"):
                    if item_name in st.session_state.order_details["cart"]:
                        del st.session_state.order_details["cart"][item_name]
                    st.rerun()
                
                # Price display
                st.markdown(f"**₹{item_data['price'] * st.session_state.order_details['cart'][item_name]['quantity']}**")
                
                total_price += item_data["price"] * st.session_state.order_details['cart'][item_name]['quantity']
    
    st.markdown(f"### Total Amount: ₹{total_price}")
    st.markdown("---")
    
    # Action buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Done Modifying"):
            st.session_state.step = "CHECKOUT"
            st.rerun()
    
    with col2:
        if st.button("❌ Cancel"):
            st.session_state.step = "CHECKOUT"
            st.rerun()

# 6. CUSTOMER VERIFICATION
elif st.session_state.step == "CUSTOMER_VERIFICATION":
    st.markdown("### 📝 Customer Details & Verification")
    
    # Order summary
    cart = st.session_state.order_details["cart"]
    total_price = 0
    
    st.markdown("#### 📋 Order Summary:")
    for item_name, item_data in cart.items():
        st.markdown(f"- **{item_data['quantity']}x {item_name}** - ₹{item_data['price'] * item_data['quantity']}")
        total_price += item_data["price"] * item_data['quantity']
    
    st.markdown(f"#### 💰 Total Amount: ₹{total_price}")
    st.markdown("---")
    
    # Customer details form
    st.markdown("#### 👤 Personal Information:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name*", placeholder="Enter your full name", 
                            value=st.session_state.order_details.get("customer_info", {}).get("name", ""))
        mobile = st.text_input("Mobile Number*", placeholder="Enter 10-digit mobile number",
                              value=st.session_state.order_details.get("customer_info", {}).get("mobile", "") if st.session_state.order_details.get("customer_info", {}).get("mobile") != "Not Provided" else "")
        
    with col2:
        address = st.text_area("Delivery Address*", placeholder="Enter your delivery address",
                              value=st.session_state.order_details.get("customer_info", {}).get("address", ""))
        notes = st.text_area("Special Notes (Optional)", placeholder="Any special requests?",
                            value=st.session_state.order_details.get("customer_info", {}).get("notes", ""))
    
    # OTP Section
    st.markdown("#### 🔐 Mobile Verification:")
    
    # Mobile OTP
    if st.button("📱 Send OTP to Mobile", key="send_mobile_otp"):
        if mobile and len(mobile) == 10 and mobile.isdigit():
            st.session_state.mobile_otp = "123456"  # Demo OTP
            st.session_state.mobile_otp_sent = True
            st.success(f"Demo OTP sent to {mobile}: 123456")
        else:
            st.error("Please enter a valid 10-digit mobile number")
    
    if st.session_state.get("mobile_otp_sent"):
        mobile_otp_input = st.text_input("Enter Mobile OTP*", placeholder="Enter 6-digit OTP", max_chars=6)
        if st.button("✅ Verify Mobile OTP", key="verify_mobile_otp"):
            if mobile_otp_input == st.session_state.get("mobile_otp", ""):
                st.session_state.mobile_verified = True
                st.success("Mobile number verified successfully!")
            else:
                st.error("Invalid OTP. Please try again.")
    
    st.markdown("---")
    
    # Verification status
    if st.session_state.get("mobile_verified"):
        st.success("📱 Mobile Verified")
    else:
        st.warning("📱 Mobile Not Verified")
    
    # Payment method
    st.markdown("#### 💳 Payment Method:")
    payment_method = st.radio("Choose payment method:", ["Cash on Delivery", "UPI Payment", "Credit/Debit Card"],
                            index=0 if not st.session_state.order_details.get("customer_info", {}).get("payment_method") 
                            else ["Cash on Delivery", "UPI Payment", "Credit/Debit Card"].index(
                                st.session_state.order_details.get("customer_info", {}).get("payment_method")))
    
    # UPI Payment Details
    if payment_method == "UPI Payment":
        st.markdown("#### 📱 UPI Payment Details:")
        upi_id = st.text_input("Enter your UPI ID*", placeholder="example@upi", 
                              value=st.session_state.order_details.get("customer_info", {}).get("upi_id", ""))
        upi_apps = st.radio("Select UPI App:", ["Google Pay", "PhonePe", "Paytm", "Amazon Pay", "Other"])
        
        if not upi_id:
            st.warning("Please enter your UPI ID")
        elif "@" not in upi_id:
            st.warning("Please enter a valid UPI ID (e.g., example@upi)")
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Back to Cart"):
            st.session_state.step = "CHECKOUT"
            st.rerun()
    
    with col2:
        if st.button("✅ Proceed to Confirm", type="primary"):
            # Validation
            if not all([name, mobile, address]):
                st.error("Please fill in all required fields (marked with *)")
            elif len(mobile) != 10 or not mobile.isdigit():
                st.error("Please enter a valid 10-digit mobile number")
            elif not st.session_state.get("mobile_verified"):
                st.error("Please verify your mobile number")
            elif payment_method == "UPI Payment" and (not upi_id or "@" not in upi_id):
                st.error("Please enter a valid UPI ID for UPI payment")
            else:
                # Save customer details
                customer_data = {
                    "name": name,
                    "mobile": mobile,
                    "address": address,
                    "notes": notes,
                    "payment_method": payment_method,
                    "total_amount": total_price
                }
                
                # Add UPI details if selected
                if payment_method == "UPI Payment":
                    customer_data["upi_id"] = upi_id
                    customer_data["upi_app"] = upi_apps
                
                st.session_state.order_details["customer_info"] = customer_data
                st.session_state.step = "ORDER_CONFIRMATION"
                st.rerun()
    
    with col3:
        if st.button("❌ Cancel"):
            st.session_state.step = "CHECKOUT"
            st.rerun()

# 7. ORDER CONFIRMATION
elif st.session_state.step == "ORDER_CONFIRMATION":
    st.markdown("### ✅ Final Order Confirmation")
    
    cart = st.session_state.order_details["cart"]
    customer_info = st.session_state.order_details.get("customer_info", {})
    total_price = 0
    
    # Order summary
    st.markdown("#### 📋 Order Summary:")
    for item_name, item_data in cart.items():
        st.markdown(f"- **{item_data['quantity']}x {item_name}** - ₹{item_data['price'] * item_data['quantity']}")
        total_price += item_data["price"] * item_data['quantity']
    
    st.markdown(f"#### 💰 Total Amount: ₹{total_price}")
    st.markdown("---")
    
    # Customer details display (read-only)
    st.markdown("#### � Customer Information:")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Name:** {customer_info.get('name', 'N/A')}")
        st.markdown(f"**Mobile:** {customer_info.get('mobile', 'N/A')}")
        
    with col2:
        st.markdown(f"**Payment Method:** {customer_info.get('payment_method', 'N/A')}")
        mobile_status = "✅ Verified" if st.session_state.get('mobile_verified') else "❌ Not Verified"
        st.markdown(f"**Mobile Status:** {mobile_status}")
        
        # Show UPI details if selected
        if customer_info.get('payment_method') == "UPI Payment":
            st.markdown(f"**UPI ID:** {customer_info.get('upi_id', 'N/A')}")
            st.markdown(f"**UPI App:** {customer_info.get('upi_app', 'N/A')}")
    
    st.markdown(f"**Delivery Address:** {customer_info.get('address', 'N/A')}")
    
    if customer_info.get('notes'):
        st.markdown(f"**Special Notes:** {customer_info['notes']}")
    
    st.markdown("---")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Back to Verification"):
            st.session_state.step = "CUSTOMER_VERIFICATION"
            st.rerun()
    
    with col2:
        if st.button("🎉 Confirm Order", type="primary"):
            if not st.session_state.backend_order_id:  # Only send to backend once
                # Prepare order data for backend
                order_data = {
                    "name": customer_info.get('name'),
                    "mobile": customer_info.get('mobile'),
                    "address": customer_info.get('address'),
                    "notes": customer_info.get('notes'),
                    "cart": cart,
                    "total": total_price,
                    "people": st.session_state.order_details.get('people', 4),
                    "appetite": st.session_state.order_details.get('appetite'),
                    "preference": st.session_state.order_details.get('preference'),
                    "payment_method": customer_info.get('payment_method'),
                    "upi_id": customer_info.get('upi_id'),
                    "upi_app": customer_info.get('upi_app')
                }
                
                # Send to backend
                success, order_id = send_order_to_backend(order_data)
                
                if success:
                    st.session_state.backend_order_id = order_id
                    st.success(f"Order saved to database! Order ID: {order_id}")
                    st.session_state.step = "ORDER_SUCCESS"
                    st.rerun()
                else:
                    st.error("Failed to save order to database. Please try again.")
            else:
                # Already saved, proceed to success
                st.session_state.step = "ORDER_SUCCESS"
                st.rerun()
    
    with col3:
        if st.button("❌ Cancel Order"):
            st.session_state.step = "CHECKOUT"
            st.rerun()

# 8. ORDER SUCCESS
elif st.session_state.step == "ORDER_SUCCESS":
    st.markdown("### 🎉 Order Placed Successfully!")
    
    customer_info = st.session_state.order_details.get("customer_info", {})
    
    st.success(f"Thank you **{customer_info.get('name', 'Customer')}**! Your order has been confirmed.")
    
    st.markdown("#### 📋 Order Details:")
    if st.session_state.backend_order_id:
        st.markdown(f"**Order ID:** {st.session_state.backend_order_id}")
    else:
        st.markdown(f"**Order ID:** #ORD{random.randint(10000, 99999)} (Local)")
    st.markdown(f"**Total Amount:** ₹{customer_info.get('total_amount', 0)}")
    st.markdown(f"**Payment Method:** {customer_info.get('payment_method', 'Cash on Delivery')}")
    
    # Show UPI details if selected
    if customer_info.get('payment_method') == "UPI Payment":
        st.markdown(f"**UPI ID:** {customer_info.get('upi_id', 'N/A')}")
        st.markdown(f"**UPI App:** {customer_info.get('upi_app', 'N/A')}")
    
    st.markdown(f"**Delivery Address:** {customer_info.get('address', 'N/A')}")
    
    st.markdown("#### ⏰ Estimated Delivery Time:")
    st.markdown("**30-45 minutes**")
    
    st.markdown("#### 📞 Contact Information:")
    st.markdown(f"**Mobile:** {customer_info.get('mobile', 'N/A')}")
    
    if customer_info.get('notes'):
        st.markdown(f"**Special Notes:** {customer_info['notes']}")
    
    st.markdown("---")
    st.markdown("### 🙏 Thank you for ordering from Foodie Hub!")
    st.markdown("We hope you enjoy your meal. Visit again soon! 😊")
    
    if st.button("🆕 Place New Order"):
        st.session_state.clear()
        st.session_state.prepared = False
        st.session_state.message_added = False
        st.session_state.backend_order_id = None
        st.rerun()
