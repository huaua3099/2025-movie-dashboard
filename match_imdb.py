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

import pandas as pd
import glob
import os

def merge_imdb_files():
    # 1. 尋找所有符合檔名規則的 CSV (例如 2025_imdb_selenium_TW.csv)
    # 這樣寫可以抓到有地區後綴的，也可以抓到原本那個沒有後綴的
    csv_files = glob.glob("2025_imdb_selenium*.csv")
    
    if not csv_files:
        print("❌ 找不到任何 '2025_imdb_selenium' 開頭的 CSV 檔案。")
        return

    print(f"📂 找到 {len(csv_files)} 個檔案: {csv_files}")

    all_dfs = []

    for filename in csv_files:
        try:
            # 讀取 CSV
            df = pd.read_csv(filename)
            
            # 檢查是否有 Region 欄位，如果沒有，嘗試從檔名推測 (例如 _TW.csv -> TW)
            # 但您上傳的檔案裡面似乎都已經有 'Region' 欄位了，所以這裡做個雙重確認
            if 'Region' not in df.columns:
                # 簡單的檔名解析邏輯
                if '_' in filename and len(filename.split('_')[-1].replace('.csv','')) == 2:
                    region_code = filename.split('_')[-1].replace('.csv','')
                    df['Region'] = region_code
                else:
                    df['Region'] = 'Unknown'

            # 標記資料來源 (方便之後擴充 Netflix 資料時區分)
            df['Source'] = 'IMDb'

            all_dfs.append(df)
            print(f"   ✅ 已讀取: {filename} ({len(df)} 筆)")
            
        except Exception as e:
            print(f"   ⚠️ 無法讀取 {filename}: {e}")

    # 2. 合併所有 DataFrame
    if all_dfs:
        master_df = pd.concat(all_dfs, ignore_index=True)
        
        # 3. 資料清洗與轉換
        # 將 'Rating' 欄位轉為數值型態的 'Score'，遇到 'N/A' 或 'Rate' 會變成 NaN
        master_df['Score'] = pd.to_numeric(master_df['Rating'], errors='coerce')
        
        # 4. 存檔
        output_filename = "master_movie_data_imdb.csv"
        master_df.to_csv(output_filename, index=False, encoding="utf-8-sig")
        
        print("\n" + "="*30)
        print(f"🎉 合併完成！")
        print(f"📊 總筆數: {len(master_df)}")
        print(f"💾 檔案已儲存為: {output_filename}")
        print("="*30)
        
        # 檢查一下各區資料量
        print("\n[各地區資料統計]")
        print(master_df['Region'].value_counts())
        
    else:
        print("沒有有效的資料可以合併。")

if __name__ == "__main__":
    merge_imdb_files()