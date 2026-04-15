# 系統流程圖設計 (Flowchart)

本文件基於 PRD 與系統架構文件（ARCHITECTURE.md），以視覺化方式呈現「機車保養與改裝紀錄系統」的使用者操作路徑與後端資料流。

## 1. 使用者流程圖 (User Flow)

展示使用者從進入網站後，可以如何導航並操作各項功能。

```mermaid
flowchart LR
  A([使用者進入網站]) --> B[首頁 - 儀表板 Dashboard]
  
  B --> C{選擇功能模組}
  
  %% 車庫與保養模組
  C -->|車庫功能| D[車庫列表頁]
  D -->|點選新增| D1[填寫新增車輛表單]
  D -->|點選編輯/刪除| D2[修改或刪除車輛]
  D -->|點擊特定車輛| E[專屬保養紀錄頁面]
  
  E -->|點選新增保養| E1[填寫保養與花費工單]
  E -->|點選編輯/刪除| E2[修改保養紀錄內容]
  
  %% 願望清單模組
  C -->|改裝規劃| F[願望清單列表]
  F -->|點選新增| F1[填寫改裝品與預算表單]
  F -->|標記狀態/編輯| F2[更新進度為「已改裝」]
  F -->|點選刪除| F3[移除改裝願望]
```

## 2. 系統序列圖 (Sequence Diagram)

此處以「使用者新增保養紀錄」為例，說明前端表單送出後，資料如何在 Flask 與 SQLite 之間流動。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask 路由 (Controller)
    participant Model as 資料模型 (Model)
    participant DB as SQLite 資料庫

    User->>Browser: 填寫保養紀錄表單並點擊「送出」
    Browser->>Flask: 發送 POST 請求 (含表單資料)
    Flask->>Flask: 進行基礎表單驗證 (如：防呆、金額不能為負數)
    Flask->>Model: 呼叫建立保養紀錄的函式
    Model->>DB: 執行 INSERT INTO SQL 語句
    DB-->>Model: 寫入成功確認
    Model-->>Flask: 取得剛剛新增的資料物件
    Flask-->>Browser: 回傳 HTTP 302 重導向 (Redirect) 至保養列表頁
    Browser-->>User: 畫面重新載入，顯示最新的保養紀錄清單
```

## 3. 功能清單與 URL 路由對照表

以下整理了系統內所有主要功能、對應的 HTTP 方法與建議的網址路徑，作為後續 API 實作與頁面開發的依據：

| 功能名稱 | HTTP 方法 | URL 路徑 (Route) | 說明 |
| :--- | :--- | :--- | :--- |
| **首頁與儀表板** | GET | `/` | 顯示近期到期保養與總花費概覽。 |
| **車庫列表** | GET | `/garage` | 顯示所有名下車輛。 |
| **新增車輛** | GET / POST | `/garage/add` | GET: 顯示新增表單<br>POST: 接收資料寫入 DB |
| **編輯車輛** | GET / POST | `/garage/<v_id>/edit` | 修改指定車輛 (`v_id`) 資訊 |
| **刪除車輛** | POST | `/garage/<v_id>/delete` | 刪除車輛及其相關的保養紀錄 |
| **保養紀錄列表** | GET | `/garage/<v_id>/maintenance` | 檢視指定車輛的歷史保養紀錄 |
| **新增保養紀錄** | GET / POST | `/garage/<v_id>/maintenance/add` | 新增該車的保養日誌與花費 |
| **編輯保養紀錄** | GET / POST | `/maintenance/<m_id>/edit` | 修改指定的保養紀錄 (`m_id`) |
| **刪除保養紀錄** | POST | `/maintenance/<m_id>/delete` | 移除該筆保養紀錄 |
| **改裝願望清單** | GET | `/wishlist` | 查看願望清單列表與預算總計 |
| **新增改裝願望** | GET / POST | `/wishlist/add` | 送出新希望安裝的改裝品與估價 |
| **編輯願望狀態** | GET / POST | `/wishlist/<w_id>/edit` | 更新金額或切換「是否已改裝」標籤 |
| **刪除改裝願望** | POST | `/wishlist/<w_id>/delete` | 把不再需要的改裝品從清單移除 |

> **備註**：`v_id` 代表 Vehicle ID (車輛編號)，`m_id` 代表 Maintenance ID (保養紀錄編號)，`w_id` 代表 Wishlist ID (願望清單編號)。所有的刪除操作都是透過 POST 方法執行，以避免爬蟲或預取行為導致資料意外刪除。
