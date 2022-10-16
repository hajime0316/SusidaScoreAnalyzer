from turtle import color
from unittest import result
import tweepy
from pprint import pprint
import json
import re
import matplotlib.pyplot as plt
from datetime import datetime


# クライアント関数を作成
def ClientInfo():
    with open("secrets/secrets.json", "r") as f:
        secret = json.load(f)
    client = tweepy.Client(
        bearer_token=secret["BEARER_TOKEN"],
        #    consumer_key=API_KEY,
        #    consumer_secret=API_SECRET,
        #    access_token=ACCESS_TOKEN,
        #    access_token_secret=ACCESS_TOKEN_SECRET,
    )
    return client


# 関数
def SearchTweets():

    # tweepy Client初期化
    client = ClientInfo()

    # User IDの取得
    user_data = client.get_user(username="hajime0316_")
    user_id = user_data.data["id"]

    next_token = None
    results = []
    while(True):
        tweets = client.get_users_tweets(user_id, max_results=100,
                                         pagination_token=next_token, tweet_fields="created_at")
        tweets_data = tweets.data
        # tweet検索結果取得
        if tweets_data != None:
            for tweet in tweets_data:
                obj = {}
                obj["tweet_id"] = tweet.id      # Tweet_ID
                obj["text"] = tweet.text  # Tweet Content
                obj["created_at"] = tweet.created_at.strftime('%Y-%m-%d %H:%M:%S')
                print(obj)
                results.append(obj)

        next_token = tweets.meta.get("next_token", None)
        if not next_token: break

    # 結果出力
    return results


def main():
    # 関数実行・出力
    results = SearchTweets()
    with open("test.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    timestamps = []
    scores = []
    speeds = []
    mistakes = []

    for r in results:
        text = r["text"]

        # 寿司打ツイートかどうかを判定
        if text.find("高級10,000円コース【普通】") == -1: continue

        p = re.compile(r"★(0|[1-9]\d*|[1-9]\d{0,2}(?:,\d{3})+)円分 お得でした！（速度：(\d+\.\d+)key/秒、ミス：(\d+)key）")
        # TODO: re.compile(r"（スコア：(0|[1-9]\d*|[1-9]\d{0,2}(?:,\d{3})+)円、速度：(\d+\.\d+)key/秒、ミス：(\d+)key）")
        #       のパターンに対応する

        m = p.search(text)

        if not m: continue  # パターンマッチしない場合はスキップ
        print(m.groups())

        score = int(m.group(1).replace(",", ""))
        speed = float(m.group(2))
        mistake = int(m.group(3))

        print(score, speed, mistake)

        timestamp = datetime.strptime(r["created_at"], "%Y-%m-%d %H:%M:%S")
        print(timestamp)
        timestamps.append(timestamp)
        scores.append(score)
        speeds.append(speed)
        mistakes.append(mistake)

    plt.plot(timestamps, scores, color="blue", linewidth=1, marker=".")
    ax1 = plt.twinx()
    ax1.plot(timestamps, speeds, color=(0.0, 0.0, 0.0, 0.5), linewidth=2)
    ax1.set_xticks([
        datetime(year=2020, month=1, day=1),
        datetime(year=2021, month=1, day=1),
        datetime(year=2022, month=1, day=1),
        datetime(year=2023, month=1, day=1)
    ])
    ax1.set_xticklabels(["2020", "2021", "2022", "2023"])

    plt.show()


if __name__ == "__main__":
    main()
