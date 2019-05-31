# docker コマンド

## 起動

| コマンド | 説明 | 参考URL |
| ---- | ---- |
| docker run -it IMAGE /bin/bash|IMAGEで/bin/bashを使用する| [docker run](https://docs.docker.com/engine/reference/commandline/run/) |
| docker exec -it CONTAINER /bin/bash |CONTAINERで/bin/bashを使用する| [docker exec](https://docs.docker.com/engine/reference/commandline/exec/) |

## 起動確認／停止／削除

| コマンド | 説明 | 参考URL |
| ---- | ---- |
| docker ps    |現在動作しているContainerを表示する| [docker ps](https://docs.docker.com/engine/reference/commandline/ps/) |
| docker stop  |現在動作しているContainerを停止する| [docker stop](https://docs.docker.com/engine/reference/commandline/stop/) |
| docker ps -a |停止したContainerを表示する| [docker ps](https://docs.docker.com/engine/reference/commandline/ps/) |
| docker rm CONTAINER |停止したCONTAINERを削除する| [docker rm](https://docs.docker.com/engine/reference/commandline/rm/) |
| docker images |ローカルにあるIMAGEを表示する| [docker images](https://docs.docker.com/engine/reference/commandline/images/) |
| docker rmi IMAGE |使用していないIMAGEを削除する| [docker rmi](https://docs.docker.com/engine/reference/commandline/rmi/) |

