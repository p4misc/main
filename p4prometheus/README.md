# p4prometheus調査用環境
本```docker-compose.yml```を使用すると以下3つのコンテナが稼働します。
- helixcoreコンテナ(Dockerfileで構築)
  - Helix Core : 1666ポート
  - node_exporter : 9100ポート
  - p4prometheus
  - crond
- Prometheusコンテナ(公式のコンテナをそのまま使用)
  - Prometheus : 9090ポート
- Grafanaコンテナ(公式のコンテナをそのまま使用)
  - Grafana : 3000ポート

```docker-compose.yml```内でexternalネットワークを指定しています。
```docker network create -d bridge helix-core-network```で事前にネットワークを作成しておく必要があります。


## Helix Coreのインストールと設定について
公式の手順に沿ってインストールしています。
1. [Linuxパッケージベースのインストール](https://www.toyo.co.jp/files/user/img/product/ss/help/perforce/r19.1/manuals/p4sag/Content/P4SAG/install.linux.packages.install.html)
2. [インストール後の設定](https://www.toyo.co.jp/files/user/img/product/ss/help/perforce/r19.1/manuals/p4sag/Content/P4SAG/install.linux.packages.configure.html)

インストール時の設定とインストール後のディレクトリ構成は以下のとおりです。  
ただし、メトリクスディレクトリはインストールによって作成されるものではなく、p4prometheus用に作成しています。

項目 | 値
--- | ---
superユーザ名 | super
superユーザのパスワード | super123456
Unicodeモード | 有効
大文字小文字の区別 | 区別しない
サーバID | master
Helix Coreのインストールディレクトリ | /opt/perforce
Helix Coreのメタデータディレクトリ(P4ROOT) | /opt/perforce/servers/master/root
Helix Coreのディポディレクトリ | /opt/perforce/servers/master/archives
Helix Coreのログディレクトリ | /opt/perforce/servers/master/logs
Helix Coreのメトリクスディレクトリ | /opt/perforce/servers/master/metrics

※ **superユーザのパスワードは稼働後に変更をしてください**


## node_exporterのインストールと設定について
インストールにあたって特別なことはしていません。
Dockerfile内の ```## Install p4prometheus``` のブロックをご参照ください。

起動時のオプションで **```Helix Coreのメトリクスディレクトリ```** ```/opt/perforce/servers/master/metrics``` のデータを参照するように指示します。


## p4prometheusのインストールと設定について
公式の手順に沿ってインストールしています。
1. [Install p4prometheus - details](https://github.com/rcowham/p4prometheus#install-p4prometheus---details)

起動時のオプションで ```p4prometheus.yml``` を設定ファイルとして与えます。  
この設定ファイルの中で以下の値を設定しています。

項目名 | 目的 | 値
--- | --- | ---
sdp_instance | SDPインスタンスの番号(不要ですがダミー値を指定) | 1
server_id | Helix CoreのサーバID | master
log_path | Helix Coreのログファイルのパス | /opt/perforce/servers/master/logs/log
metrics_output | p4prometheusに出力させるメトリクスファイルのパス | /opt/perforce/servers/master/metrics/p4_cmds.prom


## 使用方法
1. ```docker network create -d bridge helix-core-network```で、externalネットワークを作成します。
2. ```docker-compose build```で、イメージをビルドまたは取得します。
3. ```docker-compose up -d```で、作成または取得したイメージを用いてコンテナを起動します。 
4. Dockerホストマシン上で操作する場合は、```http://localhost:3000```でGrafanaにアクセスします。
5. usernameとpasswordの両方に```admin```と入力します。
6. パスワードを変更するよう促されるので、パスワードを入力します。
7. ```Add data source```をクリックします。
8. ```Prometheus```をクリックします。
9. URLに```http://localhost:9090```、Accessに```Browser```を指定して```Save & Test```をクリックします。
10. ```+```ボタンを押して、```Import```をクリックします。
11. ```Upload .json file```をクリックします。
12. 本リポジトリに登録されている```p4_stats_dashboard.json```を選択します。
13. ```Import```をクリックします。
14. いくつか収集できていないデータがありますが、サンプルのダッシュボードが表示されます。

## 備考
Helix Coreコンテナの状態を調査する場合は、```docker exec -it helixcore /bin/bash```を実行してコンテナにログインしてください。
