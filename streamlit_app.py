import streamlit as st
import os

# Import backend utility modules
import agents_engine
import domain_tools

# --- CONFIGURATION ---
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
        line-height: 1.1 !important;
    }
    
    /* 3. Core Workspace Card Blocks */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: var(--secondary-background-color) !important;
        border: 1px solid rgba(128, 128, 128, 0.15) !important;
        border-radius: 12px !important;
        padding: 24px !important;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02) !important;
    }

    /* 4. High-Contrast Primary Buttons */
    button[kind="primary"] {
        background-color: #2563eb !important;
        color: #ffffff !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        padding: 0.55rem 2rem !important;
        border: none !important;
    }
    button[kind="primary"]:hover {
        background-color: #1d4ed8 !important;
    }
    
    /* 5. Clean Operational Status Elements */
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

    /* =========================================================================
       SWIFTY AI: FLOATING ACTION PILL (Strict Chevron & Boundary Controls)
       ========================================================================= */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
        100% { transform: translateY(0px); }
    }
    @keyframes pulse-glow {
        0% { box-shadow: 0 0 0 0 rgba(37, 99, 235, 0.6); }
        70% { box-shadow: 0 0 0 12px rgba(37, 99, 235, 0); }
        100% { box-shadow: 0 0 0 0 rgba(37, 99, 235, 0); }
    }

    div[data-testid="stPopover"] {
        position: fixed !important;
        bottom: 30px !important;
        right: 30px !important;
        width: auto !important;
        max-width: 260px !important;
        z-index: 999999 !important;
    }
    
    div[data-testid="stPopover"] > button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: #ffffff !important;
        border-radius: 30px !important;
        padding: 12px 24px !important;
        width: auto !important;
        max-width: 260px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        border: none !important;
        font-weight: 600 !important;
        animation: float 3s ease-in-out infinite, pulse-glow 2s infinite;
    }
    div[data-testid="stPopover"] > button:hover {
        transform: scale(1.04) translateY(-1px) !important;
        animation-play-state: paused !important;
    }
    
    /* Aggressively strip away the native down arrow icon */
    div[data-testid="stPopover"] button svg, 
    div[data-testid="stPopover"] button [data-testid="stIcon"] {
        display: none !important;
    }
    
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
        <div style="font-size: 0.95rem; color: rgba(128,128,128,0.8); margin-top: 4px;">Fulfillment, Orders & Dispatch Logistics Hub</div>
    </div>
    """, unsafe_allow_html=True)
st.markdown("---")

# API GATEWAY INITIALIZATION
if "OPENROUTER_API_KEY" in st.secrets:
    api_key = st.secrets["OPENROUTER_API_KEY"]
else:
    st.error("Configuration Error: OPENROUTER_API_KEY is missing from Streamlit Secrets.")
    st.stop()

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

# --- NAVIGATION FLOW: HORIZONTAL TABS ---
tab_dashboard, tab_tools = st.tabs(["Dashboard Overview", "Operational Systems"])

# --- TAB 1: DASHBOARD OVERVIEW ---
with tab_dashboard:
    with st.container(border=True):
        st.write("### Welcome to Order Operations")
        st.markdown(
            "Use the **Operational Systems** tab above to access specialized calculation tools and check courier routing metrics. "
            "For active system assistance or photo triage, launch **Swifty AI** using the floating action pill in the bottom right corner."
        )

# --- TAB 2: OPERATIONAL SYSTEMS (FULLY WIRED) ---
with tab_tools:
    # Component A: Return Processing Calculator
    with st.container(border=True):
        st.subheader("Return Processing Calculator")
        st.write("Calculate restocking fee adjustments based on the returned package's structural condition.")
        
        price = st.number_input("Original Order Value (INR):", min_value=0.0, value=1000.0, step=100.0, key="calc_price_input")
        condition = st.radio("Returned Parcel Packaging Condition:", ["Sealed / Original Condition", "Opened / Damaged Packaging Box"], key="calc_cond_input")
        
        if st.button("Process Return Valuation", type="primary", key="run_valuation_btn"):
            is_damaged = condition == "Opened / Damaged Packaging Box"
            fee = domain_tools.calculate_restocking_fee(price, is_damaged)
            total_refund = price - fee
            
            st.markdown("---")
            c1, c2 = st.columns(2)
            c1.metric("Restocking Fee Deduction", f"₹{fee:,.2f}")
            c2.metric("Net Refund Issued", f"₹{total_refund:,.2f}")

    # Component B: Dispatch Routing Engine
    with st.container(border=True):
        st.subheader("Dispatch Routing Engine")
        st.write("Look up the designated logistics carrier assigned to transport orders to your target destination.")
        
        dest = st.text_input("Enter Delivery Destination (City or Country):", placeholder="e.g. Mumbai", key="router_dest_input")
        
        if st.button("Route Shipment", type="primary", key="run_routing_btn") and dest:
            st.markdown("---")
            if any(city in dest.lower() for city in ["mumbai", "delhi", "bengaluru", "chennai", "india"]):
                st.info("Designated Domestic Courier: **Delhivery Express / Blue Dart Network**")
            else:
                partner = domain_tools.evaluate_shipping_carrier(dest)
                st.info(f"Designated Export Courier: **{partner} Logistics Hub**")

# =========================================================================
# MULTI-MODAL MULTI-AGENT FLOATING WORKSPACE (Swifty AI Popover)
# =========================================================================
with st.popover("🤖 Try Swifty AI for assistance"):
    st.markdown("### 🤖 Swifty AI Agent Network")
    st.caption("Powered by automated text routing and multi-modal vision triage.")
    st.markdown("---")
    
    # Week 2: Multi-Modal File Uploader Integration
    attached_file = st.file_uploader(
        "Attach photo evidence (e.g., damaged boxes, barcodes):", 
        type=["png", "jpg", "jpeg"],
        key="agent_image_uploader"
    )
    
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
        
        # Process queries via our external multi-agent orchestration module
        with st.spinner("Routing query to designated specialist agent..."):
            if attached_file is not None:
                img_bytes = attached_file.read()
                mime_type = attached_file.type
                agent_response = agents_engine.process_agent_workflow(
                    api_key=api_key,
                    user_query=chat_input,
                    uploaded_image_bytes=img_bytes,
                    image_mime_type=mime_type
                )
            else:
                agent_response = agents_engine.process_agent_workflow(
                    api_key=api_key,
                    user_query=chat_input
                )
                
        st.session_state.messages.append({"role": "assistant", "content": agent_response})
        with history_slot:
            with st.chat_message("assistant"):
                st.markdown(agent_response)
        st.rerun()