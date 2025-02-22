# ハッカソン（入門コース） K-team
ハッカソンの入門コースKチームのChatAppです。

**最初に環境変数ファイル（.env）を作成します**
- Mac、Windows(PowerShell、Git Bash)の場合
```
cp .env.example .env
```
- Windows(コマンドプロンプト)の場合
```
copy .env.example .env
```

**起動方法**
```
docker compose up
```

**ブラウザで確認**
```
http://localhost:55000
```


### ディレクトリ構成
```
.
├── ChatApp              # サンプルアプリ用ディレクトリ
│   ├── __init__.py
│   ├── app.py
│   ├── models.py
│   ├── static          # 静的ファイル用ディレクトリ
│   ├── templates       # Template(HTML)用ディレクトリ
│   └── utils
├── Docker
│   ├── Flask
│   │   └── Dockerfile # Flask(Python)用Dockerファイル
│   └── MySQL
│       ├── Dockerfile  # MySQL用Dockerファイル
│       ├── init.sql    # MySQL初期設定ファイル
│       └── my.cnf
├── .env.example         # 環境変数ファイル（.env）を作成する為のサンプルファイル
├── docker-compose.yml   # Docker-composeファイル
└── requirements.txt     # 使用モジュール記述ファイル
```