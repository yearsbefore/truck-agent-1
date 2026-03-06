import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

st.set_page_config(
    page_title="Truck Engineering AI Agent",
    page_icon="🚛",
    layout="wide",
)

if "agent" not in st.session_state:
    from agent.core import create_agent
    st.session_state.agent = create_agent()

# 初始化历史对话会话
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = []
if "current_session_id" not in st.session_state:
    st.session_state.current_session_id = 0
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_input" not in st.session_state:
    st.session_state.pending_input = None


# Sidebar
with st.sidebar:
    st.title("🚛 Truck Engineering Assistant")
    st.markdown("---")

    # 历史对话记录区域
    st.subheader("📜 Chat History")
    
    if st.button("➕ New Chat", use_container_width=True):
        # 保存当前对话
        if st.session_state.messages:
            st.session_state.chat_sessions.append({
                "id": st.session_state.current_session_id,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "preview": st.session_state.messages[0]["content"][:30] + "..." if st.session_state.messages else "Empty",
                "messages": st.session_state.messages.copy()
            })
        
        # 创建新对话
        st.session_state.current_session_id += 1
        st.session_state.messages = []
        if "agent" in st.session_state:
            st.session_state.agent.memory.clear()
        st.rerun()

    # 显示历史对话列表
    if st.session_state.chat_sessions:
        st.markdown("**Previous Conversations:**")
        for i, session in enumerate(reversed(st.session_state.chat_sessions)):
            col1, col2 = st.columns([4, 1])
            with col1:
                if st.button(
                    f"💬 {session['timestamp']}\n{session['preview']}", 
                    key=f"session_{session['id']}",
                    use_container_width=True
                ):
                    # 加载历史对话
                    st.session_state.messages = session["messages"].copy()
                    st.session_state.current_session_id = session["id"]
                    st.rerun()
            with col2:
                if st.button("🗑️", key=f"delete_{session['id']}"):
                    st.session_state.chat_sessions.pop(len(st.session_state.chat_sessions) - 1 - i)
                    st.rerun()
    
    st.markdown("---")

    st.markdown("**Capabilities:**")
    st.markdown("🗄️ **Database Query** — Search truck models, specs, and brands")
    st.markdown("🔧 **CATIA Control** — Open models, modify parameters, export files")
    st.markdown("📋 **Regulation Check** — Verify compliance for EU / US / CN / UK")

    st.markdown("---")
    st.markdown("**Example Questions:**")
    examples = [
        "Find all heavy trucks with payload over 25 tons",
        "What Volvo models are available?",
        "Does this truck comply with EU regulations: length 17m width 2.5m height 3.9m weight 38 tons?",
        "Open the CATIA chassis model",
        "Check all regions: length 18m width 2.55m height 4m weight 45 tons",
    ]
    for ex in examples:
        if st.button(ex, use_container_width=True):
            st.session_state.pending_input = ex

    st.markdown("---")
    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        if "agent" in st.session_state:
            st.session_state.agent.memory.clear()
        st.rerun()


# Main area
st.title("🚛 Truck Engineering AI Agent")
st.caption("Database Query · CATIA Control · Regulation Check")

# 显示对话历史
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 处理输入 - 关键修改：移到最后，确保始终显示
if st.session_state.pending_input:
    user_input = st.session_state.pending_input
    st.session_state.pending_input = None
else:
    user_input = st.chat_input("Enter your request...")  # 这行始终显示输入框

if user_input:
    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 显示助手回复
    with st.chat_message("assistant"):
        with st.spinner("Agent thinking..."):
            try:
                agent = st.session_state.agent
                response = agent.invoke({
                    "input": user_input,
                })
                answer = response.get("output", "Sorry, no response was returned.")

            except Exception as e:
                import traceback
                answer = f"Error: {str(e)}\n\n```\n{traceback.format_exc()}\n```"

        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()  # 重新运行以显示新消息和输入框