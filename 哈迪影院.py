import os
import webbrowser
import urllib.parse
from playwright.sync_api import sync_playwright

# 优先级排序的站点配置
SITES = [
    {"name": "奈飞工厂", "url": "https://www.netflixgc.org/vodsearch/-------------.html?wd={q}", "keyword": "播放"},
    {"name": "低端影视", "url": "https://ddys.io/?s={q}", "keyword": "站内搜索"}, # ddys 比较特殊，先检测搜索页
    {"name": "爱壹帆", "url": "https://www.iyf.tv/search/{q}", "keyword": "视频"},
    {"name": "Gimy 剧迷", "url": "https://gimytv.ai/search/-------------.html?wd={q}", "keyword": "立即播放"},
    {"name": "4KVM", "url": "https://www.4kvm.org/xssearch?s={q}", "keyword": "movies"}
]

def auto_scout(movie_name):
    q_encoded = urllib.parse.quote(movie_name)
    
    print(f"\n[任务] 🕵️ 开始全网轮询搜索: {movie_name}")
    print("="*50)
    
    with sync_playwright() as p:
        # 启动后台浏览器
        browser = p.chromium.launch(headless=True) 
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        page = context.new_page()
        
        found = False
        for site in SITES:
            target_url = site["url"].format(q=q_encoded)
            print(f"🔍 正在侦察: {site['name']}...")
            
            try:
                # 访问搜索结果页
                page.goto(target_url, timeout=15000)
                page.wait_for_timeout(2000) # 给 2 秒加载时间
                
                # 检查页面是否有资源特征 (比如出现了电影链接或播放按钮)
                # 我们通过检查页面文字来粗略判断
                content = page.content()
                
                # 如果页面出现了电影名，或者我们定义的关键词
                if movie_name in content or site["keyword"] in content:
                    print(f"✨ 发现目标！{site['name']} 疑似有资源！")
                    print(f"🚀 正在为你直达播放页面...")
                    webbrowser.open(target_url)
                    found = True
                    break # 搜到了就立刻停，不去骚扰后面的网站
                else:
                    print(f"❌ {site['name']} 未发现有效资源，跳过...")
            
            except Exception as e:
                print(f"⚠️ {site['name']} 访问超时或出错，尝试下一个...")
                continue
        
        browser.close()
        
        if not found:
            print("\n" + "!"*50)
            print("报告：全网轮询完毕，目前主流高清站似乎都还没更新此资源。")
            print("建议：过两天再试试，或者尝试搜缩写。")
            print("!"*50)

# 运行主循环
print("\n🎬 全自动轮询特工 5.0 上线")
while True:
    q = input("\n想看什么? (输入 exit 退出): ")
    if q.lower() == 'exit': break
    if q.strip():
        auto_scout(q)
