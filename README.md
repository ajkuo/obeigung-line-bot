# obeigung-line-bot

抓取 Mobile01 相機討論群組的熱門文章內的開箱文，並藉由 LINE Message API 傳送給指定對象。

**config.py** - 設定 LINE Message API 相關資訊。
**m01.py** - 抓取指定版面有出現關鍵字的文章，並傳送給指定對象。
**data/history_post.json** - 紀錄抓取過的文章編號，以避免重複抓取。
**data/notify_list.json** - 紀錄要傳送訊息對象的 User ID。
其中兩個 json 檔案的格式皆為： ["123", "456"]


參考資料

[1] https://github.com/LukeHong/ps4-sale-notification
