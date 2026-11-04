# iOS 臺灣繁體中文化：字串目錄已補齊（App 全面驗證尚未完成）

## 版本基準

- Fork main：898d8ed746b1bfdeb26a4c2d24484844241ed990。
- 官方 bagumamartin/BitChord v1.0.4：b4aae80294cb80a5994c95ba486eb68d80d13b21；官方發行說明的 iOS 安裝檔為 BitChord-1.0.4-build13-ios-unsigned.ipa。
- main 比標籤多 3 個提交，差異僅 README.md、appcast.xml、美術資產；AppleApp 無差異。project.yml 確認版本 1.0.4、build 13。
- 沿用 main 作為 PR 基底，沒有回退功能或更新版號。

## 根本原因

1. 原有 Localizable.xcstrings 共 704 個鍵，zh-Hant 僅 133 個（18.89%），未提供 zh-TW。
2. App Language 選單的 Chinese 固定寫入 zh-Hans，沒有台灣繁體選項。
3. SettingsLine、SettingsSubToggle 與音質選項用 Text(String) 顯示動態字串，繞過 SwiftUI 本地化查找。即使新增翻譯也不會生效。
4. 許多設定文案不在字串目錄；部分 String(localized:) 使用 Bundle 的語言，未必跟隨 App 內的 locale。這部分尚未統一。

## 本次修改與覆蓋率

- 新增 zh-TW，並將已整理的臺灣用語同步至 zh-Hant，讓系統使用繁體語系時也能取得同樣翻譯。
- 新增台灣繁體語言選項，保留原有 Chinese（簡體）選項。
- 修正共用設定元件、音質選擇頁及音訊設定頁的動態標題、說明查找。保留值、ID、持久化與所有操作邏輯。
- 已覆蓋 762 / 762 個目錄項目（100%；含保留的品牌、網址、格式參數與符號）。新增 58 個原本未列入目錄的設定鍵。原有 704 個鍵已全部覆蓋（100%）。這是字串目錄覆蓋率，**不是整個 App 的中文化完成率**。
- 英文與其他非繁體語言內容逐項比較，完全保留。
- 227 個 Swift 檔案均經靜態字串掃描，包含設定、播放器、歌詞、音效、登入、下載與錯誤相關來源。掃描得到 5613 個未分類、未列入目錄的含英文字母字串出現處，分布於 195 個檔案；其中也包含 API、識別碼、日誌、測試文字與插值，不能當成 UI 缺漏數量。
- 可執行 python3 AppleApp/scripts/audit-localization.py 產生完整 AppleApp/localization-audit.json（逐檔、逐行盤點）。此生成檔不提交。

## 修改檔案

- AppleApp/Resources/Localization/Localizable.xcstrings
- AppleApp/project.yml
- AppleApp/Sources/UI/Settings/SettingsRows.swift
- AppleApp/Sources/UI/Settings/SettingsPages.swift
- AppleApp/Sources/UI/Settings/AudioSettingsPageView.swift
- AppleApp/Sources/UI/Settings/SettingsView+About.swift
- AppleApp/scripts/audit-localization.py
- AppleApp/LOCALIZATION-ZH-TW.md（本報告）
- .github/workflows/ios-zh-tw.yml（分支推送時建置未簽署 IPA，僅上傳 artifact，不發布 release）

## 檢查結果

- PASS：JSON 解析、所有 zh-TW 翻譯的格式化參數數量／型別／位置檢查，zh-TW 與 zh-Hant 回退內容一致。
- PASS：英文及其他非繁體語言的既有內容不變。
- PASS：git diff --check；所有來源修改均在 UI 顯示層。未改動音訊引擎、播放邏輯、Google 登入流程或網路 API。
- 未測試：Swift 編譯、XcodeGen 專案生成、iOS Simulator／裝置測試、SwiftLint；Linux 環境沒有 swift、xcodebuild、xcodegen、swiftlint、plutil，也缺少完整二進位依賴。沒有要求簽署憑證，沒有建立發行版。
- 未測試：中文實際截斷、Dynamic Type、橫向與 iPad 排版、VoiceOver、App 語言切換後所有畫面即時刷新，以及離線錯誤流程。

## 風險與第二階段必要工作

1. 剩餘 130 個目錄項目已完成：105 個補上中文，25 個品牌、網址、格式參數及符號保留；仍需人工複審既有沿用的繁體翻譯。
2. 依 audit JSON 逐一區分 UI 文案與程式識別碼，將所有 UI 文案接入目錄；動態插值應改成可本地化格式句，不能單純將執行期字串視為鍵。
3. 專門盤點 toast、錯誤、診斷、音效狀態、歌詞分享、AppIntents、Widget、UIKit 與系統權限提示。Widget 需獨立確認資源目錄包裝；InfoPlist 使用目的字串尚未本地化。
4. 統一本地化 helper 對 App 內選擇語言的處理，驗證 zh-TW → zh-Hant → 英文回退。現階段缺漏鍵仍會出現英文，不宣稱回退已實機驗證。
5. 設定搜尋目前保留英文關鍵詞；需加入繁體搜尋詞，確認翻譯後設定也能搜尋。
6. 在 macOS/Xcode 具備依賴的環境進行不簽署的 iOS Simulator 編譯，接著驗證小螢幕、最大字體與橫向。共用設定說明原有 fixedSize 支援換行，但沒有實機證據可保證不截斷。
7. 執行播放、佇列、下載、Google 登入回歸測試。此 PR 應維持草稿，完成以上項目後再評估合併；不直接合併 main。


## IPA 建置

新增分支自動觸發的 GitHub Actions，使用原有 scripts/package-ios-ipa.sh，以 CODE_SIGNING_ALLOWED=NO 建置。成功時上傳未簽署 IPA、SHA256.txt 與診斷盤點。工作流程會檢查 IPA 是否含 zh-TW.lproj/Localizable.strings。實際建置狀態以 Actions 記錄為準；沒有產物前不宣稱編譯成功或 IPA 已可下載。
