import threading
import queue
import time

# 建立一個共享的任務佇列
task_queue = queue.Queue()

# 定義工作者執行緒的行為
def worker(name):
    while True:
        task = task_queue.get() # 執行緒會阻塞在 task_queue.get()，直到 queue 裡有東西可以取出。
        if task is None:
            print(f"{name} 收到結束訊號，停止工作")
            break
        print(f"{name} 正在處理任務：{task}")
        time.sleep(1)  # 模擬任務處理時間
        task_queue.task_done()

# 建立並啟動工作者執行緒
threads = []
for i in range(3):
    t = threading.Thread(target=worker, args=(f"工作者-{i}",))
    t.start() # 讓它開始執行 worker() 函式。這些執行緒會在背景中持續等待任務。
    threads.append(t)

# 主執行緒放入任務
for task_num in range(10):
    task_queue.put(f"任務-{task_num}")

# 等待所有任務完成
task_queue.join()

# 發送結束訊號給工作者
for _ in threads:
    task_queue.put(None)

# 等待所有工作者結束
for t in threads:
    t.join()

print("所有任務已完成，程式結束")