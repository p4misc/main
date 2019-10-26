# Perforce Server Log Analyzer (PSLA)
Helix Coreのログ解析ツールです。

コマンドラインとWeb UIの両方を使用することができます。

Web UIはFlaskベースのWebアプリケーションとして構築されています。

## PSLAの公開元
下記のURLで公開されています。

https://swarm.workshop.perforce.com/projects/perforce-software-log-analyzer

## PSLA構築済みDockerコンテナ
本リポジトリで公開しているDockerfileまたはdocker-compose.ymlを使用すると、Perforce Server Log AnalyzerのWeb UIを稼働させることができます。

次の手順でDockerコンテナを起動できます。
- dockerコマンドで構築する場合の例
  - `docker build -t psla .`
  - `docker run -p 5050:5050 -d -it psla`
- docker-composeコマンドで構築する場合の例
  - `docker-compose up -d`

## PSLA構築済みDockerイメージ on Docker Hub
本リポジトリで公開しているDockerfileを使用して自動ビルドをしたDockerイメージを公開しています。

Docker Hub上のイメージを使用する場合は、次の手順でDockerコンテナを起動できます。
- Docker Hubを利用する場合の例:
  - `docker pull p4misc/psla`
  - `docker run -p 5050:5050 -d -it psla`

## PSLAの使用方法
PSLAのWebアプリケーションは、5050ポートで待ち受けをして稼働するように設定しました。

Webブラウザを使用して http://IPアドレスorホスト名:5050/ でアクセスしてください。
