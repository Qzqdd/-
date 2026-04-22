# AI个性化学习助手 最终稳定版 零报错
import streamlit as st
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# 1. 页面全局基础配置
st.set_page_config(page_title="AI个性化学习助手", layout="wide")
st.title("🧠 AI个性化学习助手")

# 2. 加载AI密钥配置
load_dotenv()
api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")
model_name = os.getenv("MODEL_NAME")

# 3. 初始化AI大模型
llm = ChatOpenAI(
    api_key=api_key,
    base_url=base_url,
    model=model_name,
    temperature=0.7
)

# 4. 侧边栏功能菜单
menu = st.sidebar.radio(
    "功能导航栏",
    ["知识点智能整理", "专属学习计划生成", "错题智能分析", "关于项目"]
)

# ---------------- 功能1：知识点整理 ----------------
if menu == "知识点智能整理":
    st.subheader("📚 一键梳理知识点、提炼重难点")
    user_content = st.text_area("粘贴你的课本、笔记、课件内容：", height=200)
    if st.button("✨ AI一键智能整理") and user_content:
        with st.spinner("AI正在深度梳理知识框架，请稍等..."):
            prompt = f"""
帮我对下面这段学习内容，做专业的知识点整理：
1. 提炼核心重点
2. 搭建清晰知识框架
3. 标注易错、易混淆难点
4. 给出记忆学习建议
待整理内容：
{user_content}
            """
            result = llm.invoke([HumanMessage(content=prompt)])
        st.markdown("### ✅ AI整理完成")
        st.write(result.content)

# ---------------- 功能2：生成学习计划 ----------------
elif menu == "专属学习计划生成":
    st.subheader("📅 为你定制专属个性化学习计划")
    goal = st.text_input("你的最终学习目标是什么？")
    daily_time = st.number_input("每天可以投入学习的时长（分钟）", min_value=15, max_value=300, value=60)
    level = st.selectbox("你目前的基础水平", ["零基础小白", "入门刚接触", "有一定基础", "进阶提升"])

    if st.button("🚀 生成专属计划") and goal:
        with st.spinner("AI正在量身打造学习方案..."):
            plan_prompt = f"""
用户信息：
学习目标：{goal}
每日可用学习时间：{daily_time}分钟
当前基础水平：{level}
请为用户制定一份科学合理、可落地的分阶段7天学习计划，安排每日学习任务、练习安排、复盘节点。
            """
            plan_res = llm.invoke([HumanMessage(content=plan_prompt)])
        st.markdown("### 📋 你的专属7天学习计划")
        st.write(plan_res.content)

# ---------------- 功能3：错题分析 ----------------
elif menu == "错题智能分析":
    st.subheader("✍️ 错题整理、错因解析、举一反三")
    wrong_title = st.text_input("请输入错题的题目：")
    wrong_answer = st.text_area("写下你之前的错误解法/答案：")

    if st.button("🔍 AI深度解析错题") and wrong_title:
        with st.spinner("AI正在拆解题目、分析错因..."):
            wrong_prompt = f"""
题目：{wrong_title}
我的错误解法：{wrong_answer}
请帮我：
1. 分析核心错误原因
2. 给出标准、清晰的正确解题步骤
3. 点明本题考察的知识点
4. 提供2-3道同类型巩固练习题，避免下次再错
            """
            wrong_res = llm.invoke([HumanMessage(content=wrong_prompt)])
        st.markdown("### ✅ 错题完整解析报告")
        st.write(wrong_res.content)

st.sidebar.info("💡 配置好.env里的API Key，即可解锁全部AI智能功能")