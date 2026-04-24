# 路由與頁面設計文件 (ROUTES)

本文件描述了「機車保養與改裝紀錄系統」的所有 Flask 路由，以及對應的 Jinja2 模板，幫助開發者釐清前後端資料傳遞的路徑。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁儀表板** | GET | `/` | `dashboard/index.html` | 顯示近期需保養項目與總花費概覽。 |
| **車庫列表** | GET | `/garage/` | `garage/index.html` | 顯示所有名下車輛。 |
| **新增車輛** | GET / POST | `/garage/add` | `garage/form.html` | 顯示新增表單，接收表單並寫入 DB。 |
| **編輯車輛** | GET / POST | `/garage/<v_id>/edit` | `garage/form.html` | 顯示並接收修改指定車輛 (`v_id`) 的表單。 |
| **刪除車輛** | POST | `/garage/<v_id>/delete` | — | 刪除車輛與其保養紀錄，重導向回列表。 |
| **保養紀錄清單** | GET | `/garage/<v_id>/maintenance/` | `maintenance/index.html` | 檢視指定車輛的歷史保養紀錄。 |
| **新增保養** | GET / POST | `/garage/<v_id>/maintenance/add` | `maintenance/form.html` | 針對指定車輛新增保養項目與花費。 |
| **編輯保養** | GET / POST | `/maintenance/<m_id>/edit` | `maintenance/form.html` | 修改指定保養紀錄 (`m_id`)。 |
| **刪除保養** | POST | `/maintenance/<m_id>/delete` | — | 刪除保養紀錄，重導向回該車的保養清單。 |
| **願望清單列表** | GET | `/wishlist/` | `wishlist/index.html` | 顯示願望清單列表與預算總計。 |
| **新增願望** | GET / POST | `/wishlist/add` | `wishlist/form.html` | 新增改裝品項目與預估花費。 |
| **編輯願望** | GET / POST | `/wishlist/<w_id>/edit` | `wishlist/form.html` | 更新項目內容、金額或狀態。 |
| **切換願望狀態** | POST | `/wishlist/<w_id>/toggle` | — | 快速切換「未安裝/已安裝」狀態並重導向回列表。 |
| **刪除願望** | POST | `/wishlist/<w_id>/delete` | — | 從清單移除該改裝品項目。 |

---

## 2. 路由詳細說明

### 2.1 首頁儀表板 (Dashboard Blueprint)

- **`GET /`**
  - **輸入**：無
  - **處理邏輯**：呼叫 `Vehicle.get_all()` 取得車輛清單，並依序呼叫 `MaintenanceRecord.get_due_maintenance()`，彙整出所有即將到期或已到期的保養項目。
  - **輸出**：渲染 `dashboard/index.html`。

### 2.2 車庫管理 (Garage Blueprint)

- **`GET /garage/`**
  - **輸出**：渲染 `garage/index.html`，傳入所有車輛。
- **`GET /garage/add`**
  - **輸出**：渲染 `garage/form.html`，用於新增。
- **`POST /garage/add`**
  - **輸入**：表單欄位 (`brand`, `model_name`, `current_mileage`)。
  - **處理邏輯**：呼叫 `Vehicle.create()`。
  - **輸出**：成功後重導向至 `/garage/`。
- **`GET /garage/<v_id>/edit`**
  - **輸出**：渲染 `garage/form.html`，並將取得的 `vehicle` 資料填入表單。
- **`POST /garage/<v_id>/edit`**
  - **處理邏輯**：呼叫 `Vehicle.update()`。
  - **輸出**：成功後重導向至 `/garage/`。
- **`POST /garage/<v_id>/delete`**
  - **處理邏輯**：呼叫 `Vehicle.delete()`。
  - **輸出**：重導向至 `/garage/`。

### 2.3 保養紀錄 (Maintenance Blueprint)

- **`GET /garage/<v_id>/maintenance/`**
  - **處理邏輯**：確認該車輛存在，呼叫 `MaintenanceRecord.get_by_vehicle(v_id)`。
  - **輸出**：渲染 `maintenance/index.html`。
- **`GET /garage/<v_id>/maintenance/add`**
  - **輸出**：渲染 `maintenance/form.html`。
- **`POST /garage/<v_id>/maintenance/add`**
  - **輸入**：表單欄位 (`item_name`, `mileage_at_service`, `interval_mileage`, `cost`, `service_date`, `notes`)。
  - **處理邏輯**：呼叫 `MaintenanceRecord.create()`。
  - **輸出**：重導向至 `/garage/<v_id>/maintenance/`。
- **`GET /maintenance/<m_id>/edit`**
  - **輸出**：渲染 `maintenance/form.html`。
- **`POST /maintenance/<m_id>/edit`**
  - **處理邏輯**：呼叫 `MaintenanceRecord.update()`。
  - **輸出**：重導向至該筆紀錄所屬車輛的 `/garage/<v_id>/maintenance/`。
- **`POST /maintenance/<m_id>/delete`**
  - **處理邏輯**：呼叫 `MaintenanceRecord.delete()`。
  - **輸出**：重導向回對應的保養列表頁。

### 2.4 願望清單 (Wishlist Blueprint)

- **`GET /wishlist/`**
  - **輸出**：渲染 `wishlist/index.html`。
- **`GET/POST /wishlist/add`**
  - **輸出**：渲染 `wishlist/form.html` 或 接收 POST 後呼叫 `WishlistItem.create()` 並重導向。
- **`GET/POST /wishlist/<w_id>/edit`**
  - **輸出**：渲染 `wishlist/form.html` 或 接收 POST 後呼叫 `WishlistItem.update()` 並重導向。
- **`POST /wishlist/<w_id>/toggle`**
  - **處理邏輯**：讀取目前狀態，反轉後呼叫 `WishlistItem.toggle_status()`。
  - **輸出**：重導向至 `/wishlist/`。
- **`POST /wishlist/<w_id>/delete`**
  - **處理邏輯**：呼叫 `WishlistItem.delete()`。
  - **輸出**：重導向至 `/wishlist/`。

---

## 3. Jinja2 模板清單

所有 HTML 檔案皆放於 `app/templates/` 目錄中：

- `base.html` (根模板，包含共用 Navbar 與 CSS/JS 引用)
- `dashboard/`
  - `index.html` (繼承 base.html，顯示近期保養提醒)
- `garage/`
  - `index.html` (繼承 base.html，顯示車輛列表)
  - `form.html` (繼承 base.html，新增與編輯共用表單)
- `maintenance/`
  - `index.html` (繼承 base.html，顯示某車輛的所有保養紀錄)
  - `form.html` (繼承 base.html，新增與編輯共用表單)
- `wishlist/`
  - `index.html` (繼承 base.html，顯示願望清單)
  - `form.html` (繼承 base.html，新增與編輯共用表單)
