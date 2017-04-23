# songci

A [SongCi](https://en.wikipedia.org/wiki/Ci_(poetry)) generator base on emblems shuffling and [Genetic algorithms](https://en.wikipedia.org/wiki/Genetic_algorithm).

## Overview
The project is a [SongCi](https://en.wikipedia.org/wiki/Ci_(poetry)) generator. Which basically does these things:

* Analyse SongCi contents using natural language processing techniques
* Generate naive SongCi artifacts based on specified tune patterns
* Optimize the generated artifacts using genetic algorithms, until certain criteria is met

## Requirements

* Python 3.6+
* Mongodb
* (Optional) Docker && Docker-compose

## Usage

You may choose one of the following methods to run this project.

Using Docker with sc_spider is the recommended way.

### Docker with sc_spider

1. Install Docker && Docker-compose.
1. Clone and run project [sc_spider](https://github.com/wings27/sc_spider) using Docker, sc_spider will start up two containers: mongodb and the spider itself.
2. When the spider stops, the mongodb will still be running, listening for our connections, so we can run this project now (maybe you have to open a new shell):

```bash
docker-compose up
```

### Docker

1. Install Docker && Docker-compose.
2. Install MongoDB (This project uses an existing host MongoDB, it doesn't provide a MongoDB docker image out-of-the-box)
2. (Optional) Run `docker-compose build` in case of environment updates.
3. (Optional) Modify `MONGO_URI` settings in `app.conf`.
4. Run the project:

```bash
docker-compose up
```

### Command Line (python)

1. Install MongoDB
2. Install project requirements: `pip install -r requirements.txt`
3. (Optional) Modify `MONGO_URI` settings in `app.conf`.
4. Run the project:

```bash
python run.py [analyse] [write]
```

Note: Arguments for phases can be any combinations of the following verbs:

- **analyse**: run the *analyse phase* where the nlp data are generated from songci contents and then stored to db
- **write**: run the *write phase* where new songci artifacts are written

Typically, you may want to run `python run.py analyse write` for first-time use, since you don't have the required nlp data yet.
And run `python run.py analyse` each time the original songci contents in db have been updated, in order to keep the nlp data up-to-date.
Run `python run.py write` to write songci artifacts based on the nlp data in db.

If no arguments for phases are provided, the phases will default to "analyze write"


## Features

* Very fast NLP analysis powered by an optimized parallel (multi-processing) map-reduce driver
* MongoDAO optimized for batch operations
* Brief and efficient tune patterns representations
* Customizable arguments for different phases

## Selected works

(Randomly) selected works with tune name "《浣溪沙》":

>《浣溪沙· 曼舞如丝倚画阑》
>
>曼舞如丝倚画阑，玉人歌对问平安。远山绕水夜春寒。
>分水行征湖上路，关渠转运客江南。床空恨夜也应难。

>《浣溪沙· 环碧边幽花褪残》
>
>环碧边幽花褪残，园香雨态锦衾寒。重关万转水锵然。
>柳外取嬉风淡淡，游行时坐列仙班。天疏灯半数声蝉。

>《浣溪沙· 白浪重重脚踏沧》
>
>白浪重重脚踏沧，迟春门闭少年郎。人销迢去步回廊。
>向我摧天清彻骨，伤情水冷恼人肠。河西流去梦高唐。

>《浣溪沙· 天下置之独倚阑》
>
>天下置之独倚阑，昏风四角玉笙寒。聚八尊酒问江南。
>晓枕迷归窗睡起，暗将微步上阑干。时才曲径雨斑斑。

## Releases

You can download the latest stable releases from: https://github.com/wings27/songci/releases

## Contributing

All contributions are welcomed.

However, please follow these conventions:

* Your coding style should follow [PEP 8](https://www.python.org/dev/peps/pep-0008)
