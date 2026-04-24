# Commit Skill

此 Skill 允許 AI Agent 自動執行 git add、git commit 以及 git push 指令。

## 使用方式
當使用者輸入 `/commit <commit訊息>` 時，請執行以下動作：
1. git add .
2. git commit -m "<使用者提供的訊息>"
3. git push