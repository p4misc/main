# Helix Coreの調査用ファイル格納用リポジトリ

Docker関連のファイルは `docker` ディレクトリに格納しています。

## Dockerを単独で動作させる場合:
- `docker/docker-p4d-run.sh`を実行するとサンプルディポ付きのマスターサーバのコンテナを作成することができます。
- `docker/docker-p4p-run.sh`を実行するとマスターサーバに従属するプロキシサーバのコンテナを作成することができます。

## Docker Composeで動作させる場合:
- `docker/compose-p4d-run.sh`を実行すると以下のことが行われます。
  - Docker Networkとして `helix-core-network` が作成される。
  - サンプルディポ付きのマスターサーバのコンテナが作成される。
  - マスターサーバに従属するプロキシサーバのコンテナが作成される。
