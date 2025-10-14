### Python FastAPI透過Uvicorn ASGI Server 可以幫助我們跟前端更有效率的互動

啟動 FastAPI >> ` uvicorn main:app --reload`

安裝 Postgresql >> `pip install fastapi uvicorn psycopg2-binary sqlalchemy alembic python-dotenv
`

### 預計練習項目

- CRUD Rest API
- JSON API
- XML API
- FORM SUBMIT
- 檔案上傳 API
- 檔案下載 API
- WebSocket API
- GraphQL API
- RPC
- JWT Token
- 分頁

## GPT建議學習項目

🏗️ 一、基礎延伸（API層強化）

你現有的 CRUD、JSON、XML、Form、File、WebSocket、JWT 都是基石。
可以再補這些讓 API 更完整：

1️⃣ Query 與 Pagination

實作查詢參數（filter、sort、page、limit）。

練習 Response Model（response_model）的輸出結構控制。

👉 重點：模擬真實前端查表格資料的場景。

2️⃣ Error Handling + Exception Middleware

自訂錯誤格式（例如統一成 {code, message, detail}）。

實作全域 ExceptionHandler。

加上 Logging Middleware。

👉 重點：這是實務開發不可或缺的品質提升。

3️⃣ Rate Limiting / CORS / Middleware

實作 Request 限速（使用 Starlette middleware 或 redis-based 限流）。

配置 CORS，模擬跨域前端呼叫。

👉 重點：貼近生產環境安全需求。

🧩 二、資料存取層（Persistence Layer）

FastAPI 本身是框架，但與資料層整合是核心能力。

4️⃣ ORM / Database Integration

使用 SQLAlchemy 2.x 或 Tortoise ORM。

練習建立 Model、Session、Transaction。

加上 Migration（Alembic）。

👉 練習目標：實作 User / Post / Comment 三表關聯。

5️⃣ Redis / Cache

實作快取機制（GET API Cache）。

練習 Session Token 儲存、短期資料保存。

👉 重點：你未來在電商或登入服務都會用到。

🧠 三、進階應用層（真實業務功能）
6️⃣ OAuth2 + JWT Refresh

你已經列了 JWT，可以再加上 refresh token 與權限驗證。
e.g. Depends(get_current_user) + RBAC（Role-Based Access Control）。

👉 重點：真實專案都會區分 admin / user 權限。

7️⃣ Background Tasks

使用 FastAPI 的 BackgroundTasks。

模擬寄信、推播、資料分析等非同步任務。

👉 重點：學會用 event-driven 思維處理慢任務。

8️⃣ Scheduler / CronJob

可搭配 APScheduler 建立排程任務 API。

練習排程每日報表或清理資料。

9️⃣ Dependency Injection 與 DI Container

FastAPI 的 Depends() 是強大的 DI 工具。

練習組裝 repository、service、auth 等層。

👉 重點：提升架構清晰度，貼近 DDD。

⚙️ 四、API生態與整合
🔹 GraphQL（你已列）

→ 建議使用 Strawberry 或 Ariadne。
試著整合 SQLAlchemy 並加入 Auth 驗證。

🔹 gRPC / RPC（你已列）

→ 可再搭配 protobuf 定義 contract，練習 typed communication。

🌍 五、部署與架構實戰
10️⃣ Docker 化

使用 Dockerfile + docker-compose 包 FastAPI + PostgreSQL + Redis。
👉 重點：這是進入微服務世界的門檻。

11️⃣ CI/CD Pipeline

用 GitHub Actions 自動測試與部署。
👉 重點：讓專案具備 DevOps 觀點。

12️⃣ Testing

用 pytest + httpx 撰寫整合測試。

模擬 request/response，驗證 endpoint。

13️⃣ OpenAPI / Schema Versioning

練習用 FastAPI 的 tags、version prefix (/v1, /v2)。

模擬版本升級場景。

🔮 六、創新與延伸（進階挑戰題）
主題	說明
📊 WebSocket + Redis Pub/Sub	模擬多人聊天室或即時訂單通知
🤖 AI Model Serving	用 FastAPI 包裝 ML 模型，輸入文字/圖片返回結果
🧱 Event-driven + Kafka	模擬 Outbox Pattern（可結合你之前的 Debezium 經驗）
🧰 Plugin 架構	練習將模組抽成 plugin-like 結構，易擴充
🧾 Async File Stream	實作大檔案上傳 / 分塊下載 API