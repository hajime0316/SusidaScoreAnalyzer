# SusidaScoreAnalyzer

## インストール方法

git cloneでソースコードを取得すればよい．

```git
git clone git@github.com:hajime0316/SusidaScoreAnalyzer.git
```

以降，クローン時に作成さたフォルダ (`SusidaScoreAnalyzer`フォルダ) をプロジェクトフォルダと呼ぶ．

## 使い方

### 1. secretsファイルを用意する

プロジェクトフォルダにsecretsフォルダを作成し，そこに`secrets.json`というファイルを作成する．
`secrets.json`の中身は以下の通り．

```json
{
    "BEARER_TOKEN": "Twitter APIのBearer Token"
}
```

### 2. 以下のコマンドを実行する

```txt
python susida_score_analyzer.py <twitter_user_name> <course or price> <type>
```
