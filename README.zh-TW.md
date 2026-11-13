<div align="center">

# readme-showcase

**把專案 README 做成陌生人幾秒內就看懂的產品介紹頁。**

給 Claude Code、Codex 與其他支援 `SKILL.md` 的 agent 用的 skill。

[安裝](#安裝) · [使用](#使用) · [內容](#內容) · [限制](#限制) · [English](README.md)

</div>

多數訪客在第一個畫面就決定要不要往下看。這個 skill 讓你的 agent 先想清楚訪客五秒內該看懂什麼，再依專案挑一種合適的 README 風格，錄製真實的示範與截圖，重整 README，最後檢查成果。

它從專案「能誠實展示什麼」出發，不套固定範本。CLI、瀏覽器擴充、桌面程式和函式庫各有不同的呈現方式。需要真人才能完成的素材，例如權限提示或帶聲音的錄影，它會給你一份拍攝清單，不會造假。

```mermaid
flowchart LR
  A[讀專案<br/>找出能展示的畫面] --> B[決定訪客<br/>該看懂的那張圖]
  B --> C[從 10 種風格<br/>挑一種]
  C --> D[錄製真實素材<br/>或寫拍攝清單]
  D --> E[重整<br/>README]
  E --> F[檢查連結、大小、<br/>替代文字、首屏]
```

## 安裝

skill 就是這個倉庫裡的 `readme-showcase/` 資料夾，複製到你的 agent 讀取 skill 的位置即可。

**Claude Code**

```bash
cp -r readme-showcase ~/.claude/skills/
```

**Codex**（CLI、IDE 擴充、App）

```bash
cp -r readme-showcase ~/.agents/skills/
```

Windows PowerShell 可用 `Copy-Item -Recurse readme-showcase $HOME\.claude\skills\` 或 `$HOME\.agents\skills\`。

要讓團隊共用，改放進專案的 `.claude/skills/`（Claude Code）或 `.agents/skills/`（Codex）。

## 使用

當你要求介紹、展示或改善一個倉庫，或要為 README 做示範 GIF、主視覺、截圖、架構圖時，它會自動觸發。也可以直接叫名字：

| Agent | 指令 |
|---|---|
| Claude Code | `/readme-showcase` |
| Codex | `$readme-showcase`，或從 `/skills` 選 |

範例需求：

- 「我的 README 只有文字，幫我做成像高星專案那樣。」
- 「幫這個 CLI 錄一個示範 GIF，放在 README 最上面。」
- 「加一張架構圖和簡短的快速開始。」

在產出任何耗工的東西之前，它會先告訴你計畫：用哪種風格、主視覺是什麼、哪些素材它自己能錄、哪些需要你。

## 內容

```text
readme-showcase/
├── SKILL.md                       六步流程與界線
├── references/
│   ├── readme-patterns.md         10 種 README 風格、選擇方法、GitHub 可用的 HTML
│   └── media-recipes.md           各種介面的錄製做法、拍攝清單範本
└── scripts/
    └── check_readme_assets.py     檢查圖檔、連結、大小與首屏
```

**10 種風格**來自對 24 個熱門倉庫 README 的閱讀：

| 風格 | 開頭放什麼 |
|---|---|
| 示範動畫開場 | 一段無聲短循環，產品正在做它的主要工作 |
| 影片開場 | 可播放的短片，容得下聲音或較長流程 |
| 截圖開場 | 一張真實截圖，接粗體開頭的功能與簡短安裝 |
| 每個功能配一張圖 | 每個功能標題下面有自己的截圖與圖說 |
| 以程式碼示範 | 可直接複製的指令或十行以內的範例 |
| 表格為主 | 功能或下載依平台對照的表格 |
| 數據為主 | 實測數字、圖表或論文 |
| 案例為主 | 具體列出用它做出了什麼 |
| 只留指引 | logo、一句話、連到官網 |
| 參考手冊 | 目錄加上每個選項一節 |

風格可以混搭，好的 README 通常是一種開場風格加一種內文風格。`readme-patterns.md` 說明如何依專案特徵（而不是技術棧）來選。

**檢查腳本**是純標準函式庫的 Python：

```bash
python readme-showcase/scripts/check_readme_assets.py README.md
```

它會回報找不到的本地檔案與失效的相對連結（錯誤），以及缺替代文字的圖、過大的媒體、倉庫內的影片檔、首屏沒有圖（警告）。`--self-test` 會跑內建測試。

## 限制

- **實驗階段。** 還沒有拿「用了這個 skill 做的 README」和「沒用的」做過對照。
- **媒體工具要另外安裝。** 做法用到 [VHS](https://github.com/charmbracelet/vhs)、[Playwright](https://playwright.dev)、`ffmpeg` 和 Mermaid。skill 會先確認工具在不在，不在就告訴你安裝指令。
- **有些素材需要你。** 瀏覽器分頁擷取、麥克風權限、登入後的畫面，無法誠實地用腳本產生。你會拿到拍攝清單，錄好後由 agent 裁切、壓縮。
- **它不會對外發布。** 只在本地修改 README 與新增檔案。commit、push、修改倉庫 About 與發佈 release 都要等你同意。
- **Codex 的路徑**依據 [OpenAI 的 skills 文件](https://learn.chatgpt.com/docs/build-skills)，之後可能變動。

## 授權

[MIT](LICENSE)
