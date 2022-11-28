# SusidaScoreAnalyzer

タイピングゲームの「寿司打」のスコアを可視化するPythonスクリプト．
Twitterの寿司打ツイートから寿司打のデータを取得しグラフ化する．

## 実行環境

- Python 3.9.6
- tweepy 4.10.1
- matplotlib 3.6.1
- numpy 1.23.3

## インストール方法

### 1. ソースコードのclone

git cloneでソースコードを取得する．

```git
git clone git@github.com:hajime0316/SusidaScoreAnalyzer.git
```

以降，クローン時に作成さたフォルダ (`SusidaScoreAnalyzer`フォルダ) をプロジェクトフォルダと呼ぶ．

### 2. Twitter API利用のためのsecretsファイルを用意する

プロジェクトフォルダ直下に`secrets.json`というファイルを作成する．
`secrets.json`の中身にTwitter APIのBearer Token情報を記述する．
記述方法は以下の通り．

```json
{
    "BEARER_TOKEN": "<Twitter APIのBearer Token>"
}
```

Twitter APIのBearer Tokenは[このWebサイト](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api)から取得できる．

### 3. Pythonの依存パッケージのインストール

pipコマンドで`tweepy`，`matplotlib`，`numpy`をインストールする．

```sh
pip install tweepy matplotlib numpy
```

## 使い方

プロジェクトフォルダで以下のコマンドを実行する．

```txt
python susida_score_analyzer.py <twitter_user_name> <price> <game_type>
```

コマンドの入力（引数）は以下の通り．

| 入力 (引数)           | 説明                                          | 取りうる値                               |
| --------------------- | --------------------------------------------- | ---------------------------------------- |
| `<twitter_user_name>` | 寿司打のスコアを調べる対象のTwitterユーザー名 | Twitterユーザー名 (文字列)               |
| `<price>`             | グラフ化の対象とする寿司打の値段              | 3000, 5000, 10000                        |
| `<game_type>`         | グラフ化の対象とする寿司打のゲーム種別        | 練習, 普通, 正確重視, 速度必須, 一発勝負 |

コマンドを実行すると2種類のグラフが表示される．

| グラフ名   | 概要                                                                                                         |
| ---------- | ------------------------------------------------------------------------------------------------------------ |
| 単純グラフ | 取得した寿司打のスコアとタイピング速度を単純に折れ線グラフにした図                                           |
| 平均グラフ | 期間を区切ってスコアとタイピング速度の平均値を求め，スコアを棒グラフ，タイピング速度を折れ線グラフで表した図 |

表示されているグラフを2つとも閉じるとプログラムが終了する．

## 出力ファイル

| 項目           | ファイル名                                               | 概要                                                                                                         |
| -------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| ツイートデータ | `tweets.json`                                            | Twitterから取得したツイートデータ．                                                                          |
| 単純ファイル   | `単純グラフ_<twitter_user_name>_<price>_<game_type>.png` | 取得した寿司打のスコアとタイピング速度を単純に折れ線グラフにした図                                           |
| 平均グラフ     | `平均グラフ_<twitter_user_name>_<price>_<game_type>.png` | 期間を区切ってスコアとタイピング速度の平均値を求め，スコアを棒グラフ，タイピング速度を折れ線グラフで表した図 |
