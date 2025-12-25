from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

def scrape_imdb_with_selenium(region_name, country_codes):
    """
    使用 Selenium 模擬瀏覽器爬取 IMDb
    """
    # 組合 URL
    url = f"https://www.imdb.com/search/title/?title_type=feature&release_date=2025-01-01,2025-12-31&countries={country_codes}"
    
    print(f"[{region_name}] 正在啟動瀏覽器爬取: {url}")

    # --- 設定 Selenium ---
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # 如果不想看到視窗彈出來，可以把這行註解拿掉 (但在測試階段建議開著)
    options.add_argument("--disable-blink-features=AutomationControlled") # 試圖隱藏自動化特徵
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    # 自動下載並啟動 Chrome Driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        
        # --- 關鍵：等待網頁載入 ---
        # 讓它睡個 5-8 秒，確保 JavaScript 把電影資料跑出來
        # 如果網速慢，可以設久一點
        time.sleep(8) 
        
        # 捲動視窗到底部幾次，觸發更多資料載入 (雖然 IMDb 現在通常是按鈕，但捲動是好習慣)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        time.sleep(2)
        
        # 把現在瀏覽器看到的 HTML 拿出來給 BeautifulSoup 解析
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        movies = []
        
        # --- 更新後的選擇器邏輯 ---
        # 這次我們直接找「標題」的 class，比較不容易失敗
        # IMDb 目前標題的 class 通常是 "ipc-title__text"
        
        # 找到所有包含電影資訊的容器
        # 這裡用比較寬鬆的寫法：找 h3 標籤且 class 包含 ipc-title__text
        title_tags = soup.select("h3.ipc-title__text")
        
        print(f"找到 {len(title_tags)} 個標題標籤 (包含雜訊)...")

        for tag in title_tags:
            # 取得標題文字
            text = tag.text.strip()
            
            # 過濾掉雜訊：IMDb 的標題通常是 "1. The Movie Name"
            # 我們只保留有數字開頭的，代表它是清單裡的一部電影
            if not text[0].isdigit():
                continue
                
            # 處理片名 (去除前面的排名數字 "1. ")
            try:
                title = text.split('. ', 1)[1]
            except IndexError:
                title = text # 如果切分失敗就保留原樣

            # 嘗試抓取評分 (這比較難，因為評分標籤在標題標籤的外面)
            # 我們用 parent 往上找，再找裡面的評分
            # 注意：這裡可能會因為結構變動而抓不到，設為 N/A 比較保險
            try:
                # 往上找父層，再找評分 span
                card = tag.find_parent("li")
                if card:
                    rating_tag = card.select_one("span.ipc-rating-star")
                    rating = rating_tag.text.strip().split()[0] if rating_tag else "No Rating"
                else:
                    rating = "N/A"
            except:
                rating = "N/A"

            movies.append({
                "Region": region_name,
                "Title": title,
                "Rating": rating
            })

        print(f"成功解析出 {len(movies)} 部電影！")
        return movies

    except Exception as e:
        print(f"發生錯誤: {e}")
        return []
        
    finally:
        driver.quit() # 記得關閉瀏覽器

# --- 主程式 ---

regions = {
    "HK": "HK",
    # 為了測試，我們先只跑亞洲，確認成功後再把下面註解打開
    # "Europe": "GB,FR,DE,IT,ES",
    # "America": "US,CA,BR"
}

all_data = []

for region, codes in regions.items():
    data = scrape_imdb_with_selenium(region, codes)
    all_data.extend(data)
    time.sleep(3) # 休息一下

df = pd.DataFrame(all_data)
print("\n--- 爬取結果 ---")
print(df.head())

# 只有抓到資料才存檔
if not df.empty:
    df.to_csv("2025_imdb_selenium_HK.csv", index=False, encoding="utf-8-sig")
    print("檔案已儲存！")
else:
    print("還是空的... 請檢查你的網路或瀏覽器畫面。")