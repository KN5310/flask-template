# Dockerfile
# ベースイメージ
FROM python:3.7-slim

# 作業ディレクトリ
WORKDIR /app

# PHP 8.3 (Surýリポジトリ経由) + Apache + Python をインストール
RUN apt-get update && \
    apt-get install -y lsb-release ca-certificates apt-transport-https software-properties-common gnupg2 wget && \
    echo "deb https://packages.sury.org/php $(lsb_release -sc) main" > /etc/apt/sources.list.d/php.list && \
    wget -qO - https://packages.sury.org/php/apt.gpg | apt-key add - && \
    apt-get update && \
    apt-get install -y apache2 apache2-utils libapache2-mod-fcgid \
                       python3 python3-pip php8.3-cli && \
    rm -rf /var/lib/apt/lists/*

# PHP バージョン確認（デバッグ用）
RUN php -v

# docker/requirements.txt をコンテナ内 /app にコピー
COPY docker/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# プロジェクト一式をコピー
COPY . .

# Apache CGI 有効化
RUN a2enmod cgid rewrite

# CGI スクリプトに実行権限を付与
RUN chmod +x /app/index.cgi

# CGI 用ログフォルダ作成 & 書き込み権限付与
RUN mkdir -p /app/log/log_202509 && \
    chown -R www-data:www-data /app/log && \
    chmod -R 775 /app/log

#  Dockerfile と同じ docker/ 内にある apache.conf を使用
COPY docker/apache.conf /etc/apache2/sites-available/000-default.conf

# グローバル設定に ServerName を追加（警告回避）
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

# Apache が起動したらフォアグラウンドで動作
EXPOSE 80
CMD ["apache2ctl", "-D", "FOREGROUND"]