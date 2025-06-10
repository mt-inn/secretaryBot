# Python 3.11をベースイメージとして使用
FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# システムパッケージの更新とタイムゾーンの設定
RUN apt-get update && apt-get install -y \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# タイムゾーンを設定（日本時間）
ENV TZ=Asia/Tokyo

# requirements.txtをコピーして依存関係をインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースコードをコピー
COPY src/ .

# ポート番号を環境変数として設定（必要に応じて）
EXPOSE 8000

# Botを起動
CMD ["python", "main.py"]