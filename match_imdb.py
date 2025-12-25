# import pandas as pd
# import glob
# import os

# def merge_imdb_files():
#     # 1. 尋找所有符合檔名規則的 CSV (例如 2025_imdb_selenium_TW.csv)
#     # 這樣寫可以抓到有地區後綴的，也可以抓到原本那個沒有後綴的
#     csv_files = glob.glob("2025_imdb_selenium*.csv")
    
#     if not csv_files:
#         print("❌ 找不到任何 '2025_imdb_selenium' 開頭的 CSV 檔案。")
#         return

#     print(f"📂 找到 {len(csv_files)} 個檔案: {csv_files}")

#     all_dfs = []

#     for filename in csv_files:
#         try:
#             # 讀取 CSV
#             df = pd.read_csv(filename)
            
#             # 檢查是否有 Region 欄位，如果沒有，嘗試從檔名推測 (例如 _TW.csv -> TW)
#             # 但您上傳的檔案裡面似乎都已經有 'Region' 欄位了，所以這裡做個雙重確認
#             if 'Region' not in df.columns:
#                 # 簡單的檔名解析邏輯
#                 if '_' in filename and len(filename.split('_')[-1].replace('.csv','')) == 2:
#                     region_code = filename.split('_')[-1].replace('.csv','')
#                     df['Region'] = region_code
#                 else:
#                     df['Region'] = 'Unknown'

#             # 標記資料來源 (方便之後擴充 Netflix 資料時區分)
#             df['Source'] = 'IMDb'

#             all_dfs.append(df)
#             print(f"   ✅ 已讀取: {filename} ({len(df)} 筆)")
            
#         except Exception as e:
#             print(f"   ⚠️ 無法讀取 {filename}: {e}")

#     # 2. 合併所有 DataFrame
#     if all_dfs:
#         master_df = pd.concat(all_dfs, ignore_index=True)
        
#         # 3. 資料清洗與轉換
#         # 將 'Rating' 欄位轉為數值型態的 'Score'，遇到 'N/A' 或 'Rate' 會變成 NaN
#         master_df['Score'] = pd.to_numeric(master_df['Rating'], errors='coerce')
        
#         # 4. 存檔
#         output_filename = "master_movie_data_imdb.csv"
#         master_df.to_csv(output_filename, index=False, encoding="utf-8-sig")
        
#         print("\n" + "="*30)
#         print(f"🎉 合併完成！")
#         print(f"📊 總筆數: {len(master_df)}")
#         print(f"💾 檔案已儲存為: {output_filename}")
#         print("="*30)
        
#         # 檢查一下各區資料量
#         print("\n[各地區資料統計]")
#         print(master_df['Region'].value_counts())
        
#     else:
#         print("沒有有效的資料可以合併。")

# if __name__ == "__main__":
#     merge_imdb_files()

# import pandas as pd
# import glob
# import os

# def merge_imdb_files():
#     # 1. 尋找所有符合檔名規則的 CSV (例如 2025_imdb_selenium_TW.csv)
#     # 這樣寫可以抓到有地區後綴的，也可以抓到原本那個沒有後綴的
#     csv_files = glob.glob("2025_imdb_selenium*.csv")
    
#     if not csv_files:
#         print("❌ 找不到任何 '2025_imdb_selenium' 開頭的 CSV 檔案。")
#         return

#     print(f"📂 找到 {len(csv_files)} 個檔案: {csv_files}")

#     all_dfs = []

#     for filename in csv_files:
#         try:
#             # 讀取 CSV
#             df = pd.read_csv(filename)
            
#             # 檢查是否有 Region 欄位，如果沒有，嘗試從檔名推測 (例如 _TW.csv -> TW)
#             # 但您上傳的檔案裡面似乎都已經有 'Region' 欄位了，所以這裡做個雙重確認
#             if 'Region' not in df.columns:
#                 # 簡單的檔名解析邏輯
#                 if '_' in filename and len(filename.split('_')[-1].replace('.csv','')) == 2:
#                     region_code = filename.split('_')[-1].replace('.csv','')
#                     df['Region'] = region_code
#                 else:
#                     df['Region'] = 'Unknown'

#             # 標記資料來源 (方便之後擴充 Netflix 資料時區分)
#             df['Source'] = 'IMDb'

#             all_dfs.append(df)
#             print(f"   ✅ 已讀取: {filename} ({len(df)} 筆)")
            
#         except Exception as e:
#             print(f"   ⚠️ 無法讀取 {filename}: {e}")

#     # 2. 合併所有 DataFrame
#     if all_dfs:
#         master_df = pd.concat(all_dfs, ignore_index=True)
        
#         # 3. 資料清洗與轉換
#         # 將 'Rating' 欄位轉為數值型態的 'Score'，遇到 'N/A' 或 'Rate' 會變成 NaN
#         master_df['Score'] = pd.to_numeric(master_df['Rating'], errors='coerce')
        
