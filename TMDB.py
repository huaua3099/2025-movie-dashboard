import requests
import pandas as pd
import time

# --- 設定區 ---
API_KEY = "9d29640dac511b569f6f16ec3dc3434c" # 您提供的 API Key
BASE_URL = "https://api.themoviedb.org/3/discover/movie"

def get_korea_all_movies_leaderboard():
    all_movies = []
    
    # 參數設定
    params = {
        "api_key": API_KEY,
        "language": "zh-TW",          # 依然抓中文片名，方便閱讀
        "region": "KR",               # 【關鍵修改】鎖定「南韓地區」的上映資訊與熱度
        "sort_by": "popularity.desc", # 依照南韓當地的熱度排序
        
        # 設定年份：2025 全年度
        "primary_release_date.gte": "2025-01-01",
        "primary_release_date.lte": "2025-12-31",
        
        "page": 1 
    }

    print(f"正在抓取 2025 年【南韓】上映之熱門電影排行...")

    # 抓取前 3 頁 (Top 60)
    for page in range(1, 4):
        print(f"正在下載第 {page} 頁資料...")
        params["page"] = page
        
        try:
            response = requests.get(BASE_URL, params=params)
            data = response.json()
            
            if "results" in data:
                for item in data["results"]:
                    # 判斷產地 (如果沒有資料，預設為 KR - 南韓)
                    origin = item.get("origin_country", ["KR"])[0] if item.get("origin_country") else "KR"
                    
                    movie_info = {
                        "Region": origin,
                        "Title": item.get("title"),
                        
                        # 依據您上一段程式碼的邏輯，這裡將「熱度」數值存入 "Rating" 欄位
                        "Rating": item.get("popularity"),
                    }
                    all_movies.append(movie_info)
            else:
                print("沒有數據 (可能 API Key 錯了)")
                break
                
        except Exception as e:
            print(f"連線錯誤: {e}")
            
        time.sleep(0.3)

    return all_movies

# --- 主程式 ---

# 1. 執行
ranking_data = get_korea_all_movies_leaderboard()

# 2. 轉成 DataFrame
df = pd.DataFrame(ranking_data)

# 3. 顯示前 10 名
print("\n--- 🏆 2025 南韓熱門電影 Top 10 ---")
# 印出：產地、片名、熱度(Rating欄位)
print(df[["Region", "Title", "Rating"]].head(10))

# 4. 存檔 (檔名改為 Korea)
df.to_csv("2025_Korea_Global_Leaderboard.csv", index=False, encoding="utf-8-sig")
print("\n檔案已儲存為 2025_Korea_Global_Leaderboard.csv")