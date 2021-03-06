# Docker & Helix Installer

## Helix Installer
https://swarm.workshop.perforce.com/projects/perforce_software-helix-installer/ で公開されています。

レプリカ構成などの複雑な構成も考慮してHelix Core環境を構築することができます。

Helix Installer自体は以下の要領で使用します。
- reset_sdp.shを入手して `/hxdepots/reset` に配置する
- reset_sdp.shに実行権限を付与する
- 設定ファイルの雛形を生成する (`reset_sdp.sh -C > settings.cfg`)
- 生成した設定ファイルの雛形を編集する
- 編集した設定ファイルを使用してHelix Coreのインスタンスを作成する (`reset_sdp.sh -c settings.cfg -fast`)

P4Pythonが必要な場合はインストールスクリプトを実行します。
- perforceユーザでP4Pythonをインストールする (`/hxdepots/sdp/Server/Unix/setup/install_sdp_python.sh`)

インスタンス起動用のスクリプトも生成されます。
- Helix Coreインスタンスを起動する (`/p4/1/bin/p4d_1_init start`)

## コンテナの起動
`docker-compose up -d`でコンテナを起動できます(上記の手順もすべて行います)。

`docker-compose.yml` および 関連する`Dockerfile` では以下のことをすべて行います。
- ubuntu18updイメージの作成
  - Ubuntu 18.04の公式イメージを入手する
  - 公式イメージに不足しているパッケージをインストールする
- helixイメージの作成
  - Helix Installer(`reset_sdp.sh`)を入手する
  - 上述した要領でHelix Coreのインスタンスを作成する
  - P4Pythonをインストールする

## Helix Coreへのアクセス
雛形ファイル(`settings.cfg`)の内容をそのまま使用してHelix Coreインスタンスを構築しているため、以下の設定になっています。
- ユーザ: `perforce`
- パスワード: `F@stSCM!`
- SSL接続: `有効`
- ポート番号: `1999`

このため、`docker-compose up -d` の実行後は、`ssl:IPアドレス:1999` または `ssl:ホスト名:1999` でHelix Coreに接続してください。

## settings.cfgの内容確認
コンテナにログインして `/hxdepots/reset/settings.cfg` の内容を確認するか、
`docker cp helix:/hxdepots/reset/settings.cfg .` を実行してホストにファイルを取得して内容を確認してください。
