# 基本コマンド

## docker コマンド

### 起動

| コマンド | 説明 | 参考URL |
| ---- | ---- |
| docker run -it IMAGE /bin/bash|IMAGEで/bin/bashを使用する| [run](https://docs.docker.com/engine/reference/commandline/run/) |
| docker exec -it CONTAINER /bin/bash |CONTAINERで/bin/bashを使用する| [exec](https://docs.docker.com/engine/reference/commandline/exec/) |

### 起動確認／停止／削除

| コマンド | 説明 | 参考URL |
| ---- | ---- |
| docker ps    |現在動作しているContainerを表示する| [ps](https://docs.docker.com/engine/reference/commandline/ps/) |
| docker stop  |現在動作しているContainerを停止する| [stop](https://docs.docker.com/engine/reference/commandline/stop/) |
| docker ps -a |停止したContainerを表示する| [ps](https://docs.docker.com/engine/reference/commandline/ps/) |
| docker rm CONTAINER |停止したCONTAINERを削除する| [rm](https://docs.docker.com/engine/reference/commandline/rm/) |
| docker images |ローカルにあるIMAGEを表示する| [images](https://docs.docker.com/engine/reference/commandline/images/) |
| docker rmi IMAGE |使用していないIMAGEを削除する| [rmi](https://docs.docker.com/engine/reference/commandline/rmi/) |

## docker-compose コマンド

### 起動/停止

| コマンド | 説明 | 参考URL |
| ---- | ---- | ---- |
| docker-compose up -d|docker-compose.ymlのあるフォルダで起動する| [up](https://docs.docker.com/compose/reference/up/) |
| docker-compose down|docker-compose.ymlのあるフォルダで停止する| [down](https://docs.docker.com/compose/reference/down/) |
| docker-compose up|docker-compose.ymlのあるフォルダで起動し、Containerのstdoutを表示する| [up](https://docs.docker.com/compose/reference/up/) |
| Ctrl-C | docker-compose upで起動したContainerを停止する| |

### ログ確認

| コマンド | 説明 | 参考URL |
| ---- | ---- |
| docker-compose logs -f|docker-compose.ymlのあるフォルダでdetachされたstdoutに接続する| [logs](https://docs.docker.com/compose/reference/up/) |
| Ctrl-C | docker-compose logs -fを停止する| |

