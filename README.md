# Discord Auto Role

![Python](https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python&logoColor=white)
![discord.py](https://img.shields.io/badge/discord.py-2.4%2B-5865F2?logo=discord&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

在新成員加入 Discord 伺服器時，自動指派指定身分組的 Python 機器人。

## Features

- 使用 `.env` 管理機器人 Token 與角色設定
- 支援以角色 `ID` 或角色 `名稱` 指派身分組
- 可選擇限制只在單一 guild/server 生效
- 採用 `commands.Bot` + `setup_hook()` + Cog 的現代結構
- 內建設定驗證與啟動日誌

## Project Structure

```text
.
├─ src/discord_auto_role/
│  ├─ __main__.py
│  ├─ bot.py
│  ├─ config.py
│  ├─ logging_config.py
│  ├─ role_selector.py
│  └─ cogs/auto_role.py
├─ tests/
├─ .env.example
└─ pyproject.toml
```

## Requirements

- Python 3.11+
- 啟用 Discord Developer Portal 中的 `Server Members Intent`
- 已將機器人加入目標 Discord 伺服器

## Quick Start

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

## Environment Variables

| Name | Required | Description |
| --- | --- | --- |
| `DISCORD_BOT_TOKEN` | Yes | Discord Bot Token |
| `DISCORD_GUILD_ID` | No | 限制僅在指定 guild 進行自動派發 |
| `DISCORD_ROLE_ID` | Recommended | 目標身分組 ID |
| `DISCORD_ROLE_NAME` | Optional fallback | 目標身分組名稱 |

建議優先使用 `DISCORD_ROLE_ID`，因為角色名稱可能重複或後續被修改。

## Development

執行單元測試：

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

語法檢查：

```bash
python -m compileall src tests
```

## Notes

- `.env` 已加入 `.gitignore`，不會被推送到 GitHub
- 如果角色找不到，機器人會記錄 warning，不會直接崩潰
- 若需要延伸歡迎訊息、slash commands 或更多事件，可在 `cogs/` 中新增模組
