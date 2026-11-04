# iOS 臺灣繁體中文化：第一階段（尚未完成）

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
- 已翻譯 632 / 762 個目錄項目（82.94%）。新增 58 個原本未列入目錄的設定鍵。原有 704 個鍵中覆蓋 574 個（81.53%）。這是字串目錄覆蓋率，**不是整個 App 的中文化完成率**。
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

## 檢查結果

- PASS：JSON 解析、所有 zh-TW 翻譯的格式化參數數量／型別／位置檢查，zh-TW 與 zh-Hant 回退內容一致。
- PASS：英文及其他非繁體語言的既有內容不變。
- PASS：git diff --check；所有來源修改均在 UI 顯示層。未改動音訊引擎、播放邏輯、Google 登入流程或網路 API。
- 未測試：Swift 編譯、XcodeGen 專案生成、iOS Simulator／裝置測試、SwiftLint；Linux 環境沒有 swift、xcodebuild、xcodegen、swiftlint、plutil，也缺少完整二進位依賴。沒有要求簽署憑證，沒有建立發行版。
- 未測試：中文實際截斷、Dynamic Type、橫向與 iPad 排版、VoiceOver、App 語言切換後所有畫面即時刷新，以及離線錯誤流程。

## 風險與第二階段必要工作

1. 完成下列 130 個目錄項目，人工審閱既有沿用的繁體翻譯；保留品牌、網址與格式字串。
2. 依 audit JSON 逐一區分 UI 文案與程式識別碼，將所有 UI 文案接入目錄；動態插值應改成可本地化格式句，不能單純將執行期字串視為鍵。
3. 專門盤點 toast、錯誤、診斷、音效狀態、歌詞分享、AppIntents、Widget、UIKit 與系統權限提示。Widget 需獨立確認資源目錄包裝；InfoPlist 使用目的字串尚未本地化。
4. 統一本地化 helper 對 App 內選擇語言的處理，驗證 zh-TW → zh-Hant → 英文回退。現階段缺漏鍵仍會出現英文，不宣稱回退已實機驗證。
5. 設定搜尋目前保留英文關鍵詞；需加入繁體搜尋詞，確認翻譯後設定也能搜尋。
6. 在 macOS/Xcode 具備依賴的環境進行不簽署的 iOS Simulator 編譯，接著驗證小螢幕、最大字體與橫向。共用設定說明原有 fixedSize 支援換行，但沒有實機證據可保證不截斷。
7. 執行播放、佇列、下載、Google 登入回歸測試。此 PR 應維持草稿，完成以上項目後再評估合併；不直接合併 main。

## 仍缺少 zh-TW 的目錄鍵（130）

