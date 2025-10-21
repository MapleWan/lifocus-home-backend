# 快速运行

使用`python3.12.11`运行成功，理论上 `python3.10.x`以上都可以运行成功

1. 修改`.env`文件中对应的数据库连接相关参数，`SECRET_KEY`可以考虑不修改
2. `pip install -r requirements.txt`
3. `rm -rf migrations`
4. `flask db init`
5. `flask db migrate -m 'init'`
6. `flask db upgrade`

# LiFocus 简介
