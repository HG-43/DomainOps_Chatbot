import os
# High-priority patch to bypass the Streamlit Cloud Protobuf compatibility bug
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import streamlit as st
import random

# Import backend utility modules
import agents_engine
import domain_tools

# --- CONFIGURATION ---
st.set_page_config(page_title="SwiftSupport India", layout="centered")

# NATURAL, GROUNDED ASSISTANT PHRASES
OPERATIONAL_SPINNERS = [
    "Swifty is thinking...",
    "Looking into the details for you...",
    "Checking the latest updates...",
    "Reviewing your request...",
    "Searching for the best answer..."
]

st.markdown("""
    <style>
    /* 1. Structural Canvas Polishing */
    div[data-testid="stAppDeployButton"] { display: none !important; }
    footer { visibility: hidden; }
    
    .portal-header {
        border-left: 5px solid #2563eb;
        padding-left: 16px;
        margin-bottom: 24px;
        margin-top: 10px;
    }
    .portal-title {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.04em !important;
        margin: 0 !important;
        line-height: 1.1 !important;
    }
    
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: var(--secondary-background-color) !important;
        border: 1px solid rgba(128, 128, 128, 0.15) !important;
        border-radius: 12px !important;
        padding: 24px !important;
        margin-bottom: 24px;
    }

    button[kind="primary"] {
        background-color: #2563eb !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.55rem 2rem !important;
        border: none !important;
    }
    button[kind="primary"]:hover { background-color: #1d4ed8 !important; }

    /* SWIFTY AI: FLOATING ACTION PILL */
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

    div[data-testid="stPopover"] {
        position: fixed !important;
        bottom: 30px !important;
        right: 30px !important;
        width: auto !important;
        z-index: 999999 !important;
    }
    
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
        animation: float-loop 3s ease-in-out infinite, pulse-ring 2s infinite;
    }
    
    div[data-testid="stPopover"] button svg, 
    div[data-testid="stPopover"] button [data-testid="stIcon"] {
        display: none !important;
    }
    
    div[data-testid="stPopoverWindow"] {
        width: 400px !important;
        border-radius: 16px !important;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.25) !important;
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

if "OPENROUTER_API_KEY" in st.secrets:
    api_key = st.secrets["OPENROUTER_API_KEY"]
else:
    st.error("Missing API Key configuration secrets.")
    st.stop()

# --- SIDEBAR PANEL ---
with st.sidebar:
    st.header("Operations Desk")
    st.success("Fulfillment Core Active")
    st.markdown("---")
    with st.expander("Fulfillment Handbook"):
        if os.path.exists("core_policy.txt"):
            with open("core_policy.txt", "r", encoding="utf-8") as f:
                st.caption(f.read())

# --- NAVIGATION FLOW: TABS INTERFACE ---
tab_dashboard, tab_tools = st.tabs(["Dashboard Overview", "Operational Systems"])

# TAB 1: DASHBOARD OVERVIEW
with tab_dashboard:
    with st.container(border=True):
        st.write("### Welcome to Order Operations")
        st.markdown(
            "Use the **Operational Systems** tab above to access real-time database lookups and tool computation logic sheets. "
            "For automated case escalations or photo verification triage, launch the **Swifty AI** assistant pill floating in the bottom corner."
        )

# TAB 2: OPERATIONAL SYSTEMS
with tab_tools:
    
    # 1. LIVE LEDGER DISPATCH FINDER (Optimized Card Overhaul)
    with st.container(border=True):
        st.subheader("🗄️ Real-Time Manifest Ledger Search")
        st.write("Query the live operational database directly using tracking IDs to pull courier metrics.")
        
        search_id = st.text_input("Enter Active Tracking ID:", value="SWIFT-BLR-5601", placeholder="e.g. SWIFT-BOM-4002")
        
        if st.button("Query Database Ledger", type="primary"):
            record = domain_tools.lookup_mock_order(search_id)
            st.markdown("---")
            if record:
                # Premium HTML injection cards that are fully immune to horizontal text-wrapping breaks
                status_color = "#eab308" if "Delay" in record["status"] else ("#ef4444" if "Exception" in record["status"] else "#10b981")
                bg_badge = "rgba(234, 179, 8, 0.1)" if "Delay" in record["status"] else ("rgba(239, 68, 68, 0.1)" if "Exception" in record["status"] else "rgba(16, 185, 129, 0.1)")
                
                st.markdown(f"""
                    <div style="background-color: var(--background-color); padding: 18px; border: 1px solid rgba(128,128,128,0.2); border-radius: 10px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                            <span style="font-size: 0.8rem; font-weight: 700; color: #64748b; letter-spacing: 0.05em; text-transform: uppercase;">Manifest Activity Record</span>
                            <span style="background-color: {bg_badge}; color: {status_color}; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700;">{record['status']}</span>
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 16px;">
                            <div>
                                <div style="font-size: 0.75rem; color: #64748b; font-weight: 600; margin-bottom: 2px;">Destination Hub</div>
                                <div style="font-size: 1.1rem; font-weight: 700;">{record['destination']}</div>
                            </div>
                            <div>
                                <div style="font-size: 0.75rem; color: #64748b; font-weight: 600; margin-bottom: 2px;">Assigned Courier</div>
                                <div style="font-size: 1.1rem; font-weight: 700;">{record['carrier']}</div>
                            </div>
                        </div>
                        <div style="background-color: rgba(37, 99, 235, 0.05); border-left: 3px solid #2563eb; padding: 12px; border-radius: 4px;">
                            <div style="font-size: 0.75rem; color: #2563eb; font-weight: 700; margin-bottom: 4px;">Live Telemetry Details</div>
                            <div style="font-size: 0.9rem; line-height: 1.45;">{record['details']}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.error("❌ Tracking ID anomaly: Record missing or archived in central cluster vaults.")

    # 2. Return Processing Calculator
    with st.container(border=True):
        st.subheader("🧮 Return Processing Calculator")
        price = st.number_input("Original Order Value (INR):", min_value=0.0, value=1000.0, step=100.0)
        condition = st.radio("Returned Parcel Packaging Condition:", ["Sealed / Original Condition", "Opened / Damaged Packaging Box"])
        
        if st.button("Process Return Valuation"):
            is_damaged = condition == "Opened / Damaged Packaging Box"
            fee = domain_tools.calculate_restocking_fee(price, is_damaged)
            st.markdown("---")
            c1, c2 = st.columns(2)
            c1.metric("Restocking Fee Deduction", f"₹{fee:,.2f}")
            c2.metric("Net Refund Issued", f"₹{price - fee:,.2f}")

# =========================================================================
# FLOATING ASSISTANT WORKSPACE WIDGET (Swifty AI Popover Drawer)
# =========================================================================
with st.popover("🤖 Try Swifty AI"):
    st.markdown("### 🤖 Swifty AI Agent Network")
    st.caption("Fulfillment intelligence with dynamic automated routing keys.")
    st.markdown("---")
    
    attached_img = st.file_uploader("📸 Upload Claims Photo Evidence:", type=["png", "jpg", "jpeg"])
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
        
        chosen_spinner = random.choice(OPERATIONAL_SPINNERS)
        
        with st.spinner(chosen_spinner):
            agent_response = agents_engine.process_agent_workflow(
                api_key=api_key,
                user_query=chat_input,
                uploaded_image_file=attached_img
            )
                
        st.session_state.messages.append({"role": "assistant", "content": agent_response})
        with history_slot:
            with st.chat_message("assistant"):
                st.markdown(agent_response)
        st.rerun()