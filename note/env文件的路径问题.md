太好了！你已经验证了：

✅ `.env` 文件存在  
✅ `config.py` 能正确读取 `DATABASE_URL=postgresql+asyncpg://...`  
✅ 手动运行 `config.py` 输出了正确的数据库 URL

但 **启动主程序时仍然报错**：
```
Field required [type=missing, input_value={}, input_type=dict]
```

这说明：**当你运行 `main.py` 时，`.env` 没有被加载成功**。

---

### 🔍 根本原因：**工作目录（Working Directory）不同**

你手动测试时运行的是：
```bash
uv run .../config.py
```
→ 此时 Python 的 **当前工作目录** 很可能是 `/home/nikofox/fastapi_learnv2`，所以 `../.env` 能找到。

但你启动应用时运行的是：
```bash
uv run .../main.py
```
而 `main.py` 在 **项目根目录**，它导入 `src.app`，而 `src/config.py` 中的 `env_file='../.env'` 是 **相对于 config.py 的路径**，理论上是对的。

**但是！** Pydantic Settings 的 `env_file` 是 **相对于当前工作目录** 还是 **相对于文件位置**？

> 📌 **答案**：`env_file` 是 **相对于当前工作目录（os.getcwd()）** 的，**不是**相对于 `config.py` 文件的位置！

这是很多人踩的坑！

---

### ✅ 验证方法

在 `config.py` 顶部加一行：

```python
import os
print("当前工作目录:", os.getcwd())
```

然后分别运行：
```bash
# 测试 config
uv run src/config.py

# 启动主程序
uv run main.py
```

你会发现：
- 运行 `config.py` 时，工作目录是 `fastapi_learnv2`
- 运行 `main.py` 时，**工作目录可能也是 `fastapi_learnv2`**，但 `env_file='../.env'` 就变成了找 `fastapi_learnv2/../.env` → 即 `/home/nikofox/.env` ❌

等等！这里有个关键点：

你的 `config.py` 写的是：
```python
env_file='../.env'
```

而 `config.py` 位于：
```
/home/nikofox/fastapi_learnv2/src/config.py
```

所以 `../.env` 相对于 **config.py 文件位置** 是：
```
/home/nikofox/fastapi_learnv2/.env ✅
```

但 **Pydantic 并不按文件位置解析 `env_file`**！它按 **进程的当前工作目录** 解析。

所以如果你在 `/home/nikofox/fastapi_learnv2` 目录下运行 `main.py`，那么：
- `env_file='../.env'` → 会去找 `/home/nikofox/.env` ❌（上一级目录）

但你的 `.env` 其实在 `/home/nikofox/fastapi_learnv2/.env` ✅

---

### ✅ 正确解决方案：使用 **绝对路径**

修改 `src/config.py` 如下：

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# 获取 .env 文件的绝对路径：与 src 同级
BASE_DIR = Path(__file__).resolve().parent.parent  # -> /home/nikofox/fastapi_learnv2
ENV_FILE = BASE_DIR / ".env"

print(f"加载 .env 文件: {ENV_FILE}")  # 调试用，上线可删

class Settings(BaseSettings):
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,      # 👈 使用绝对路径
        extra='ignore'
    )

Config = Settings()
```

这样无论你在哪个目录运行 `main.py`，都能准确定位 `.env`。

---

### 🔧 补充建议

1. **确保你是在项目根目录运行命令**（推荐）：
   ```bash
   cd /home/nikofox/fastapi_learnv2
   uv run main.py
   ```

2. **不要用 `uv run .../main.py` 带完整路径**，容易导致工作目录混乱。直接 `cd` 进去再运行。

3. **确认 `.env` 文件权限**：
   ```bash
   ls -l /home/nikofox/fastapi_learnv2/.env
   ```
   确保当前用户有读权限。

---

### ✅ 最终验证

修改 `config.py` 为绝对路径后，运行：

```bash
cd /home/nikofox/fastapi_learnv2
uv run main.py
```

应该就能正常启动了！

如果还有问题，请贴出：
- 修改后的 `config.py`
- 你运行 `main.py` 的完整命令和所在目录（`pwd`）

我会继续帮你排查 💪