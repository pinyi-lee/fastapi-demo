cd app

//初始化環境設置
python3 -m venv venv
source venv/bin/activate
pip3 install --upgrade pip
pip3 install -r ../build/requirements.txt

//進入環境設置
python3 -m venv venv

//開啟專案
uvicorn main:app --reload

//離開環境設置
deactivate