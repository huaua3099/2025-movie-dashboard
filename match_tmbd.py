import streamlit as st
import pandas as pd

# 1. 頁面設定
st.set_page_config(page_title="2025 全球電影數據中心", layout="wide", page_icon="🍿")

# 2. 讀取資料
@st.cache_data
def load_data():
    try:
        # 讀取合併後的資料
        df = pd.read_csv("master_movie_data_merged.csv")
        return df
    except FileNotFoundError:
        return None

df = load_data()

# 3. 標題與簡介
st.title("🍿 2025 全球電影數據中心")
st.markdown("整合 **Netflix 台灣排行榜** 與 **TMDb 各國熱門電影** 的即時數據儀表板。")

if df is not None:
    # === 側邊欄：篩選器 ===
    st.sidebar.header("🔍 篩選面板")
    
    # (A) 選擇資料來源
    # 這裡很關鍵！因為 Netflix 和 TMDb 的欄位意義不同
    all_sources = df['Source'].unique().tolist()
    selected_source = st.sidebar.selectbox("資料來源 (Source)", all_sources)
    
    # (B) 選擇地區
    # 根據選定的來源，找出有哪些地區可選 (例如 Netflix 目前只有 TW)
    available_regions = df[df['Source'] == selected_source]['Region'].unique().tolist()
    selected_regions = st.sidebar.multiselect(
        "選擇地區 (Region)",
        options=available_regions,
        default=available_regions
    )

    # === 資料過濾 ===
    filtered_df = df[
        (df['Source'] == selected_source) & 
        (df['Region'].isin(selected_regions))
    ]

    # === 核心顯示邏輯 (根據來源變身) ===
    
    st.divider()

    # --- 情境 1: Netflix (看排名) ---
    if selected_source == 'Netflix':
        st.subheader(f"🔥 Netflix 熱門收視排行榜 ({', '.join(selected_regions)})")
        
        # 關鍵指標
        col1, col2 = st.columns(2)
        col1.metric("電影總數", f"{len(filtered_df)} 部")
        # Netflix 第1名
        top1 = filtered_df[filtered_df['Rank'] == 1]['Title'].values
        top1_text = top1[0] if len(top1) > 0 else "無"
        col2.metric("本週冠軍 (Rank 1)", top1_text)

        # 排序：名次越小越好 (1 -> 10)
        filtered_df = filtered_df.sort_values(by='Rank', ascending=True)
        
        # 顯示
        left, right = st.columns([1.5, 1])
        with left:
            st.dataframe(
                filtered_df[['Region', 'Title', 'Rank']],
                use_container_width=True,
                hide_index=True,
                height=600
            )
        with right:
            st.info("💡 這裡顯示的是 **「收視排名」** (數字越小代表越熱門)")
            # 統計：哪些電影霸榜最多次 (如果有跨地區資料更有用)
            top_titles = filtered_df['Title'].value_counts().head(10)
            st.bar_chart(top_titles)
            st.caption("上榜頻率統計")

    # --- 情境 2: TMDb (看熱度/評分) ---
    else: # selected_source == 'TMDb'
        st.subheader(f"📈 TMDb 全球熱門趨勢 ({', '.join(selected_regions)})")
        
        # 分數篩選器 (只在 TMDb 模式顯示)
        min_score = st.sidebar.slider("最低評分/熱度", 0.0, 10.0, 5.0, 0.1)
        filtered_df = filtered_df[filtered_df['Score'] >= min_score]

        # 關鍵指標
        col1, col2, col3 = st.columns(3)
        col1.metric("入榜電影", f"{len(filtered_df)} 部")
        
        # 找出最高分
        if not filtered_df.empty:
            best_movie = filtered_df.loc[filtered_df['Score'].idxmax()]
            col2.metric("最高分電影", best_movie['Title'], f"{best_movie['Score']} 分")
            col3.metric("平均分數", f"{filtered_df['Score'].mean():.2f}")

        # 排序：分數越高越好 (10 -> 0)
        filtered_df = filtered_df.sort_values(by='Score', ascending=False)

        # 顯示
        left, right = st.columns([1.5, 1])
        with left:
            st.dataframe(
                filtered_df[['Region', 'Title', 'Score']],
                use_container_width=True,
                hide_index=True,
                height=600
            )
        with right:
            st.success("💡 這裡顯示的是 **「觀眾評分/熱度」** (數字越大代表評價越好)")
            if not filtered_df.empty:
                # 取前 10 名畫橫向長條圖
                top_10 = filtered_df.head(10).sort_values(by='Score', ascending=True)
                st.bar_chart(
                    data=top_10,
                    x='Score',
                    y='Title',
                    color='#FF4B4B', # 紅色系
                    horizontal=True
                )
                st.caption("Top 10 高分電影")

else:
    st.error("❌ 找不到 `master_movie_data_merged.csv`，請確認檔案已上傳！")