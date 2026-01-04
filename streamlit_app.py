import streamlit as st
import urllib.parse

# 页面配置
st.set_page_config(page_title="Hadi 影视特工", page_icon="🎬")

# 标题
st.title("🎬 Hadi 影视私人搜索站")
st.markdown("---")

# 优先级列表
SITES = [
    ("奈飞工厂 (首选)", "https://www.netflixgc.org/vodsearch/-------------.html?wd={q}"),
    ("低端影视 (画质)", "https://ddys.io/"),
    ("爱壹帆 (海外)", "https://www.iyf.tv/list"),
    ("Gimy 剧迷", "https://gimytv.ai/"),
    ("4KVM (磁力)", "https://www.4kvm.org/xssearch?s={q}"),
    ("红牛资源", "https://www.hongniuziyuan.com/")
]

# 搜索框
movie_name = st.text_input("🔍 输入电影或剧集名：", placeholder="例如：黑客帝国")

if movie_name:
    q_encoded = urllib.parse.quote(movie_name)
    st.write(f"### 🎯 搜索：{movie_name}")
    
    # 按照优先级排列按钮
    for name, url_tmpl in SITES:
        target_url = url_tmpl.format(q=q_encoded)
        # 点击按钮直接在新标签页打开
        st.link_button(f"🚀 前往 {name} 搜索", target_url, use_container_width=True)
    
    st.info("💡 提示：按顺序点，第一个没搜到就点第二个。")