#         # 4. 存檔
#         output_filename = "master_movie_data_imdb.csv"
#         master_df.to_csv(output_filename, index=False, encoding="utf-8-sig")
        
#         print("\n" + "="*30)
#         print(f"🎉 合併完成！")
#         print(f"📊 總筆數: {len(master_df)}")
#         print(f"💾 檔案已儲存為: {output_filename}")
#         print("="*30)
        
#         # 檢查一下各區資料量
#         print("\n[各地區資料統計]")
#         print(master_df['Region'].value_counts())
        
#     else:
#         print("沒有有效的資料可以合併。")

# if __name__ == "__main__":
#     merge_imdb_files()
import streamlit as st
import pandas as pd

# 1. 設定網頁標題與版面
st.set_page_config(page_title="2025 IMDb 全球電影情報中心", layout="wide", page_icon="🎬")

# 2. 讀取資料函數 (加上快取功能，讓網頁跑更快)
@st.cache_data
def load_data():
    try:
        # 讀取 CSV 檔案
        df = pd.read_csv("master_movie_data_imdb.csv")
        
        # 確保分數欄位是數字 (處理可能的錯誤資料)
        df['Score'] = pd.to_numeric(df['Score'], errors='coerce')
        
        return df
    except FileNotFoundError:
        return None

# 載入資料
df = load_data()

# 3. 網頁介面設計
st.title("🎬 2025 IMDb 全球電影情報中心")
st.markdown("匯集 **台灣、南韓、日本、香港、澳洲** 等地的最新電影評分數據")

if df is not None:
    # === 側邊欄：篩選條件 ===
    st.sidebar.header("🔍 篩選面板")
    
    # (A) 地區篩選
    # 取得所有地區清單
    all_regions = sorted(df['Region'].unique().tolist())
    
    # 預設全選
    selected_regions = st.sidebar.multiselect(
        "選擇地區 (Region)",
        all_regions,
        default=all_regions
    )
    
    # (B) 分數篩選
    min_score = st.sidebar.slider("最低評分 (Score)", 0.0, 10.0, 6.0, 0.1)

    # === 資料過濾邏輯 ===
    # 1. 篩選地區
    filtered_df = df[df['Region'].isin(selected_regions)]
    # 2. 篩選分數 (且排除沒有分數的 N/A)
    filtered_df = filtered_df[filtered_df['Score'] >= min_score]
    # 3. 排序 (高分在前)
    filtered_df = filtered_df.sort_values(by='Score', ascending=False)

    # === 關鍵指標 (KPI) ===
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("符合條件電影數", f"{len(filtered_df)} 部")
    with col2:
        # 顯示最高分的那部電影
        if not filtered_df.empty:
            top_movie = filtered_df.iloc[0]['Title']
            top_score = filtered_df.iloc[0]['Score']
            st.metric("目前冠軍", f"{top_movie}", f"{top_score} 分")
        else:
            st.metric("目前冠軍", "無資料")
    with col3:
        # 顯示平均分
        if not filtered_df.empty:
            avg_score = filtered_df['Score'].mean()
            st.metric("平均評分", f"{avg_score:.1f} 分")
        else:
            st.metric("平均評分", "0 分")

    st.divider() # 分隔線

    # === 主要內容區 (左右兩欄) ===
    left_col, right_col = st.columns([2, 1])

    with left_col:
        st.subheader("📋 詳細片單")
        
        # 簡單的文字搜尋框
        search_txt = st.text_input("搜尋片名...", "")
        if search_txt:
            filtered_df = filtered_df[filtered_df['Title'].str.contains(search_txt, case=False)]
            
        # 顯示資料表 (隱藏 Source 欄位，比較乾淨)
        st.dataframe(
            filtered_df[['Region', 'Title', 'Rating', 'Score']],
            use_container_width=True,
            hide_index=True,
            height=600
        )

    with right_col:
        st.subheader("🏆 Top 10 排行榜")
        
        if not filtered_df.empty:
            # 取前 10 名
            top_10_df = filtered_df.head(10).sort_values(by='Score', ascending=True) # 為了讓長條圖從高到低排，這裡要反過來
            
            # 畫橫向長條圖
            st.bar_chart(
                data=top_10_df,
                x="Score",
                y="Title",
                color="#F5C518", # IMDb 的經典黃色
                horizontal=True  # 橫向顯示比較好讀片名
            )
            
            # 額外分析：各地區上榜數量
            st.subheader("📊 地區分佈")
            region_counts = filtered_df['Region'].value_counts()
            st.bar_chart(region_counts)

        else:
            st.info("沒有資料，請調整篩選條件。")

else:
    st.error("找不到檔案 `master_movie_data_imdb.csv`，請確認檔案已上傳！")
