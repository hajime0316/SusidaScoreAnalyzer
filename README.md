# SusidaScoreAnalyzer

タイピングゲームの「寿司打」のスコアを可視化するPythonスクリプト．
Twitterの寿司打ツイートから寿司打のデータを取得しグラフ化する．

## 実行環境

- Python 3.9.6
- tweepy 4.10.1

## インストール方法

git cloneでソースコードを取得する．

```git
git clone git@github.com:hajime0316/SusidaScoreAnalyzer.git
```

以降，クローン時に作成さたフォルダ (`SusidaScoreAnalyzer`フォルダ) をプロジェクトフォルダと呼ぶ．

## 使い方

### 1. secretsファイルを用意する

プロジェクトフォルダ直下に`secrets.json`というファイルを作成する．
`secrets.json`の中身にTwitter APIを使用するためのBearer Tokenの情報を記述する．
記述方法は以下の通り．

```json
{
    "BEARER_TOKEN": "<Twitter APIのBearer Token>"
}
```

### 2. 以下のコマンドを実行する

```txt
python susida_score_analyzer.py <twitter_user_name> <price> <game_type>
```

上記コマンドを実行すると2種類のグラフが表示される．

1. 単純グラフ: 寿司打のスコアとタイピング速度を単純にプロットしたグラフ
2. 平均グラフ: 期間を区切ってスコアとタイピング速度の平均値を求め，スコアを棒グラフ，タイピング速度を折れ線グラフで表したグラフ

表示されているグラフウィンドウを2つとも閉じるとプログラムが終了する．
