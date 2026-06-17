import streamlit as st
import requests
import xml.etree.ElementTree as ET
from anthropic import Anthropic
import base64

# Load secret keys securely from the cloud app settings
try:
    ANTHROPIC_API_KEY = st.secrets["YOUR_ANTHROPIC_KEY"]
    NEWS_API_KEY = st.secrets["YOUR_NEWS_API_KEY"]
except:
    st.error("Missing API Keys! Please add them to your Streamlit Advanced Secrets Settings.")
    st.stop()

client = Anthropic(api_key=ANTHROPIC_API_KEY)

def fetch_global_financial_news():
    url = f"https://newsapi.org{NEWS_API_KEY}"
    try:
        response = requests.get(url).json()
        articles = response.get("articles", [])[:5]
        news_text = "GLOBAL MARKET UPDATES:\n"
        for art in articles:
            news_text += f"- {art['title']} (Source: {art['source']['name']})\n"
        return news_text
    except:
        return "Global News Fetching Error."

def fetch_indian_financial_news():
    rss_url = "https://moneycontrol.com"
    try:
        response = requests.get(rss_url)
        root = ET.fromstring(response.content)
        news_text = "INDIAN MARKET UPDATES:\n"
        for item in root.findall('.//item')[:5]:
            title = item.find('title').text
            news_text += f"- {title} (Source: Moneycontrol)\n"
        return news_text
    except:
        return "Indian News Fetching Error."

def encode_image_to_base64(uploaded_file):
    return base64.b64encode(uploaded_file.read()).decode("utf-8")

st.set_page_config(page_title="Super AI Financial Advisor", layout="wide")
st.title("🧙‍♂️ Global AI Financial Advisor")
st.subheader("Powered by Claude 3.5 Sonnet, Live News Feeds & Whale Tracking")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Step 1: Upload Portfolio")
    portfolio_image = st.file_uploader("Upload Portfolio Screenshot (Image)", type=["jpg", "jpeg", "png"])
    portfolio_text = st.text_area("Or Paste Tickers/Text Manually", placeholder="Example: 50 shares of Reliance, 10 shares of AAPL, 0.5 BTC")

with col2:
    st.markdown("### Step 2: Live Market Context")
    st.write("Clicking analyze will automatically grab real-time news from Bloomberg, Reuters, Moneycontrol, and Wall Street Insights.")
    analyze_button = st.button("🚀 RUN SUPERCOMPUTER ANALYSIS", use_container_width=True)

if analyze_button:
    if not portfolio_image and not portfolio_text:
        st.error("Please provide your portfolio via image upload or text input first!")
    else:
        with st.spinner("Fetching live global data, tracking market kings, and crunching math..."):
            global_news = fetch_global_financial_news()
            indian_news = fetch_indian_financial_news()
            live_news_payload = f"{global_news}\n\n{indian_news}"
            
            master_prompt = f"""
            You are the central engine of a hyper-advanced, global AI financial advisor app. 
            Your task is to process the user's data, present 3 custom portfolio models, select the absolute best model for this moment, and run a supercomputer-level analysis.

            [LIVE AUTOMATED NEWS & MARKET ENVIRONMENT]:
            {live_news_payload}

            [USER MANUALLY PROVIDED PORTFOLIO DATA]:
            {portfolio_text if portfolio_text else "User uploaded an image instead. Look at the attached image for holdings."}

            Follow this strict output layout:

            # 🌟 ULTIMATE VERDICT & THE BEST PORTFOLIO FOR YOU
            Evaluate the user's asset mix against the live global/Indian news and macro data. Present 3 custom-tailored portfolio models:
            1. "The Weatherproof Whale" (Ray Dalio & Warren Buffett style)
            2. "The Aggressive Sector Rotator" (Stanley Druckenmiller style)
            3. "The Asymmetric Black Swan" (Michael Burry style)
            
            Explicitly declare which one of these three models is the absolute BEST choice for the current exact market scenario and explain the exact structural reason why.

            # 📉 GLOBAL MACRO & MARKET CRASH RISK ASSESSER
            - Give an explicit Market Crash Risk Score from 1 to 10.
            - Name 3 specific macroeconomic triggers that could cause a massive market bubble pop right now.

            # 👑 WHALE TRACKING & HISTORICAL PARALLELS
            - Outline what the 5 market kings are doing or historically do in this specific setup: 1) Warren Buffett, 2) Michael Burry, 3) Ray Dalio, 4) Stanley Druckenmiller, 5) Nancy Pelosi.
            - Tie today's context to a specific historical market era (e.g., 2000 tech crash, 2008 crash, 1970s stagflation). What happened next then, and what must the user learn from it?

            # 🔄 PRO SECTOR ROTATION MATRIX
            - Review the 11 stock market sectors. Identify which are overbought/dangerous and which are undervalued/accumulating.
            - Provide an exact roadmap: Which sectors to exit/trim and which sectors to rotate capital into.

            # 🛠️ YOUR PORTFOLIO TECHNICAL & FINANCIAL CRITIQUE
            - Give a deep fundamental assessment of the user's current holdings (Debt risks, valuation traps, cash flows).
            - Highlight any immediate technical vulnerabilities (overconcentration, momentum-chasing traps).

            # 📋 STEP-BY-STEP ACTION BLUEPRINT
            - Provide a detailed, explicit list of actions to transition the user's current portfolio smoothly into the recommended "BEST" model.

            Be brutally honest, deeply quantitative, analytical, and back up every single claim with explicit logical or institutional reasons.
            """

            message_content = []
            if portfolio_image:
                base64_image = encode_image_to_base64(portfolio_image)
                img_type = portfolio_image.type if portfolio_image.type in ["image/jpeg", "image/png", "image/gif", "image/webp"] else "image/jpeg"
                message_content.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": img_type,
                        "data": base64_image
                    }
                })
            
            message_content.append({
                "type": "text",
                "text": master_prompt
            })

            try:
                response = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=4000,
                    messages=[{"role": "user", "content": message_content}]
                )
                st.success("Analysis Complete!")
                st.markdown("---")
                st.markdown(response.content[0].text)
            except Exception as e:
                st.error(f"API Connection Error: {str(e)}")
