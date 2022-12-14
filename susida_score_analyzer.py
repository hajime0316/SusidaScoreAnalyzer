import tweepy
import json
import re
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
import sys
import matplotlib.dates as mdates
import numpy as np


# クライアント関数を作成
def ClientInfo():
    script_dir = Path(__file__).resolve().parent
    if (script_dir / "secrets" / "secrets.json").exists():
        secrets_file_path = script_dir / "secrets" / "secrets.json"
    elif (script_dir / "secrets.json").exists():
        secrets_file_path = script_dir / "secrets.json"
    else:
        raise Exception("'secrets.json' was not found.")

    with secrets_file_path.open() as f:
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
def SearchTweets(user_name):

    # tweepy Client初期化
    client = ClientInfo()

    # User IDの取得
    user_data = client.get_user(username=user_name)

    # User IDが取得できない（無効なユーザー名）の場合に例外を投げる
    if len(user_data.errors) != 0:
        raise Exception("Invalid user name")

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
    if len(sys.argv) < 4:
        print("Usage: python susida_score_analyzer.py <twitter_user_name> <price> <game_type>")
        sys.exit(1)

    user_name = sys.argv[1]

    # <price>は最初文字列としてチェックした後数値に変換
    prices = ["3000", "5000", "10000"]
    price = sys.argv[2]
    if price not in prices:
        print("Error: Invalid input value <price>")
        print(f"Possible values for the argument <price>: {', '.join(prices)}")
        sys.exit(1)
    price = int(price)  # priceを数値に変換

    game_type = sys.argv[3]
    game_types = ["練習", "普通", "正確重視", "速度必須", "一発勝負"]
    if game_type not in game_types:
        print("Error: Invalid input value <game_type>")
        print(f"Possible values for the argument <game_type>: {', '.join(game_types)}")
        sys.exit(1)

    # 関数実行・出力
    results = SearchTweets(user_name)
    with open("tweets.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    timestamps = []
    scores = []
    speeds = []
    mistakes = []

    for r in results:
        text = r["text"]

        # 寿司打ツイートかどうかを判定

        if text.find(f"{'{:,}'.format(price)}円コース【{game_type}】で、") == -1 or text.find("#寿司打") == -1:
            continue

        p1 = re.compile(r"★(0|[1-9]\d*|[1-9]\d{0,2}(?:,\d{3})+)円分 お得でした！（速度：(\d+\.\d+)key/秒、ミス：(\d+)key）")
        # p1_data = ["gain", "speed", "mistake"]
        p2 = re.compile(r"（スコア：(0|[1-9]\d*|[1-9]\d{0,2}(?:,\d{3})+)円、速度：(\d+\.\d+)key/秒、ミス：(\d+)key）")
        # p2_data = ["score", "speed", "mistake"]
        p3 = re.compile(r"(0|[1-9]\d*|[1-9]\d{0,2}(?:,\d{3})+)円分 損でした…（速度：(\d+\.\d+)key/秒、ミス：(\d+)key）")

        m1 = p1.search(text)
        m2 = p2.search(text)
        m3 = p3.search(text)

        if m1:
            score = int(m1.group(1).replace(",", "")) + price
            speed = float(m1.group(2))
            mistake = int(m1.group(3))
        elif m2:
            score = int(m2.group(1).replace(",", ""))
            speed = float(m2.group(2))
            mistake = int(m2.group(3))
        elif m3:
            score = price - int(m3.group(1).replace(",", ""))
            speed = float(m3.group(2))
            mistake = int(m3.group(3))
        else:
            continue

        print(score, speed, mistake)

        timestamp = datetime.strptime(r["created_at"], "%Y-%m-%d %H:%M:%S")
        print(timestamp)
        timestamps.append(timestamp)
        scores.append(score)
        speeds.append(speed)
        mistakes.append(mistake)

    # 単純グラフの作成
    fig_1 = plt.figure("単純グラフ")
    fig_1_ax1 = fig_1.add_subplot(2, 1, 1)
    fig_1_ax1.plot(timestamps, scores, color=(244 / 255, 127 / 255, 17 / 255, 0.5),
                   marker=".", linewidth=1, label="Score")
    fig_1_ax1.legend()

    # タイピング速度をプロットする
    fig_1_ax2 = fig_1.add_subplot(2, 1, 2)
    fig_1_ax2.plot(timestamps, speeds, color=(117 / 255, 47 / 255, 8 / 255, 0.5),
                   marker=".", linewidth=1, label="Typing speed")
    fig_1_ax2.legend()

    # 時間軸ラベルの設定
    locator = mdates.AutoDateLocator(minticks=3, maxticks=5)
    fig_1_ax1.xaxis.set_major_locator(locator)
    fig_1_ax2.xaxis.set_major_locator(locator)

    fig_1.savefig(f"単純グラフ_{user_name}_{price}円_{game_type}.png")

    # 平均グラフの作成
    fig_2 = plt.figure("平均グラフ")
    fig_2_ax = fig_2.add_subplot()

    # 平均の計算
    SECTION_NUM = 10
    section_scores = [[] for i in range(SECTION_NUM)]
    section_speeds = [[] for i in range(SECTION_NUM)]
    start_timestamp = min(timestamps)
    end_timestamp = max(timestamps)
    duration = end_timestamp - start_timestamp

    dt = duration / SECTION_NUM

    for i in range(len(timestamps)):
        flag = False
        for section_i in range(SECTION_NUM):
            if (start_timestamp + dt * section_i <= timestamps[i] and timestamps[i] < start_timestamp + dt * (section_i + 1)):
                section_scores[section_i].append(scores[i])
                section_speeds[section_i].append(speeds[i])
                flag = True
                break

        if not flag:
            section_scores[-1].append(scores[i])
            section_speeds[-1].append(speeds[i])

    mean_scores = []
    mean_speeds = []
    for section_i in range(SECTION_NUM):
        mean_scores.append(np.mean(section_scores[section_i]))
        mean_speeds.append(np.mean(section_speeds[section_i]))

    print(mean_scores)
    print(mean_speeds)

    mean_timestamps = [start_timestamp + dt * (i + 0.5) for i in range(SECTION_NUM)]

    print(mean_timestamps)

    # スコアのプロット
    fig_2_ax.bar(mean_timestamps, [x - price for x in mean_scores], bottom=price,
                 color="#f7a95b", width=dt / 2, align="center", label="Score")
    fig_2_ax.legend(bbox_to_anchor=(0.0, 1.0), loc="lower left")

    # 基準線をプロット
    fig_2_ax.axhline(price, color='black', lw=1)

    # タイピング速度をプロット
    twin_ax = fig_2_ax.twinx()
    twin_ax.plot(mean_timestamps, mean_speeds, color="#752f09", marker=".", linewidth=1, label="Typing speed")
    twin_ax.legend(bbox_to_anchor=(1.0, 1.0), loc="lower right")

    # 時間軸ラベルの設定
    locator = mdates.AutoDateLocator(minticks=3, maxticks=5)
    twin_ax.xaxis.set_major_locator(locator)

    fig_2.savefig(f"平均グラフ_{user_name}_{price}円_{game_type}.png")

    plt.show()


if __name__ == "__main__":
    main()
