## Docker Commands

コンテナをバックグラウンドで起動する。

```bash
docker compose up -d
```

起動中のコンテナでコマンドを実行する。

```bash
docker compose exec <service_name> <command>
```

uvの仮想環境でコマンドを実行する。

```bash
uv run --no-sync <command>
```

一時的な `test` コンテナを作成してテストを実行する。終了後はコンテナを削除する。

```bash
docker compose run --rm test
```

コンテナを停止・削除する。volumeは残る。

```bash
docker compose down
```

コンテナとvolumeを削除する。DBデータも削除される。

```bash
docker compose down -v
```
