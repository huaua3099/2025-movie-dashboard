# import pandas as pd
# import glob
# import os

# # 1. 找出所有符合命名規則的 CSV 檔案
# csv_files = glob.glob("*Formatted.csv") # 搜尋所有結尾是 Formatted.csv 的檔案
# print(f"找到以下檔案: {csv_files}")

# # 2. 合併資料
# df_list = []
# for filename in csv_files:
#     df = pd.read_csv(filename)
    
#     # === 自動判斷來源 (Source) ===
#     if "Netflix" in filename:
#         df['Source'] = 'Netflix'
#         # 如果原始資料欄位叫 Rating，改名為 Rank (因為 Netflix 是排名)
#         if 'Rating' in df.columns:
#             df.rename(columns={'Rating': 'Rank'}, inplace=True)
            
#     elif "IMDb" in filename:
#         df['Source'] = 'IMDb'
#         # 如果原始資料欄位叫 Rating，改名為 Score
#         if 'Rating' in df.columns:
#             df.rename(columns={'Rating': 'Score'}, inplace=True)
            
#     else:
#         df['Source'] = 'Unknown' # 其他來源

#     df_list.append(df)

# # 3. 結合並存檔
# if df_list:
#     master_df = pd.concat(df_list, ignore_index=True)
#     master_df.to_csv("master_movie_data.csv", index=False, encoding="utf-8-sig")
#     print(f"合併成功！共 {len(master_df)} 筆資料，已產生 master_movie_data.csv")
#     print(master_df.head()) # 檢查一下前幾筆
# else:
#     print("沒找到檔案，請確認 CSV 檔跟程式在同一個資料夾。")
# import streamlit as st
# import pandas as pd

# st.set_page_config(page_title="2025 全球電影數據中心", layout="wide")

# # --- 讀取資料 ---
# @st.cache_data
# def load_data():
#     try:
#         # 讀取 CSV
#         df = pd.read_csv("master_movie_data.csv")
        
#         # === 🚨 自動修復資料邏輯 (防止報錯) ===
        
#         # 1. 如果 Source 欄位全是空的，預設填入 'Netflix'
#         if 'Source' in df.columns and df['Source'].isnull().all():
#             df['Source'] = 'Netflix'
            
#         # 2. 如果只有 Rating 欄位，沒有 Rank 或 Score，根據 Source 補上
#         if 'Rating' in df.columns:
#             if 'Rank' not in df.columns:
#                 df['Rank'] = df['Rating']  # 假設 Rating 就是 Rank
#             if 'Score' not in df.columns:
#                 df['Score'] = df['Rating'] # 假設 Rating 就是 Score
                
#         # 3. 移除 Source 還是空的資料 (雙重保險)
#         df = df.dropna(subset=['Source'])
        
#         return df
#     except FileNotFoundError:
#         return None

# df = load_data()

# st.title("🎬 2025 全球電影數據中心")

# if df is not None:
#     # === 側邊欄 ===
#     st.sidebar.header("🔍 篩選面板")
    
#     # 1. 資料來源篩選
#     # 這裡使用 dropna() 確保不會選到空值
#     all_sources = df['Source'].unique().tolist()
    
#     if not all_sources:
#         st.error("資料來源 (Source) 欄位無有效數據。")
#         st.stop()
        
#     selected_source = st.sidebar.selectbox("你想看哪種數據？", all_sources)
    
#     # 2. 地區篩選
#     available_regions = df[df['Source'] == selected_source]['Region'].unique().tolist()
#     selected_regions = st.sidebar.multiselect(
#         "選擇地區:",
#         options=available_regions,
#         default=available_regions
#     )

#     # === 資料過濾 ===
#     filtered_df = df[
#         (df['Source'] == selected_source) & 
#         (df['Region'].isin(selected_regions))
#     ]

#     # === 顯示邏輯 ===
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         st.subheader(f"📋 {selected_source} 電影清單")
        
#         display_cols = ['Region', 'Title'] # 預設欄位
        
