import streamlit as st
import requests
import xml.etree.ElementTree as ET
import google.generativeai as genai
from PIL import Image

# =========================================================================
# 1. HARDCODED FREE API KEY 
# =========================================================================
# CRUCIAL: Replace the text inside the quotes below with your real Gemini key.
# Your working key MUST begin with the letters "AIzaSy".


# Configure the free Google AI library using your key
genai.configure(api_key=GEMINI_API_KEY)

# =========================================================================
# 2. AUTOMATED INDIAN MARKET UPDATES (Free Feed)
# =========================================================================
def fetch_indian_financial_news():
    rss_url = "https://moneycontrol.com"
    try:
        response = requests.get(rss_url)
        root = ET.fromstring(response.content)
        news_text = "INDIAN MARKET & SECTOR UPDATES:\n"
        for item in root.findall('.//item')[:8]:
            title = item.find('title').text
            news_text += f"- {title} (Source: Moneycontrol)\n"
        return news_text
    except:
        return "Market data feed currently refreshing."

# =========================================================================
# 3. USER INTERFACE (Optimized for Mobile Screens)
# =========================================================================
st.set_page_config(page_title="Free Super AI Advisor", layout="wide")
st.title("🧙‍♂️ Free Global AI Financial Advisor")
st.subheader("Powered by Google Gemini Free Tier & Live Whale Tracking")

st.markdown("### Step 1: Provide Your Portfolio")
portfolio_image = st.file_uploader("Upload Portfolio Screenshot (Image)", type=["jpg", "jpeg", "png"])
portfolio_text = st.text_area("Or Paste Tickers Manually", placeholder="Example: 50 shares of Reliance, 10 shares of Tata Motors, 0.5 BTC")

st.markdown("### Step 2: Run Analysis")
st.write("The supercomputer will check Moneycontrol headlines and live whale data automatically.")
analyze_button = st.button("🚀 RUN SUPERCOMPUTER ANALYSIS", use_container_width=True)

# =========================================================================
# 4. ONE-CLICK ADVISORY PIPELINE
# =========================================================================
if analyze_button:
    if not portfolio_image and not portfolio_text:
        st.error("Please provide your portfolio via image upload or text input first!")
    else:
        with st.spinner("Crunching data like a financial supercomputer..."):
            
            live_market_news = fetch_indian_financial_news()
            
            master_prompt = f"""
            You are the central engine of a hyper-advanced, global AI financial advisor app. 
            Your task is to process the user's data, present 3 custom portfolio models, select the absolute best model for this moment, and run a supercomputer-level analysis.

            [LIVE AUTOMATED MARKET SCENARIO]:
            {live_market_news}

            [USER PORTFOLIO DATA]:
            {portfolio_text if portfolio_text else "User uploaded an image. Look at the attached image for holdings and tickers."}

            Follow this strict output layout:

            # 🌟 ULTIMATE VERDICT & THE BEST PORTFOLIO FOR YOU
            Evaluate the user's asset mix against the live data. Present 3 custom-tailored portfolio models:
            1. "The Weatherproof Whale" (Ray Dalio & Warren Buffett style)
            2. "The Aggressive Sector Rotator" (Stanley Druckenmiller style)
            3. "The Asymmetric Black Swan" (Michael Burry style)
            
            Explicitly declare which one of these three models is the absolute BEST choice for the current exact market scenario and explain the exact structural reason why.

            # 📉 GLOBAL MACRO & MARKET CRASH RISK ASSESSER
            - Give an explicit Market Crash Risk Score from 1 to 10.
            - Name 3 specific macroeconomic triggers that could cause a massive market bubble pop right now.

            # 👑 WHALE TRACKING & HISTORICAL PARALLELS
            - Outline what the 5 market kings are doing or historically do in this specific setup: 1) Warren Buffett, 2) Michael Burry, 3) Ray Dalio, 4) Stanley Druckenmiller, 5) Nancy Pelosi.
            - Tie today's context to a specific historical market era (e.g., 2000 tech crash, 2008 crash, 1970s stagflation). What happened next then?

            # 🔄 PRO SECTOR ROTATION MATRIX
            - Review the major stock market sectors. Identify which are overbought/dangerous and which are undervalued/accumulating.
            - Provide an exact roadmap: Which sectors to exit/trim and which sectors to rotate capital into.

            # 🛠️ YOUR PORTFOLIO TECHNICAL & FINANCIAL CRITIQUE
            - Give a deep fundamental assessment of the user's current holdings (Valuation traps, risks).
            - Highlight any immediate technical vulnerabilities (overconcentration, momentum traps).

            # 📋 STEP-BY-STEP ACTION BLUEPRINT
            - Provide a detailed, explicit list of actions to transition the user's current portfolio smoothly into the recommended "BEST" model.

            Be brutally honest, deeply quantitative, analytical, and back up every single claim with explicit logical or institutional reasons. Provide rigorous educational logic.
            """

            try:
                # Fire up the completely free Gemini model
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                if portfolio_image:
                    img = Image.open(portfolio_image)
                    response = model.generate_content([master_prompt, img])
                else:
                    response = model.generate_content(master_prompt)
                
                st.success("Analysis Complete!")
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Execution Error: {str(e)}")
