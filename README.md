# 🦾 AI Personal Fitness Coach Agent

**Author:** Justin Bryden Arroco  
**Course:** ANLYTC04 Finals  

## 📌 Project Overview
The AI Personal Fitness Coach is an intelligent, agentic web application designed to provide personalized workout routines, form corrections, and targeted exercise recommendations. By leveraging a locally hosted Large Language Model (LLM), the system ensures zero cloud inference costs, total data privacy, and uncapped usage.

## 🏗️ System Architecture
While many agentic systems rely on heavy frameworks like LangChain or CrewAI, this project implements a **custom, lightweight ReAct (Reasoning + Acting) loop** directly in Python. 

The architecture consists of three main components:
1. **The Engine (Local LLM):** Powered by Llama 3 (8B) running locally via LM Studio. This acts as the reasoning brain of the agent.
2. **The Interface (Streamlit):** A dynamic, night-themed frontend that maintains session state, handles user inputs, and renders visual anatomy diagrams conditionally.
3. **The Tool Dispatcher:** A custom-built Python routing system. When the LLM determines it needs external data, it outputs a hidden trigger tag (e.g., `[FETCH: chest]`). The backend intercepts this, pauses the LLM, queries the **API Ninjas Exercise Database**, and dynamically injects the verified data and visual assets back into the LLM's context window for a seamless user response.

## 🛠️ Libraries & Technologies Used
* **`streamlit`**: For building the interactive web interface and managing session state memory.
* **`openai`**: The official Python client, re-routed to interface with the local LM Studio server instead of OpenAI's cloud servers.
* **`requests`**: For executing HTTP GET requests to the external API Ninjas database.
* **`python-dotenv`**: For securely managing local environment variables and API keys.

## 🚀 Setup & Installation Instructions

### 1. Prerequisites
* Python 3.10+
* LM Studio installed locally.
* An API key from API Ninjas.

### 2. Environment Setup
Create a virtual environment and install the required dependencies:
    
    python -m venv venv
    .\venv\Scripts\activate
    pip install streamlit openai requests python-dotenv

### 3. Configuration
Create a `.env` file in the root directory and add your API key:
    
    API_NINJAS_KEY=your_api_key_here

### 4. Launch the Local AI Server
1. Open LM Studio.
2. Load the `Llama-3-8B-Instruct` model.
3. Go to the Local Server tab and click **Start Server** (Ensure it runs on `http://localhost:1234/v1`).

### 5. Run the Application
With the virtual environment active and LM Studio running, launch the frontend:
    
    streamlit run app.py