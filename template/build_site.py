#!/usr/bin/env python3
"""
桌遊週報 — 網站建置腳本
用法： python3 template/build_site.py data/週報數據_YYYY-MM-DD.json
動作：
  1. 讀取當週 JSON，注入固定框架 template/桌遊週報_框架.html
  2. 輸出 reports/<date>.html
  3. 更新 reports.json 索引（首頁 index.html 會讀它自動列出所有期數）
每週只需新增一份 data/週報數據_YYYY-MM-DD.json，再跑一次本腳本即可。
"""
import sys, json, os, re

TPL_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TPL_DIR)
FRAME = os.path.join(TPL_DIR, "桌遊週報_框架.html")
REPORTS_DIR = os.path.join(ROOT, "reports")
MANIFEST = os.path.join(ROOT, "reports.json")


def strip_html(s):
    return re.sub(r"<[^>]+>", "", s or "").strip()


def main():
    if len(sys.argv) < 2:
        print("用法: python3 template/build_site.py data/週報數據_YYYY-MM-DD.json")
        sys.exit(1)
    data_path = sys.argv[1]
    with open(data_path, encoding="utf-8") as f:
        data = json.load(f)

    date = data.get("date")
    if not date:
        print("錯誤：JSON 缺少 date 欄位"); sys.exit(1)

    # 1+2. 建置該期報告
    with open(FRAME, encoding="utf-8") as f:
        html = f.read()
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    out_html = html.replace("__DATA_JSON__", payload)
    os.makedirs(REPORTS_DIR, exist_ok=True)
    report_rel = f"reports/{date}.html"
    with open(os.path.join(ROOT, report_rel), "w", encoding="utf-8") as f:
        f.write(out_html)

    # 3. 更新索引
    manifest = []
    if os.path.exists(MANIFEST):
        with open(MANIFEST, encoding="utf-8") as f:
            manifest = json.load(f)
    manifest = [m for m in manifest if m.get("date") != date]
    manifest.append({
        "date": date,
        "range": data.get("range", ""),
        "headline": data.get("headline", "桌遊產業週報"),
        "summary": data.get("summary") or strip_html(data.get("intro", ""))[:90],
        "file": report_rel,
    })
    manifest.sort(key=lambda m: m.get("date", ""), reverse=True)
    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"已建置 {report_rel} 並更新 reports.json（共 {len(manifest)} 期）")


if __name__ == "__main__":
    main()
