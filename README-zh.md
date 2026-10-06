# Discord Auto Role

[![Release](https://img.shields.io/github/v/release/KageRyo/discord-auto-role)](https://github.com/KageRyo/discord-auto-role/releases/latest)
[![Tests](https://github.com/KageRyo/discord-auto-role/actions/workflows/tests.yml/badge.svg)](https://github.com/KageRyo/discord-auto-role/actions/workflows/tests.yml)
![Python](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2FKageRyo%2Fdiscord-auto-role%2Fmain%2Fpyproject.toml&logo=python&logoColor=white)
![discord.py](https://img.shields.io/badge/discord.py-2.7%2B-5865F2?logo=discord&logoColor=white)
[![License](https://img.shields.io/github/license/KageRyo/discord-auto-role)](LICENSE)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-FE5196?logo=conventionalcommits&logoColor=white)](https://www.conventionalcommits.org/en/v1.0.0/)
[![Last commit](https://img.shields.io/github/last-commit/KageRyo/discord-auto-role)](https://github.com/KageRyo/discord-auto-role/commits/main)

**在新成員加入 Discord 伺服器時，自動指派指定身分組的 Python 機器人。**

[English](README.md)

## 功能

- 使用 `.env` 管理機器人 Token 與身分組設定
- 支援以身分組 `ID` 或 `名稱` 指定目標身分組
- 可選擇只在單一伺服器（guild）生效
- 略過機器人帳號，其他 bot 加入時不會被指派身分組
- 支援成員審核（Membership Screening／Onboarding）：待審核的成員會在完成驗證後才取得身分組
- 指派前會先檢查機器人的 `Manage Roles` 權限與身分組階層，無法指派時記錄明確的警告而不是直接出錯
- 提供 `/autorole` 斜線指令（僅限具備 `Manage Roles` 權限的管理員），可檢查設定以及身分組是否能被指派
- 只請求需要的 gateway intents（`guilds` + `members`）
- 採用 `commands.Bot`、`setup_hook()`、Cog 與 app commands 的現代架構

## 專案結構

```text
.
├─ src/discord_auto_role/
│  ├─ __main__.py
│  ├─ bot.py
│  ├─ command_sync.py
│  ├─ config.py
│  ├─ logging_config.py
│  ├─ role_selector.py
│  └─ cogs/auto_role.py
├─ tests/
├─ .env.example
└─ pyproject.toml
```

## 需求

- Python 3.11+
- 一個已建立 bot 使用者的 Discord 應用程式
- 機器人的最高身分組必須**高於**要指派的身分組

## Discord 設定

1. 前往 [Discord Developer Portal](https://discord.com/developers/applications) 建立應用程式，並在 **Bot** 頁面複製 bot token。
2. 在同一頁的 *Privileged Gateway Intents* 中啟用 **Server Members Intent**。沒有啟用的話，機器人收不到成員加入事件。
3. 以 `bot` 與 `applications.commands` 兩個 scope，加上 `Manage Roles` 權限邀請機器人。請把 `YOUR_APPLICATION_ID` 換成 **General Information** 頁面上的應用程式 ID：

   ```text
   https://discord.com/oauth2/authorize?client_id=YOUR_APPLICATION_ID&scope=bot+applications.commands&permissions=268435456
   ```

4. 在 **伺服器設定 → 身分組** 中，把機器人的身分組拖到要指派的身分組上方。Discord 不允許機器人指派等於或高於自己最高身分組的身分組。
5. 在 Discord 開啟 **開發者模式**（*使用者設定 → 進階*），就能在伺服器與身分組上按右鍵複製 ID，填入 `.env`。

機器人啟動後，在伺服器中執行 `/autorole`，確認顯示 **Ready to assign** 即完成設定。

## 快速開始

1. 建立虛擬環境並安裝依賴：

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```

2. 複製環境變數範本：

   ```bash
   cp .env.example .env
   ```

3. 編輯 `.env`：

   ```dotenv
   DISCORD_BOT_TOKEN=your-bot-token
   DISCORD_GUILD_ID=123456789012345678
   DISCORD_ROLE_ID=987654321098765432
   DISCORD_ROLE_NAME=
   ```

4. 啟動機器人：

   ```bash
   python -m discord_auto_role
   ```

## 環境變數

| 名稱 | 必填 | 說明 |
| --- | --- | --- |
| `DISCORD_BOT_TOKEN` | 是 | Discord bot token |
| `DISCORD_GUILD_ID` | 否 | 只在這個伺服器自動指派身分組；斜線指令也會立即同步到這個伺服器 |
| `DISCORD_ROLE_ID` | 建議 | 要指派的身分組 ID |
| `DISCORD_ROLE_NAME` | 備用 | 要指派的身分組名稱 |

建議優先使用 `DISCORD_ROLE_ID`，因為身分組名稱可能重複或之後被修改。

## 斜線指令

| 指令 | 可使用者 | 說明 |
| --- | --- | --- |
| `/autorole` | 具備 `Manage Roles` 權限的成員 | 顯示目標身分組，以及機器人是否能指派它（僅自己可見） |

設定 `DISCORD_GUILD_ID` 時，指令會註冊到該伺服器並立即出現；未設定時則註冊為全域指令，可能需要一段時間才會出現。

啟動時，機器人會把自己的指令和 Discord 上已註冊的指令比對，只有在名稱、描述或預設權限不同時才會同步，因此平常重啟不會觸發指令的速率限制。開啟或關閉 `DISCORD_GUILD_ID` 時，也會清除前一種模式留下的指令，避免同一個指令出現兩次。

## 開發

執行單元測試：

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

語法檢查：

```bash
python -m compileall src tests
```

每次 push 到 `main` 以及每個 pull request，GitHub Actions 都會在 Python 3.11、3.12、3.13 上執行以上檢查。

## 疑難排解

| 狀況 | 原因與解法 |
| --- | --- |
| 新成員一直沒拿到身分組 | 到 Developer Portal 啟用 **Server Members Intent**，然後重新啟動機器人 |
| 日誌顯示 `the bot is missing the Manage Roles permission` | 給機器人的身分組 `Manage Roles` 權限，或用上面的網址重新邀請 |
| 日誌顯示身分組 `is not below the bot's highest role` | 在 **伺服器設定 → 身分組** 中把機器人的身分組移到目標身分組上方 |
| 日誌顯示 `Role not found` | 檢查 `.env` 中的 `DISCORD_ROLE_ID`／`DISCORD_ROLE_NAME` 與 `DISCORD_GUILD_ID` |
| 看不到 `/autorole` | 用包含 `applications.commands` scope 的網址重新邀請；未設定 `DISCORD_GUILD_ID` 時，全域指令可能需要一段時間才會出現 |
| 有開成員審核的伺服器，成員較晚拿到身分組 | 正常行為：成員完成審核（Membership Screening／Onboarding）後才會指派 |

## 注意事項

- `.env` 已列在 `.gitignore` 中，不會被推送到 GitHub。請勿提交任何 bot token。
- 找不到或無法指派身分組時，機器人會記錄警告而不會崩潰
- 若要加入歡迎訊息、更多斜線指令或其他事件，可在 `cogs/` 中新增模組

## 版本紀錄

所有版本請見 [CHANGELOG.md](CHANGELOG.md)，發行說明請見 [GitHub Releases](https://github.com/KageRyo/discord-auto-role/releases)。

## 參與貢獻

歡迎回報問題、改善文件或提交 pull request。開 PR 前請先閱讀 [CONTRIBUTING.md](CONTRIBUTING.md)。感謝 [CONTRIBUTORS.md](CONTRIBUTORS.md) 中的每一位貢獻者。

## 授權

Discord Auto Role 以 [MIT License](LICENSE) 授權釋出。

Copyright © 2022–2026 **Chien-Hsun Chang** 與 [貢獻者們](CONTRIBUTORS.md)。
