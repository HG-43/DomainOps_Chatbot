import streamlit as st
import os

# Import backend utility modules
import agents_engine
import domain_tools

# --- CONFIGURATION ---
st.set_page_config(page_title="SwiftSupport India", layout="centered")

st.markdown("""
    <style>
    /* 1. Structural Element Resets */
    div[data-testid="stAppDeployButton"] { display: none !important; }
    footer { visibility: hidden; }
    
    /* 2. Premium Title Bar Accents */
    .portal-header {
        border-left: 5px solid #2563eb;
        padding-left: 16px;
        margin-bottom: 24px;
        margin-top: 10px;
    }
    .portal-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        margin: 0;
        line-height: 1.1;
    }
    
    /* 3. High-Contrast Container Workspace Blocks */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: var(--secondary-background-color) !important;
        border: 1px solid rgba(128, 128, 128, 0.15) !important;
        border-radius: 12px !important;
        padding: 24px !important;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02) !important;
    }

    /* 4. Form Action Buttons */
    button[kind="primary"] {
        background-color: #2563eb !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.55rem 2rem !important;
        border: none !important;
    }
    button[kind="primary"]:hover {
        background-color: #1d4ed8 !important;
    }

    /* =========================================================================
       SWIFTY AI: SINGLE STANDALONE FLOATING ACTION PILL (Strict Geometries)
       ========================================================================= */
    @keyframes float-loop {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-6px); }
        100% { transform: translateY(0px); }
    }
    @keyframes pulse-ring {
        0% { box-shadow: 0 0 0 0 rgba(37, 99, 235, 0.5); }
        70% { box-shadow: 0 0 0 12px rgba(37, 99, 235, 0); }
        100% { box-shadow: 0 0 0 0 rgba(37, 99, 235, 0); }
    }

    /* Fixed alignment limits to block any item stacking */
    div[data-testid="stPopover"] {
        position: fixed !important;
        bottom: 30px !important;
        right: 30px !important;
        width: auto !important;
        z-index: 999999 !important;
    }
    
    /* Formats the popover trigger window into a clean interactive pill */
    div[data-testid="stPopover"] > button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: #ffffff !important;
        border-radius: 30px !important;
        padding: 12px 24px !important;
        height: 46px !important;
        width: auto !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        border: none !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        
        /* Smooth runtime animation tracking */
        animation: float-loop 3s ease-in-out infinite, pulse-ring 2s infinite;
    }
    div[data-testid="stPopover"] > button:hover {
        transform: scale(1.03) translateY(-1px) !important;
        animation-play-state: paused !important;
    }
    
    /* Safely completely remove the caret drop arrow icon to protect width */
    div[data-testid="stPopover"] button svg, 
    div[data-testid="stPopover"] button [data-testid="stIcon"] {
        display: none !important;
    }
    
    /* Chat popup overlay frame dimensions */
    div[data-testid="stPopoverWindow"] {
        width: 385px !important;
        border-radius: 16px !important;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- PORTAL HEADER HERO BLOCK ---
st.markdown("""
    <div class="portal-header">
        <h1 class="portal-title">SwiftSupport India</h1>
        <div style="font-size: 0.95rem; color: #64748b; margin-top: 4px; font-weight: 500;">Fulfillment, Orders & Dispatch Logistics Hub</div>
    </div>
    """, unsafe_allow_html=True)
st.markdown("---")

# API GATEWAY INITIALIZATION
if "OPENROUTER_API_KEY" in st.secrets:
    api_key = st.secrets["OPENROUTER_API_KEY"]
else:
    st.error("Configuration Error: OPENROUTER_API_KEY is missing from Streamlit Secrets.")
    st.stop()

# --- SIDEBAR PANEL (Fonts Cleaned to Fix Icon Overlaps) ---
with st.sidebar:
    st.header("Operations Desk")
    st.success("Fulfillment Active")
    st.markdown("---")
    with st.expander("Fulfillment Handbook"):
        if os.path.exists("core_policy.txt"):
            with open("core_policy.txt", "r", encoding="utf-8") as f:
                st.caption(f.read())
        else:
            st.caption("Logistics policy file not found.")

# --- NAVIGATION FLOW: TABS INTERFACE ---
tab_dashboard, tab_tools = st.tabs(["Dashboard Overview", "Operational Systems"])

# --- TAB 1: DASHBOARD OVERVIEW ---
with tab_dashboard:
    with st.container(border=True):
        st.write("### Welcome to Order Operations")
        st.markdown(
            "Use the **Operational Systems** tab above to access calculation tools and check courier network options. "
            "For advanced automated queries, voice transcriptions, or visual evidence triage, open the integrated assistant "
            "via the floating action pill in the bottom corner."
        )

# --- TAB 2: OPERATIONAL SYSTEMS ---
with tab_tools:
    # Tool Node A: Return Processing Calculator
    with st.container(border=True):
        st.subheader("Return Processing Calculator")
        st.write("Calculate restocking fee adjustments based on the returned package's structural condition.")
        
        price = st.number_input("Original Order Value (INR):", min_value=0.0, value=1000.0, step=100.0, key="sys_price_field")
        condition = st.radio("Returned Parcel Packaging Condition:", ["Sealed / Original Condition", "Opened / Damaged Packaging Box"], key="sys_cond_field")
        
        if st.button("Process Return Valuation", type="primary", key="sys_val_trigger"):
            is_damaged = condition == "Opened / Damaged Packaging Box"
            fee = domain_tools.calculate_restocking_fee(price, is_damaged)
            total_refund = price - fee
            
            st.markdown("---")
            c1, c2 = st.columns(2)
            c1.metric("Restocking Fee Deduction", f"₹{fee:,.2f}")
            c2.metric("Net Refund Issued", f"₹{total_refund:,.2f}")

    # Tool Node B: Dispatch Routing Engine
    with st.container(border=True):
        st.subheader("Dispatch Routing Engine")
        st.write("Look up the designated logistics carrier assigned to transport orders to your target destination.")
        
        dest = st.text_input("Enter Delivery Destination (City or Country):", placeholder="e.g. Mumbai", key="sys_dest_field")
        
        if st.button("Route Shipment", type="primary", key="sys_route_trigger") and dest:
            st.markdown("---")
            if any(city in dest.lower() for city in ["mumbai", "delhi", "bengaluru", "chennai", "india"]):
                st.info("Designated Domestic Courier: **Delhivery Express / Blue Dart Network**")
            else:
                partner = domain_tools.evaluate_shipping_carrier(dest)
                st.info(f"Designated Export Courier: **{partner} Logistics Hub**")

# =========================================================================
# STANDALONE FLOATING ASSISTANT WIDGET (Single, Contained Popover Pill)
# =========================================================================
with st.popover("🤖 Try Swifty AI"):
    st.markdown("### 🤖 Swifty AI Agent Network")
    st.caption("Voice, Vision, and Autonomous Multimodal Intelligence Hub")
    st.markdown("---")
    
    # Multimodal File Input Fields
    col_img, col_aud = st.columns(2)
    with col_img:
        attached_img = st.file_uploader("📸 Photo Triage", type=["png", "jpg", "jpeg"])
    with col_aud:
        attached_aud = st.file_uploader("🎙️ Voice Memo", type=["mp3", "wav", "m4a"])
    
    st.markdown("---")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    history_slot = st.container()
    
    with history_slot:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
    chat_input = st.chat_input("Ask a logistics or financial query...")
    
    if chat_input:
        st.session_state.messages.append({"role": "user", "content": chat_input})
        with history_slot:
            with st.chat_message("user"):
                st.markdown(chat_input)
        
        with st.spinner("Swifty Agents are analyzing inputs..."):
            agent_response = agents_engine.process_agent_workflow(
                api_key=api_key,
                user_query=chat_input,
                uploaded_image=attached_img,
                uploaded_audio=attached_aud
            )
                
        st.session_state.messages.append({"role": "assistant", "content": agent_response})
        with history_slot:
            with st.chat_message("assistant"):
                st.markdown(agent_response)
        st.rerun()