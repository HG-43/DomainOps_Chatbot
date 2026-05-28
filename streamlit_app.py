import streamlit as st
import os
from openai import OpenAI

# Import backend utility modules
import knowledge_rag
import domain_tools

# --- CONFIGURATION ---
PRIMARY_MODEL = "meta-llama/llama-3.3-70b-instruct"
FALLBACK_MODEL = "meta-llama/llama-3.2-3b-instruct"

# --- REFINED LOGISTICS ENGINE STYLING ---
st.set_page_config(page_title="SwiftSupport India", layout="centered")

st.markdown("""
    <style>
    /* 1. Structural Cleanups */
    div[data-testid="stAppDeployButton"] { display: none !important; }
    footer { visibility: hidden; }
    
    /* 2. Premium Left-Accent Title Typography */
    .portal-header {
        border-left: 5px solid #2563eb;
        padding-left: 16px;
        margin-bottom: 20px;
        margin-top: 10px;
    }
    .portal-title {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.03em !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1.1 !important;
    }
    
    /* 3. Core Workspace Card Blocks */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: var(--secondary-background-color) !important;
        border: 1px solid rgba(128, 128, 128, 0.15) !important;
        border-radius: 12px !important;
        padding: 26px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02) !important;
    }

    /* 4. High-Contrast Primary Buttons (Logistics Blue) */
    button[kind="primary"] {
        background-color: #2563eb !important;
        color: #ffffff !important;
        border-radius: 6px !important;
        border: none !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 0.55rem 2rem !important;
        box-shadow: 0 2px 5px rgba(37, 99, 235, 0.2) !important;
        transition: background-color 0.15s ease !important;
    }
    button[kind="primary"]:hover {
        background-color: #1d4ed8 !important;
    }
    
    /* 5. Suggestion Chips Layout (Sleek Bordered Badges) */
    button[kind="secondary"] {
        background-color: transparent !important;
        color: var(--text-color) !important;
        border: 1px solid rgba(128, 128, 128, 0.3) !important;
        border-radius: 20px !important;
        padding: 0.4rem 1.2rem !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        width: 100% !important;
        transition: all 0.15s ease-in-out !important;
    }
    button[kind="secondary"]:hover {
        background-color: rgba(37, 99, 235, 0.08) !important;
        border-color: #2563eb !important;
        color: #2563eb !important;
    }
    
    /* 6. Form Label Hierarchy Fixes */
    div[data-testid="stSelectbox"] label p {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: var(--text-color) !important;
        margin-bottom: 6px !important;
    }
    
    /* 7. Native Container Integration Overrides */
    div[data-testid="stNumberInput"], div[data-testid="stTextInput"] input, div[data-testid="stSelectbox"] > div {
        border-radius: 6px !important;
    }

    /* 8. Crisp Live System Badge */
    .status-badge {
        display: inline-flex;
        align-items: center;
        background-color: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.2);
        color: #059669;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 15px;
    }
    .status-dot {
        width: 6px;
        height: 6px;
        background-color: #10b981;
        border-radius: 50%;
        margin-right: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- APP HEADER HERO BLOCK ---
st.markdown("""
    <div class="portal-header">
        <h1 class="portal-title">SwiftSupport India</h1>
        <div style="font-size: 0.95rem; color: rgba(128,128,128,0.8); margin-top: 4px;">Fulfillment, Orders & Dispatch Logistics Hub</div>
    </div>
    """, unsafe_allow_html=True)
st.markdown("---")

# API GATEWAY
if "OPENROUTER_API_KEY" in st.secrets:
    api_key = st.secrets["OPENROUTER_API_KEY"]
else:
    st.error("Configuration Error: OPENROUTER_API_KEY is missing from Streamlit Secrets.")
    st.stop()

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

# --- SIDEBAR PANEL ---
with st.sidebar:
    st.header("Operations Desk")
    st.markdown('<div class="status-badge"><div class="status-dot"></div>Fulfillment Active</div>', unsafe_allow_html=True)
    st.markdown("---")
    with st.expander("Fulfillment Handbook"):
        if os.path.exists("core_policy.txt"):
            with open("core_policy.txt", "r", encoding="utf-8") as f:
                st.caption(f.read())
        else:
            st.caption("Logistics policy file not found.")

# --- NAVIGATION FLOW: INTEGRATED DROPDOWN SELECTOR ---
user_intent = st.selectbox(
    "Select an issue category to begin execution:",
    [
        "Select your issue category...",
        "Calculate Order Return & Restocking Fee",
        "Track Dispatch Carrier & Delivery Network",
        "Review Store Fulfillment Guidelines",
        "Open Order Support Desk Chat"
    ]
)

st.markdown("<br>", unsafe_allow_html=True)

base_system = (
    "You are SwiftSupport India, an expert customer care agent specializing in retail orders and delivery logistics.\n"
    "Never reference ACME, US shipping, or FedEx. All domestic Indian dispatches go via Delhivery or Blue Dart.\n"
    "Answer queries clearly and professionally using the provided order guidelines."
)

# --- DYNAMIC LAYER CONTENT CARDS ---

# DEFAULT LAYOUT: Dashboard landing block
if user_intent == "Select your issue category...":
    with st.container(border=True):
        st.write("### Welcome to Order Operations")
        st.markdown(
            "Please select an operational category from the menu selection field above to route your request. "
            "The clearing engine automatically processes regional courier routing, product packaging values, "
            "and centralized fulfillment handshakes."
        )

# VIEW 1: Return Processing Calculator
elif user_intent == "Calculate Order Return & Restocking Fee":
    with st.container(border=True):
        st.subheader("Return Processing Calculator")
        st.write("Calculate restocking fee adjustments based on the returned package's condition.")
        
        price = st.number_input("Original Order Value (INR):", min_value=0.0, value=1000.0, step=100.0)
        condition = st.radio("Returned Parcel Packaging Condition:", ["Sealed / Original Condition", "Opened / Damaged Packaging Box"])
        
        if st.button("Process Return Valuation", type="primary"):
            is_damaged = condition == "Opened / Damaged Packaging Box"
            fee = domain_tools.calculate_restocking_fee(price, is_damaged)
            total_refund = price - fee
            
            st.markdown("---")
            c1, c2 = st.columns(2)
            c1.metric("Restocking Fee Deduction", f"₹{fee:,.2f}")
            c2.metric("Net Refund Issued", f"₹{total_refund:,.2f}")

# VIEW 2: Dispatch Carrier Finder
elif user_intent == "Track Dispatch Carrier & Delivery Network":
    with st.container(border=True):
        st.subheader("Dispatch Routing Engine")
        st.write("Look up the designated logistics carrier assigned to transport orders to your target destination.")
        
        dest = st.text_input("Enter Delivery Destination (City or Country):", placeholder="e.g. Mumbai")
        
        if st.button("Route Shipment", type="primary") and dest:
            st.markdown("---")
            if any(city in dest.lower() for city in ["mumbai", "delhi", "bengaluru", "chennai", "india"]):
                st.info("Designated Domestic Courier: **Delhivery Express / Blue Dart Network**")
            else:
                partner = domain_tools.evaluate_shipping_carrier(dest)
                st.info(f"Designated Export Courier: **{partner} Logistics Hub**")

# VIEW 3: Fulfillment Manual Guidelines
elif user_intent == "Review Store Fulfillment Guidelines":
    with st.container(border=True):
        st.subheader("Store Fulfillment Guidelines")
        st.write("Official return processing timelines and courier constraints sourced directly from the shipping database.")
        st.markdown("---")
        policy = knowledge_rag.retrieve_domain_context("return policy window")
        st.info(policy)

# VIEW 4: Help Desk Chat Support
elif user_intent == "Open Order Support Desk Chat":
    with st.container(border=True):
        st.subheader("Order Support Desk")
        st.write("Select a quick-inquiry dispatch chip or submit an order question below:")
        
        # SUGGESTION CHIPS (Sleek minimalist secondary triggers)
        chip_col1, chip_col2, chip_col3 = st.columns(3)
        chosen_suggestion = None
        
        with chip_col1:
            if st.button("⏱️ Return Timeline", type="secondary"):
                chosen_suggestion = "What is the official return policy timeline window?"
        with chip_col2:
            if st.button("📦 Damaged Box Fee", type="secondary"):
                chosen_suggestion = "What is the fee if my product packaging box is missing?"
        with chip_col3:
            if st.button("🚚 Courier Services", type="secondary"):
                chosen_suggestion = "Which domestic courier services do you use inside India?"
                
        st.markdown("---")
        
        if "messages" not in st.session_state:
            st.session_state.messages = []
            
        history_slot = st.container()
        
        with history_slot:
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
                    
        chat_input = st.chat_input("Ask a question about your shipment or order status...")
        active_query = chat_input or chosen_suggestion
        
        if active_query:
            with history_slot:
                with st.chat_message("user"):
                    st.markdown(active_query)
            
            with st.spinner("Accessing fulfillment files..."):
                ctx = knowledge_rag.retrieve_domain_context(active_query)
                sys_prompt = f"{base_system}\n\nPOLICY CONTEXT:\n{ctx}"
                
                try:
                    res = client.chat.completions.create(
                        model=PRIMARY_MODEL,
                        messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": active_query}]
                    )
                    ans = res.choices[0].message.content
                except:
                    res = client.chat.completions.create(
                        model=FALLBACK_MODEL,
                        messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": active_query}]
                    )
                    ans = res.choices[0].message.content
            
            with history_slot:
                with st.chat_message("assistant"):
                    st.markdown(ans)
                    
            st.session_state.messages.append({"role": "user", "content": active_query})
            st.session_state.messages.append({"role": "assistant", "content": ans})
            st.rerun()