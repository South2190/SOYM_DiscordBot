# 各種ライブラリのインポート
import discord
import twitter

import yaml
import os
from datetime import datetime
from logging import getLogger, config

# トークンデータの読み込み
import OAuthData

# 前処理
title = 'SOYM_DiscordBot version1.0.5.211110'
os.system('title ' + title)
client = discord.Client()
#hideRT = 'RT @{aName}:'.format(aName = OAuthData.twitter_name)

# ロガーの準備
LOG = getLogger(__name__)
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(os.getcwd())

# フォルダが存在しない場合作成する
if os.path.isdir('logdump') == False:
	os.mkdir('logdump')

# 古いログファイルが見つかった場合は名前を変更する
ofilename = 'logdump/logger.log'
if os.path.isfile(ofilename):
	i = 0
	flag = True
	while(flag):
		lfilename = 'logdump/logger_{num}.log'.format(num = i)
		flag = os.path.isfile(lfilename)
		i += 1
	os.rename(ofilename, lfilename)

config.dictConfig(yaml.load(open('log_config.yaml').read(), Loader=yaml.SafeLoader))

LOG.info(title)
LOG.info('--------------- START LOGGING ---------------')

# 起動時に動作する処理
@client.event
async def on_ready():
	# 起動したらチャンネルにログイン通知を送信
	login_channel = client.get_channel(OAuthData.discord_channel)
	#s_msg = await login_channel.send('起動しました')
	LOG.info('ログインしました')

	# 10秒待った後に起動通知メッセージを削除
	os.system('timeout 11')
	#await s_msg.delete()

	# Twitterからツイートを取得
	oauth = twitter.OAuth(OAuthData.access_token, OAuthData.access_token_secret, OAuthData.consumer_key, OAuthData.consumer_secret)
	twitter_api = twitter.Twitter(auth=oauth)

	stream = twitter.TwitterStream(auth=oauth, secure=True)

	while(True):
		try:
			# 特定ユーザーのツイートをリアルタイムで受信
			LOG.info('ツイートの受信を開始します')
			for tweet in stream.statuses.filter(follow = OAuthData.twitter_account_id):
				# ツイートを出力
				tl = '({time} tweetID:{id}) [@{username}]:{text}\n'.format(time=datetime.now().strftime("%Y/%m/%d %H:%M:%S"), id = tweet['id'], username = tweet['user']['screen_name'], text = tweet['text'])
				print(tl)

				# 新曲追加に関するツイートの抽出
				if all(
					# ツイート元が@ongeki_officialの場合
					[tweet['user']['screen_name'] == OAuthData.twitter_name,
					# いずれかのワードが含まれていた場合
					any(
						[('追加' in tweet['text'] and ('新曲' in tweet['text'] or '楽曲' in tweet['text'])),
						'一挙公開' in tweet['text'],
						'LUNATIC' in tweet['text']]
					),
					# リツイートでない場合
					'RT @' not in tweet['text']]
				):
					LOG.debug(tl)
					LOG.info("ツイートが見つかりました")
					url = 'https://twitter.com/{user}/status/{tweetid}'.format(user = tweet['user']['screen_name'], tweetid = tweet['id'])
					await login_channel.send(url)

				"""
				# ツイートに「exit」のワードが含まれていた場合
				if 'exit' in tweet['text']:
					exit()
				"""

		# 原因不明のKeyErrorはログを吐かせて無視する
		except KeyError as ke:
			print(ke)
			LOG.warning("KeyErrorを無視しました")

		except Exception as e:
			LOG.error(e)

# Botの起動とDiscordサーバーへの接続
client.run(OAuthData.discord_token)

if __name__ != '__main__':
	exit()