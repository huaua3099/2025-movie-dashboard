# import pandas as pd
# import glob

# # 1. 找出所有符合命名規則的 CSV 檔案
# # 這裡假設你的檔案都在同一個資料夾，且檔名包含 "Netflix"
# csv_files = glob.glob("*Netflix*Formatted.csv")

# print(f"找到以下檔案: {csv_files}")

# # 2. 合併資料
# df_list = []
# for filename in csv_files:
#     df = pd.read_csv(filename)
#     df_list.append(df)

# # 3. 結合並存檔
# if df_list:
#     master_df = pd.concat(df_list, ignore_index=True)
#     master_df.to_csv("master_movie_data.csv", index=False, encoding="utf-8-sig")
#     print("合併成功！已產生 master_movie_data.csv")
# else:
#     print("沒找到檔案，請確認 CSV 檔跟程式在同一個資料夾。")



import streamlit as st
import pandas as pd

st.set_page_config(page_title="2025 全球電影數據中心", layout="wide")

# --- 讀取資料 ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("master_movie_data.csv")
        return df
    except FileNotFoundError:
        return None

df = load_data()

st.title("🎬 2025 全球電影數據中心")

if df is not None:
    # === 側邊欄 ===
    st.sidebar.header("🔍 篩選面板")
    
    # 1. 資料來源篩選 (Netflix vs IMDb)
    all_sources = df['Source'].unique().tolist()
    selected_source = st.sidebar.selectbox("你想看哪種數據？", all_sources)
    
    # 2. 地區篩選
    # 根據選定的來源，找出有哪些地區可選
    available_regions = df[df['Source'] == selected_source]['Region'].unique().tolist()
    selected_regions = st.sidebar.multiselect(
        "選擇地區:",
        options=available_regions,
        default=available_regions
    )

    # === 資料過濾 ===
    filtered_df = df[
        (df['Source'] == selected_source) & 
        (df['Region'].isin(selected_regions))
    ]

    # === 顯示邏輯 (根據來源顯示不同欄位) ===
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"📋 {selected_source} 電影清單")
        
        if selected_source == 'Netflix':
            # 如果是 Netflix，顯示「排名」
            # 依照 Rank 排序 (小到大)
            filtered_df = filtered_df.sort_values(by='Rank', ascending=True)
            display_cols = ['Region', 'Title', 'Rank']
            st.info("💡 Netflix 數據顯示的是 **「當週排名」** (數字越小越好)")
            
        elif selected_source == 'IMDb':
            # 如果是 IMDb，顯示「評分」
            # 依照 Score 排序 (大到小)
            filtered_df = filtered_df.sort_values(by='Score', ascending=False)
            display_cols = ['Region', 'Title', 'Score']
            st.info("💡 IMDb 數據顯示的是 **「觀眾評分」** (滿分 10 分)")
        
        else:
            display_cols = ['Region', 'Title', 'Source']

        # 顯示表格
        st.dataframe(
            filtered_df[display_cols],
            use_container_width=True,
            hide_index=True
        )

    with col2:
        st.subheader("📊 統計圖表")
        
        if not filtered_df.empty:
            # 統計最常出現的電影 (跨區霸榜)
            top_titles = filtered_df['Title'].value_counts().head(10)
            
            st.write(f"**{selected_source} 熱門電影 (上榜次數)**")
            st.bar_chart(top_titles)
            
            # 如果是 IMDb，還可以畫一個「評分分佈圖」
            if selected_source == 'IMDb':
                st.write("**評分分佈**")
                st.line_chart(filtered_df['Score'])
        else:
            st.warning("沒有資料可顯示，請調整篩選條件。")

else:
    st.error("找不到 master_movie_data.csv，請先執行 merge_all.py")