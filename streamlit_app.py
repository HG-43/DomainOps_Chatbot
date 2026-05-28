import streamlit as st
import time
import json
import os
from openai import OpenAI

# Import your custom functional backend modules
import knowledge_rag
import domain_tools

# --- CONFIGURATION ---
PRIMARY_MODEL = "meta-llama/llama-3.3-70b-instruct"
FALLBACK_MODEL = "meta-llama/llama-3.2-3b-instruct"

# --- UI STYLE INJECTION (Theme-Agnostic & Corporate Minimalist) ---
st.set_page_config(page_title="SwiftSupport India", layout="centered")

st.markdown("""
    <style>
    /* Safely hide the deploy button and default footer footprint */
    .stAppDeployButton, .stDeployButton { display: none !important; visibility: hidden !important; }
    footer { visibility: hidden; }
    
    /* Clean, high-contrast typography adjustments */
    h1 { font-family: 'Inter', -apple-system, sans-serif; font-weight: 700; letter-spacing: -0.02em; }
    .stCaption { font-size: 1rem; letter-spacing: 0.01em; }
    
    /* Sleek corporate primary action button styling */
    div.stButton > button:first-child {
        background-color: #0066cc; 
        color: white; 
        border-radius: 6px; 
        border: none; 
        font-weight: 500;
        padding: 0.5rem 1.5rem;
        transition: background-color 0.2s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #0052a3;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("SwiftSupport India")
st.caption("Official Corporate Support Portal | Bengaluru Hub")
st.markdown("---")

# SECRETS DEPLOYMENT AUDITOR
if "OPENROUTER_API_KEY" in st.secrets:
    api_key = st.secrets["OPENROUTER_API_KEY"]
else:
    st.error("Missing system authentication credentials configuration parameters.")
    st.stop()

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

# Tool Manifest
tools_manifest = [
    {
        'type': 'function',
        'function': {
            'name': 'calculate_restocking_fee',
            'description': 'Calculates the 15% restocking fee if a return product box is damaged or missing.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'item_price': {'type': 'number', 'description': 'The original retail price of the item.'},
                    'is_box_damaged': {'type': 'boolean', 'description': 'True if the packaging box is missing or damaged.'}
                },
                'required': ['item_price', 'is_box_damaged']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'evaluate_shipping_carrier',
            'description': 'Determines the shipping carrier based on destination.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'destination_country': {'type': 'string', 'description': 'The destination country.'}
                },
                'required': ['destination_country']
            }
        }
    }
]

# --- SIDEBAR CONTROL CORE ---
with st.sidebar:
    st.header("Help Desk Information")
    st.info("System Status: Operational")
    st.markdown("---")
    
    with st.expander("Store Policies"):
        if os.path.exists("core_policy.txt"):
            with open("core_policy.txt", "r", encoding="utf-8") as f:
                st.caption(f.read())
        else:
            st.caption("Store guidelines are currently undergoing updates.")
            
    with st.expander("Frequently Asked Questions"):
        st.markdown("""
        * Account verification processes
        * Return fee calculation rules for items missing packaging
        * Distribution network lookup for domestic regions
        """)

# CHAT LAYER MEMORY INITIALIZATION
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- MAIN WORKFLOW: GUIDED MENU OPTIONS ---
st.subheader("Select an issue category to begin:")
user_intent = st.selectbox(
    "Choose an option below:",
    [
        "Select your issue category...",
        "Calculate Return & Restocking Fee",
        "Verify Shipping Carrier & Delivery Network",
        "Review Store Policies",
        "General Support Chat"
    ],
    label_visibility="collapsed"
)

st.markdown("---")

base_system = (
    "You are SwiftSupport India, a professional and concise customer care agent.\n"
    "Answer the user's specific selection precisely based on the corporate manual rules.\n"
    "Do not use casual phrases, exclamation marks, or technical terms like JSON, functions, or tools.\n"
)

# --- DYNAMIC INTERFACE ROUTING ---
if user_intent == "Calculate Return & Restocking Fee":
    st.write("### Return Fee Calculator")
    item_price_input = st.number_input("Enter the original purchase price of your item:", min_value=0.0, value=1000.0, step=500.0)
    box_status = st.radio("What is the current condition of the original product packaging?", ["Perfect and Sealed", "Damaged, Opened, or Completely Missing"])
    
    if st.button("Calculate Final Refund"):
        is_damaged = True if box_status == "Damaged, Opened, or Completely Missing" else False
        fee = domain_tools.calculate_restocking_fee(item_price_input, is_damaged)
        refund_amt = item_price_input - fee
        
        st.markdown("#### Calculation Summary:")
        st.markdown(f"* Restocking Fee: INR {fee:,.2f}")
        st.markdown(f"* Estimated Refund Amount: INR {refund_amt:,.2f}")

elif user_intent == "Verify Shipping Carrier & Delivery Network":
    st.write("### Courier Network Lookup")
    dest_country = st.text_input("Enter your shipping destination city or country:", placeholder="e.g., Mumbai, United Kingdom, France...")
    
    if st.button("Verify Shipping Partner") and dest_country:
        if "india" in dest_country.lower() or any(city in dest_country.lower() for city in ["mumbai", "delhi", "bengaluru", "chennai", "kolkata"]):
            st.info("Delivery Network: Delhivery Express / Blue Dart")
        else:
            carrier = domain_tools.evaluate_shipping_carrier(dest_country)
            st.info(f"Delivery Network: {carrier}")

elif user_intent == "Review Store Policies":
    st.write("### Official Store Return Policies")
    context_data = knowledge_rag.retrieve_domain_context("return policy window")
    st.info(context_data)

elif user_intent == "General Support Chat":
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    if chat_input := st.chat_input("Type your inquiry here..."):
        with st.chat_message("user"):
            st.markdown(chat_input)
        st.session_state.messages.append({"role": "user", "content": chat_input})
        
        with st.spinner("Processing..."):
            context = knowledge_rag.retrieve_domain_context(chat_input)
            full_prompt = f"{base_system}\nSTORE POLICY MANUAL:\n{context}"
            
            try:
                res = client.chat.completions.create(
                    model=PRIMARY_MODEL,
                    messages=[{"role": "system", "content": full_prompt}, {"role": "user", "content": chat_input}]
                )
                output = res.choices[0].message.content
            except:
                res = client.chat.completions.create(
                    model=FALLBACK_MODEL,
                    messages=[{"role": "system", "content": full_prompt}, {"role": "user", "content": chat_input}]
                )
                output = res.choices[0].message.content
                
        with st.chat_message("assistant"):
            st.markdown(output)
        st.session_state.messages.append({"role": "assistant", "content": output})