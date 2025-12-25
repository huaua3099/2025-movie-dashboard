# import pandas as pd
# import io
# import requests

# def fetch_australia_netflix_data():
#     url = "https://www.netflix.com/tudum/top10/data/all-weeks-countries.tsv"
    
#     print(f"正在連線至 Netflix 官方資料庫抓取澳洲數據...")
    
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
        
#         # 讀取 TSV
#         df = pd.read_csv(io.StringIO(response.text), sep='\t')
        
#         # --- 資料清洗 ---
#         df['week'] = pd.to_datetime(df['week'])
        
#         # 1. 篩選 2025 年
#         filter_year = (df['week'] >= '2025-01-01') & (df['week'] <= '2025-12-31')
        
#         # 2. 【關鍵修改】只鎖定 Australia
#         filter_country = df['country_name'] == 'Australia'
        
#         # 3. 篩選電影 (排除影集)
#         filter_category = df['category'].str.contains('Films', case=False)
        
#         # 執行篩選
#         df_clean = df[filter_year & filter_country & filter_category].copy()
        
#         if df_clean.empty:
#             print("目前抓不到 2025 年澳洲資料，請確認日期範圍。")
#             return

#         # --- 格式化成 Region, Title, Rating ---
        
#         # 1. 將 Region 統一設為 "AU"
#         df_clean['Region'] = 'AU'
        
#         # 2. 重新命名欄位
#         # Title = 片名
#         # Rating = 當週排名 (1-10)
#         df_clean = df_clean.rename(columns={
#             'show_title': 'Title',
#             'weekly_rank': 'Rating'
#         })
        
#         # 3. 只保留需要的欄位
#         final_df = df_clean[['Region', 'Title', 'Rating']]
        
#         # 4. 去除重複，取該電影的最佳排名
#         final_df = final_df.groupby(['Region', 'Title'], as_index=False)['Rating'].min()
        
#         # 依照排名排序 (第1名在最上面)
#         final_df = final_df.sort_values(by='Rating', ascending=True)

#         # 顯示前 10 筆
#         print(f"成功整理出 {len(final_df)} 筆澳洲熱門電影！")
#         print(final_df.head(10))
        
#         # 存檔
#         final_df.to_csv("2025_Netflix_Australia_Formatted.csv", index=False, encoding="utf-8-sig")
#         print("\n檔案已儲存為: 2025_Netflix_Australia_Formatted.csv")

#     except Exception as e:
#         print(f"發生錯誤: {e}")

# if __name__ == "__main__":
#     fetch_australia_netflix_data()