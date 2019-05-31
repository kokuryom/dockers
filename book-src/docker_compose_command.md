# docker-compose コマンド

## 起動/停止

| コマンド | 説明 | 参考URL |
| ---- | ---- | ---- |
| docker-compose up -d|docker-compose.ymlのあるフォルダで起動する| [docker-compose up](https://docs.docker.com/compose/reference/up/) |
| docker-compose down|docker-compose.ymlのあるフォルダで停止する| [docker-compose down](https://docs.docker.com/compose/reference/down/) |
| docker-compose up|docker-compose.ymlのあるフォルダで起動し、Containerのstdoutを表示する| [docker-compose up](https://docs.docker.com/compose/reference/up/) |
| Ctrl-C | docker-compose upで起動したContainerを停止する| |

## ログ確認

| コマンド | 説明 | 参考URL |
| ---- | ---- |
| docker-compose logs|docker-compose.ymlのあるフォルダでdetachされたstdoutに接続する| [docker-compose logs](https://docs.docker.com/compose/reference/up/) |
| Ctrl-C | docker-compose logsを停止する| |

