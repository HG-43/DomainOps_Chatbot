# SwiftSupport India 🧡

**SwiftSupport India** is a high-performance, AI-driven customer service portal designed for a modern retail environment. It leverages a Retrieval-Augmented Generation (RAG) architecture to provide accurate, policy-grounded support for orders, returns, and regional logistics within India.

---

## 🚀 Core Features

*   **Policy-Grounded Chat:** Uses RAG to answer questions based strictly on official store manuals.
*   **Intelligent Fee Calculation:** Automatically computes restocking fees for returns based on packaging condition and item price.
*   **Regional Logistics Routing:** Dynamically identifies shipping carriers (Delhivery, Blue Dart) for domestic Indian cities.
*   **Intent-Driven UI:** Features a guided menu system for immediate, error-free user routing.
*   **Secure Architecture:** Includes multi-stage guardrails to prevent technical data leaks or malicious prompt injection.

---

## 🛠️ Technical Stack

*   **Frontend:** Streamlit (Clean, Minimalist Corporate UI)
*   **LLM Engine:** Meta-Llama 3.3-70B (via OpenRouter)
*   **Logic:** Python 3.x
*   **Security:** Multi-layer input/output guardrails and secure secret management.

---

## 📦 Installation & Local Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/SwiftSupport-India.git](https://github.com/YOUR_USERNAME/SwiftSupport-India.git)
cd SwiftSupport-India