
from app import app
from dotenv import load_dotenv
load_dotenv()  # 加载 .env 文件
if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=10630, debug=True)
    app.run()