- "1"
- ""
- "%@"
- "%d"
- "%lld"
- "%lld Hz"
- "%lld of %lld tracks matched. Choose the matches to keep. Unmatched tracks stay in the playlist and can be matched later."
- "%lld of %lld tracks · %@"
- "%lld%%"
- "%lld."
- "+%lld"
- "123.5 MB total · Runs 100% on-device · Private"
- "46.7 MB of models · Runs 100% on-device · Private"
- "A library you host yourself, played from the server rather than from a catalogue. It takes no part in the ranking above — it holds your own files, so it is not standing in for anything."
- "A party server is a deployment somebody has to run. This app does not ship one."
- "A version switch resumes where you left off. With this off it restarts from the top, since no alignment is attempted."
- "AirPlay"
- "AirPlay & Bluetooth"
- "Albums group themselves once a folder with tagged music is scanned."
- "Albums you save on YouTube Music show up here — or scan a folder on this device."
- "An API key and shared secret are required to authorise. Don’t share them."
- "Apple’s Headphone Accommodations, Adaptive Audio and Conversation Awareness are managed in system Accessibility, AirPods settings and Control Center. BitChord keeps your manual EQ choices."
- "Artists group themselves once a folder with tagged music is scanned."
- "Artists you follow on YouTube Music show up here — or scan a folder on this device."
- "Auto-hide keeps the still sleeve when no motion clip was found. Prefer Spotify asks Spotify's catalogue first when looking one up."
- "BITCHORD"
- "Beat This! (beat and downbeat detection) and open-unmix UMX-L (vocal detection). Both are verified against a pinned checksum after download."
- "Beat This! (beat and downbeat detection) and open-unmix umxhq (vocal detection). Both are downloaded once and verified against a pinned checksum."
- "Beat This! (beat and downbeat detection, optionally accelerated by Core ML), open-unmix umxhq (vocal detection), and the Core ML compilation of the same Beat This! checkpoint. All are downloaded once and verified against a pinned checksum."
- "Beat model installed with Core ML acceleration; vocal detection can be added for vocal-clash avoidance"
- "Beat model installed; vocal detection can be added for vocal-clash avoidance"
- "Beat, downbeat and vocal models installed, accelerated by Core ML — %@ on disk"
- "BitChord analyzes your tracks on-device to match beats, time crossfades, and prevent vocal clashes between songs."
- "BitChord installs from its releases page, so this opens it in your browser."
- "BitChord watches the folder you choose for music files. Filtering keeps everything that is not a song out of the list."
- "BitChord will still prefer its copy when the match is the same recording. It will not when it is not."
- "Bluetooth"
- "CarPlay"
- "Channels you subscribe to show up here."
- "Compare counter changes while a track plays. The output callback also runs with an empty queue, so idle silent callbacks are expected."
- "Core ML · Neural Engine"
- "DAC"
- "Finds the singing at the start and end of each track so two vocals do not overlap during a transition."
- "Discord"
- "Discord has no API for an app to set your presence, so this signs in as your account and speaks its protocol. Your token is stored on this device and only ever sent to Discord — but it is your whole account, and automating one is against Discord's terms of service. Bans for presence alone aren't a thing anyone reports; it's still your call."
- "Downloaded once and kept in BitChord's storage. Removing a model takes effect immediately: Automix falls back to tempo analysis without the beat model, and stops watching for vocal clashes without the vocal one."
- "Drag the puck: sideways tilts warm ↔ bright, up and down shapes the mids."
- "Everyone in a party has to be pointed at the same server, and it has to be one somebody is running."
- "Exported downloads live in the shared Music folder. Private ones stay inside BitChord's own storage."
- "Follow artists on YouTube Music — or scan a folder on this device."
- "Forgets the address, the account and the password. Nothing on the server is touched."
- "Gapless stays on at 0s. Automix picks timing per track; crossfade sets the manual blend length."
- "GitHub"
- "HDMI"
- "High Performance Mode holds the display at the chosen refresh rate instead of letting the system vary it. Expect noticeably shorter battery life while it is on."
- "Holding a high refresh rate keeps the display working harder the whole time BitChord is open, and the battery drains faster for it. Turn it on anyway?"
- "Import a CSV or TSV playlist export from Spotify or Apple Music, or drop an .m3u file in your music folder."
- "Import a CSV or TSV playlist export from Spotify or Apple Music, save a playlist on YouTube Music, or drop an .m3u file in your music folder."
- "L"
- "Liked playlists, albums and artists live here."
- "Liked playlists, albums and artists you save show up here."
- "Lossless includes Hi-Res when an enabled source supplies it. Audio Pipeline shows the format actually decoded."
- "Match Source Sample Rate asks the route to switch clock families between tracks. Bit-perfect output is available on macOS when the DAC grants exclusive access and the lossless source format is supported. The Audio Pipeline readout shows what is actually in effect."
- "Millions of songs, played properly"
- "Models are downloaded once and verified via SHA-256. Manage anytime in Settings."
- "Models download once · Runs 100% on-device · Private"
- "Narrower shapes around 250 Hz, 1 kHz and 4 kHz."
- "Needed for the PaxSeniX sources. Stored in the Keychain, not in preferences."
- "No downloads yet. Save a track from Now Playing or a collection menu."
- "Non-music segments and audible boundaries are always used by Automix."
- "One **album** you kept coming back to."
- "PCM 16"
- "Paste the sp_dc cookie from an open Spotify web session. BitChord uses it only to look up looping motion art. Leave blank to skip."
- "PaxSeniX Spotify and PaxSeniX Musixmatch reach two catalogues Apple Music does not carry, and both need a key from paxsenix.org. Everything else on this list works without one. Stored in the Keychain, not in preferences."
- "Personalized recommendations and your library, on every device."
- "Pick a folder — BitChord reads its tags, artwork and plays it with gapless and crossfade."
- "Play a few songs and this page will fill in with minutes, top tracks and artists."
- "Play a few songs this year and this page will fill in with minutes, top tracks and artists."
- "Playlists you save show up here."
- "Playlists, albums and artists you save show up here."
- "Plays on this account show up here, newest first."
- "Podcasts you follow show up here."
- "Point BitChord at a WebDAV share in Sources and it will appear here."
- "Preserves the recording. Playback speed, Automix and crossfade keep their own settings."
- "R"
- "Recent technical events stay on this device. Reports exclude credentials and private paths. Audio capture is available separately in Audio Pipeline."
- "Reference clarity adds tonal contour, centered bass and gentle width. Manual EQ and spatial remain optional."
- "Runs the same Beat This! model on the Neural Engine, several times faster than the CPU path. Requires the beat model."
- "Same song in Downloads and on this share. Choose which copy wins."
- "Save a track from Now Playing — BitChord tags it and keeps it here."
- "Save albums on YouTube Music — or scan a folder on this device."
- "Scan a folder to see its songs here too."
- "Seven-band parametric EQ with shelves at both ends. Flat is sample-identical passthrough."
- "Show what you’re playing on your Discord profile, updating as the track does."
- "Songs you add to your YouTube Music library — or a folder you scan on this device."
- "Songs you add to your library show up here."
- "Spotify Canvas"
- "Spotify sp_dc cookie (optional canvas)"
- "Swipe up for Up Next, swipe down to return to the player."
- "Swipe up or down to adjust when the lyrics appear"
- "The same Beat This! model, compiled for the Neural Engine. It falls back to the standard beat model on short tracks or if inference fails."
- "The server answered and there is no audio in it. If you expected a folder here, it may be somewhere else on the share."
- "The system picker routes this app's audio — AirPlay, Bluetooth and the device speaker."
- "There isn't much from this month yet. Play a few songs and it will fill in."
- "There was one **artist** you never got tired of."
- "There was one **genre** you came back to again and again."
- "This download and a track on your WebDAV share name the same song."
- "This invite points at somebody else’s party server, so joining switches this device to it."
- "This is a preference, not a per-track setting — the same lag applies to every track, so it is set once."
- "This is your **Replay** — the year in music you actually played."
- "Tracks you play will show up here."
- "Tried in this order — drag to reorder. The highest-priority source to answer at all wins, unless Prefer Word-Synced Lyrics says to keep looking for a word-synced one."
- "Tried top to bottom. Reorder in Settings → Lyrics → Lyrics Sources."
- "Turn off to give BitChord audio priority. Other apps may pause."
- "Turn on to keep other apps audible."
- "Vocal model installed — without the beat model Automix falls back to tempo analysis"
- "WebDAV"
- "When on, a merely line-synced answer waits for a word-synced one further down the list."
- "Wider shapes with a richer sound."
- "You got through **%lld songs** by **%lld artists**."
- "You played **%lld songs**, one was your anthem."
- "YouTube Music"
- "https://cloud.example.com/dav"
- "https://your-server.com"
- "https://…"
- "open-unmix reads how much singing is in each moment, so Automix can keep two vocals from overlapping."
- "open-unmix umxhq"
- "sp_dc cookie"
- "{song_name}, {artist_name} and {album_name} are replaced with the track. The first button opens the song on YouTube Music, the second this project."
- "•"
