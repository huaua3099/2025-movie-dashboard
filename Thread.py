import threading
import time
finish_lock = threading.Lock()

def run_race(student_id, student_name, run_time, results):
    start_delay = (time.time() * 1000000) % 0.01 
    time.sleep(start_delay)
    # 模擬跑步
    time.sleep(run_time)
    finish_time = time.time()
    with finish_lock:
        results.append((finish_time, student_id, student_name))
        print(f"[完成] 學生 {student_id}: {student_name}")

def race_simulation(students, run_time=2.0):
    threads = []
    results = []
    print(f"\n--- 模擬跑步比賽（每位學生跑步時間 = {run_time} 秒） ---")
    # 建立每位學生的執行緒
    for student_id, student_name in students:
        t = threading.Thread(target=run_race, args=(student_id, student_name, run_time, results))
        t.start()
        threads.append(t)
    # 等待所有學生完成
    for t in threads:
        t.join()
    # 排序完成名次
    results_sorted = sorted(results, key=lambda x: x[0])
    print("\n== 本次比賽名次 ==")
    for rank, (_, student_id, student_name) in enumerate(results_sorted, start=1):
        print(f"第{rank}名. 學生 {student_id}: {student_name}")
    return results_sorted
# 五位小學生
students = [
    (1, "小明"),
    (2, "小華"),
    (3, "小美"),
    (4, "小強"),
    (5, "小玲")
]
# 執行比賽
race_simulation(students, run_time=10.0)
