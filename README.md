# moremoresns
# OverView　"moremoresns"

"moremoresns"はSNSの投稿をサポートするアプリです。
投稿したいけど何を投稿したらいいかわからない問題を解決します。

<!-- [Go to app](https://xxx) -->
<!-- から使用することができます。 -->
# DEMO
<!-- ![screenshot](/readme_images/xxx.png) -->
# Features
簡単な質問に答えることで自動で投稿が生成され、すぐに投稿できます。
定期的に質問は届きます。
# Installation :balloon:
環境設定には`docker`を使用します。`git`によって環境をコピーし、`docker`によって起動できます。
```bash
git clone git@github.com:na0ki-y/docker_first.git
cd docker-python/
docker compose up -d --build
```

接続は以下で行います。または、VScodeで接続できます。

```bash
docker compose exec サービス名 bash
docker exec -it コンテナ名 /bin/bash
```

シークレットファイルがあります。
```bash
cd /opt/server/
mkdir secrets
cd secrets
touch secrets.json
```
中身の形式は以下です。
```secrets.json
{
    "Line":{
        "Channel_id":"1111",
        "Channel_access_token":"xxxxx",
        "Channel_secret": "xxxxxx"
    }
}
```

docker環境内で以下のコマンドを実行するとサーバーが起動します。
```bash
cd /root/opt/server
pipenv shell
uvicorn run:app
```

# Author
na_0ki
