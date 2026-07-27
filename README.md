# 桌遊產業週報

每週彙整國際與台灣桌遊產業動態的靜態網站，設計為 GitHub Pages 一鍵託管。

## 結構

```
index.html                     首頁（讀 reports.json 自動列出所有期數）
reports.json                   期數索引（build 腳本自動維護，勿手改）
reports/<date>.html            每期報告（build 腳本產生）
template/桌遊週報_框架.html      固定版面框架（含渲染邏輯，每週不動）
template/build_site.py         建置腳本
data/週報數據_<date>.json       每期資料（唯一每週需新增的檔）
```

設計原則：**版面框架固定，每週只新增一份 JSON 資料檔**，再跑 build 產生該期 HTML 並更新首頁索引。

## 首次上架（在 Claude Code / 你的電腦上執行一次）

```bash
cd site
git init
git add -A
git commit -m "init: 桌遊產業週報"
git branch -M main
git remote add origin https://github.com/<你的帳號>/<repo>.git
git push -u origin main
```

到 GitHub repo → Settings → Pages → Source 選 `main` 分支、根目錄 `/`，
數分鐘後網站上線於 `https://<你的帳號>.github.io/<repo>/`。

## 每週更新流程

1. 產生當週資料檔 `data/週報數據_YYYY-MM-DD.json`
   （Cowork 的排程任務會自動搜尋新聞並產出這份 JSON；或手動比照現有檔案格式編輯）。
   搜尋時「台灣在地動態」section 除了展會/募資動態外，**務必額外查詢台灣代理商與出版社（如新天鵝堡、大馬、propaganda、小雞等）本週是否有新品上市/新作發售公告**，
   若有則以 `tag:"新品上市"` 標記該張 card（見下方 JSON 格式），讓首頁與報告頁清楚區分出新品上市消息；若查無明確、可信來源的上市消息，就不要硬湊，維持該子類別留白即可。
2. 建置並更新索引：
   ```bash
   python3 template/build_site.py data/週報數據_YYYY-MM-DD.json
   ```
3. 發佈：
   ```bash
   git add -A && git commit -m "週報 YYYY-MM-DD" && git push
   ```

## 全自動（選配）

在你自己的電腦上用系統 cron 每週一呼叫 Claude Code，跑「搜尋 → 產 JSON → build → git push」一條龍，因為本機 git/`gh` 已授權，不需儲存任何權杖。範例 crontab（每週一 09:00）：

```
0 9 * * 1 cd /path/to/site && claude -p "更新本週桌遊週報：搜尋過去七天新聞（含台灣代理商/出版社的新品上市公告），比照 data/ 既有格式產出 data/週報數據_$(date +\%F).json，執行 python3 template/build_site.py 該檔，然後 git add/commit/push" >> ~/boardgame-weekly.log 2>&1
```

## 資料檔 JSON 格式

頂層：`headline`、`range`、`date`(YYYY-MM-DD)、`intro`(可含 HTML)、`summary`(選填，首頁摘要)、`sections[]`、`sources[]`、`footnote`。
每個 section：`num`、`title`、`en`、可選 `tw:true`、可選 `none`、`cards[]`。
每張 card：`title`、`date`、可選 `tag`、`body`(可含 HTML)、可選 `figs[]`({value,label})、可選 `foot`、`sources[]`({name,url})、可選 `tw:true`。

`tag` 為自由文字徽章，用於標記 card 類別（如國際募資區用 `"Kickstarter"`、`"Gamefound"`；台灣區用 `"新品上市"` 標記台灣代理/在地新作發售消息）。