#         if selected_source == 'Netflix':
#             # 確保 Rank 欄位存在
#             if 'Rank' in filtered_df.columns:
#                 filtered_df = filtered_df.sort_values(by='Rank', ascending=True)
#                 display_cols.append('Rank')
#                 st.info("💡 Netflix 數據顯示的是 **「當週排名」** (數字越小越好)")
#             else:
#                 st.warning("⚠️ 找不到排名 (Rank) 資料")
            
#         elif selected_source == 'IMDb':
#             # 確保 Score 欄位存在
#             if 'Score' in filtered_df.columns:
#                 filtered_df = filtered_df.sort_values(by='Score', ascending=False)
#                 display_cols.append('Score')
#                 st.info("💡 IMDb 數據顯示的是 **「觀眾評分」** (滿分 10 分)")
#             else:
#                 st.warning("⚠️ 找不到評分 (Score) 資料")

#         # 顯示表格
#         st.dataframe(
#             filtered_df[display_cols],
#             use_container_width=True,
#             hide_index=True
#         )

#     with col2:
#         st.subheader("📊 統計圖表")
        
#         if not filtered_df.empty:
#             top_titles = filtered_df['Title'].value_counts().head(10)
            
#             st.write(f"**{selected_source} 熱門電影 (上榜次數)**")
#             st.bar_chart(top_titles)
            
#             # IMDb 特有的評分分佈
#             if selected_source == 'IMDb' and 'Score' in filtered_df.columns:
#                 st.write("**評分分佈**")
#                 st.line_chart(filtered_df['Score'])
#         else:
#             st.warning("沒有資料可顯示，請調整篩選條件。")

# else:
#     st.error("找不到 master_movie_data.csv，請確認檔案是否已上傳或產生。")


import streamlit as st
import pandas as pd

st.set_page_config(page_title="2025 全球電影數據中心", layout="wide", page_icon="🎬")

@st.cache_data
def load_data():
    try:
        return pd.read_csv("master_movie_data.csv")
    except:
        return None

df = load_data()

st.title("🎬 2025 全球電影數據中心")

if df is not None:
    # === 側邊欄 ===
    st.sidebar.header("🔍 篩選")
    
    # 1. 選擇資料來源
    sources = df['Source'].unique().tolist()
    selected_source = st.sidebar.selectbox("資料來源", sources)
    
    # 2. 選擇地區
    # 根據選的來源，動態更新地區選單
    available_regions = df[df['Source'] == selected_source]['Region'].unique().tolist()
    selected_regions = st.sidebar.multiselect("地區", available_regions, default=available_regions)
    
    # === 資料過濾 ===
    filtered_df = df[
        (df['Source'] == selected_source) & 
        (df['Region'].isin(selected_regions))
    ]

    # === 顯示邏輯 (根據來源變身) ===
    if selected_source == 'Netflix':
        st.subheader("🔥 Netflix 熱門收視排名")
        st.info("指標：Rank (名次，越小越好)")
        
        # 排序：名次 1 -> 10
        filtered_df = filtered_df.sort_values('Rank', ascending=True)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.dataframe(filtered_df[['Region', 'Title', 'Rank']], use_container_width=True, hide_index=True)
        with col2:
            # 統計最常上榜的電影
            top_titles = filtered_df['Title'].value_counts().head(10)
            st.bar_chart(top_titles)

    elif selected_source == 'IMDb':
        st.subheader("⭐ IMDb 觀眾評分榜")
        st.info("指標：Score (評分，越高越好)")
        
        # 排序：分數 10 -> 0
        filtered_df = filtered_df.sort_values('Score', ascending=False)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.dataframe(filtered_df[['Region', 'Title', 'Score']], use_container_width=True, hide_index=True)
        with col2:
            # 畫出前 10 名分數圖
            if not filtered_df.empty:
                top_10 = filtered_df.head(10).set_index('Title')['Score']
                st.bar_chart(top_10, color="#F5C518") # IMDb 黃色

else:
    st.error("請先執行 merge_all.py 產生 master_movie_data.csv")