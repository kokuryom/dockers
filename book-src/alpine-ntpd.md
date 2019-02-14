# NTP Server by Docker

## dockers/alpine-ntpd
* Dockerfile
* docker-compose.yml
* check.sh
* conf
  * ntpd.conf

## Configuration

<div style="float:left;">

| file | role |
| - | - |
| conf/ntpd.conf | 上位NTP Serverを設定します | 

</div><div style="clear: both;"></div>

### conf/ntpd.conf
```
listen on *

server ntp.nict.jp
server ntp.jst.mfeed.ad.jp
```

## 起動
起動後、ロガーを追記モードで起動します。
```
$ docker-compose up -d
$ docker-compose logs -f
```

数分後、clock is now syncedと表示されれば同期成功です
<p style="color: red;">注意： インターネットに接続できないなどの理由で同期できないとNTP Serverとして動作を開始しません。</p>

```
myntpd  | reply from 133.243.238.243: offset -0.000437 delay 0.003680, next query 34s
myntpd  | reply from 210.173.160.57: offset 0.000364 delay 0.003804, next query 33s
myntpd  | clock is now synced
myntpd  | reply from 133.243.238.243: offset -0.000834 delay 0.003595, next query 32s
```

別ターミナルでcheck.shを使用すると動作チェックができます。\* が付いているレコードが同期していることを示します。
```
$ sh check.sh
peer
   wt tl st  next  poll          offset       delay      jitter
133.243.238.243 ntp.nict.jp
    1 10  1    1s   34s        -0.753ms     3.702ms     0.780ms
210.173.160.57 ntp.jst.mfeed.ad.jp
 *  1 10  2   30s   33s         0.074ms     3.283ms     0.393ms
```
