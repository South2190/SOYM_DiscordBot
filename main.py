# 各種ライブラリのインポート
import discord
import twitter

import yaml
import os
from datetime import datetime
from logging import getLogger, config
#import concurrent.futures
# トークンデータの読み込み
import OAuthData

# 変数の宣言
global oauth
channel_id = OAuthData.discord_channel
account_id = OAuthData.twitter_account_id
focus_account = OAuthData.twitter_name

# 前処理
client = discord.Client()

LOG = getLogger(__name__)
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(os.getcwd())
config.dictConfig(yaml.load(open('log_config.yaml').read(), Loader=yaml.SafeLoader))

# 起動時に動作する処理
@client.event
async def on_ready():
	# 起動したらチャンネルにログイン通知が送信される
	login_channel = client.get_channel(channel_id)
	s_msg = await login_channel.send('起動しました')
	LOG.info('ログインしました')
	# 10秒待った後に起動通知メッセージを削除
	os.system('timeout 11')
	await s_msg.delete()
	# Twitterからツイートを取得
	oauth = twitter.OAuth(OAuthData.access_token, OAuthData.access_token_secret, OAuthData.consumer_key, OAuthData.consumer_secret)
	twitter_api = twitter.Twitter(auth=oauth)

	stream = twitter.TwitterStream(auth=oauth, secure=True)

	while(True):
		try:
			# 特定ユーザーのツイートをリアルタイムで受信
			LOG.info('ツイートの受信を開始します')
			for tweet in stream.statuses.filter(follow = account_id):
				# ツイートを出力
				tl = '({time} tweetID:{id}) [@{username}]:{text}\n'.format(time=datetime.now().strftime("%Y/%m/%d %H:%M:%S"), id = tweet['id'], username = tweet['user']['screen_name'], text = tweet['text'])
				print(tl)

				"""
				print('追加' in tweet['text'])
				print('新曲' in tweet['text'])
				print('楽曲' in tweet['text'])
				print('一挙公開' in tweet['text'])
				print('LUNATIC' in tweet['text'])
				print('追加' in tweet['text'] and ('新曲' in tweet['text'] or '楽曲' in tweet['text']))
				print(any([('追加' in tweet['text'] and ('新曲' in tweet['text'] or '楽曲' in tweet['text'])), '一挙公開' in tweet['text'], 'LUNATIC' in tweet['text']]))
				print(tweet['user']['screen_name'] == focus_account)
				"""

				# ツイートに特定のワードが含まれていた場合
				if any([('追加' in tweet['text'] and ('新曲' in tweet['text'] or '楽曲' in tweet['text'])), '一挙公開' in tweet['text'], 'LUNATIC' in tweet['text']]) and tweet['user']['screen_name'] == focus_account:
					LOG.debug(tl)
					LOG.info("ツイートが見つかりました")
					url = 'https://twitter.com/{user}/status/{tweetid}'.format(user = tweet['user']['screen_name'], tweetid = tweet['id'])
					await login_channel.send(url)

				# ツイートに「exit」のワードが含まれていた場合
				if 'exit' in tweet['text']:
					exit()

		# 原因不明のKeyErrorはログを吐かせて無視する
		except KeyError as ke:
			print(ke)
			LOG.warning("KeyErrorを無視しました")

# Botの起動とDiscordサーバーへの接続
client.run(OAuthData.discord_token)

if __name__ != '__main__':
	exit()