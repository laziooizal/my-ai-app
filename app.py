import streamlit as st
from openai import OpenAI
import anthropic
import concurrent.futures

st.set_page_config(page_title="AI 聯合問答助手", page_icon="🤖", layout="wide")
st.title("🤖 AI 聯合問答助手")
st.markdown("輸入一個問題，同時獲取多個 AI 模型的回答！")

st.sidebar.header("🔑 設定 API 金鑰")
openai_key = st.sidebar.text_input("OpenAI (ChatGPT) API Key", type="password")
claude_key = st.sidebar.text_input("Anthropic (Claude) API Key", type="password")
deepseek_key = st.sidebar.text_input("DeepSeek API Key", type="password")
grok_key = st.sidebar.text_input("xAI (Grok) API Key", type="password")

def get_chatgpt_response(prompt, key):
    if not key: return "⚠️ 未提供 API Key，跳過此模型。"
    try:
        client = OpenAI(api_key=key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ 發生錯誤：{str(e)}"

def get_claude_response(prompt, key):
    if not key: return "⚠️ 未提供 API Key，跳過此模型。"
    try:
        client = anthropic.Anthropic(api_key=key)
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        return f"❌ 發生錯誤：{str(e)}"

def get_deepseek_response(prompt, key):
    if not key: return "⚠️ 未提供 API Key，跳過此模型。"
    try:
        client = OpenAI(api_key=key, base_url="https://api.deepseek.com")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ 發生錯誤：{str(e)}"

def get_grok_response(prompt, key):
    if not key: return "⚠️ 未提供 API Key，跳過此模型。"
    try:
        client = OpenAI(api_key=key, base_url="https://api.x.ai/v1")
        response = client.chat.completions.create(
            model="grok-beta",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ 發生錯誤：{str(e)}"

user_question = st.chat_input("請輸入你想問所有 AI 的問題...")

if user_question:
    st.markdown(f"**🗣️ 你的問題：** {user_question}")
    st.markdown("---")
    
    with st.spinner("各路 AI 正在思考中，請稍候..."):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_gpt = executor.submit(get_chatgpt_response, user_question, openai_key)
            future_claude = executor.submit(get_claude_response, user_question, claude_key)
            future_deepseek = executor.submit(get_deepseek_response, user_question, deepseek_key)
            future_grok = executor.submit(get_grok_response, user_question, grok_key)
            
            ans_gpt = future_gpt.result()
            ans_claude = future_claude.result()
            ans_deepseek = future_deepseek.result()
            ans_grok = future_grok.result()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🟢 ChatGPT")
        st.info(ans_gpt)
        st.subheader("🔵 DeepSeek")
        st.info(ans_deepseek)
    with col2:
        st.subheader("🟠 Claude")
        st.success(ans_claude)
        st.subheader("⚫ Grok")
        st.success(ans_grok)
