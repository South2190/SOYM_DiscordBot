# ///////////////////////////////////////////////////////////////
#
#				！警告！
#
#		この実行ファイルは書き換えないでください。
#
# ///////////////////////////////////////////////////////////////

# 各種ライブラリのインポート
#import configparser
import os
import sys
import tkinter as tk
import tkinter.simpledialog as simpledialog
from datetime import datetime
from json import load
from logging import getLogger, config
from tkinter import messagebox

title = 'SOYM_DiscordBot version1.1.0.211214'

# ライブラリをインストールするかどうかをユーザーに確認し、インストールする
def AskInstall():
	AskMsg = '{leng}つのライブラリがインストールされていません。インストールしますか?'.format(leng = len(InstallLib))
	Slt = messagebox.askyesno(title, AskMsg)

	if Slt:
		for LibName in InstallLib:
			LOGt = 'ライブラリ"{LName}"をインストールしています'.format(LName = LibName)
			LOG.info(LOGt)
			command = 'pip install {LName}'.format(LName = LibName)
			os.system(command)

	else:
		messagebox.showerror(title, "Botの動作にはライブラリをインストールする必要があります。Botを終了します。")
		exit()

# OAuthData.pyにアクセストークンが定義されているかどうかを確認する
# 定義されていない項目がある場合、Botを終了する
def CheckData():
	flag = True

	if(not OAuthData.consumer_key or len(OAuthData.consumer_key) <= 0):
		LOG.critical('"OAuthData.consumer_key"が定義されていません')
		flag = False

	if(not OAuthData.consumer_secret or len(OAuthData.consumer_secret) <= 0):
		LOG.critical('"OAuthData.consumer_secret"が定義されていません')
		flag = False

	if(not OAuthData.access_token or len(OAuthData.access_token) <= 0):
		LOG.critical('"OAuthData.access_token"が定義されていません')
		flag = False

	if(not OAuthData.access_token_secret or len(OAuthData.access_token_secret) <= 0):
		LOG.critical('"OAuthData.access_token_secret"が定義されていません')
		flag = False

	if(not OAuthData.discord_token or len(OAuthData.discord_token) <= 0):
		LOG.critical('"OAuthData.discord_token"が定義されていません')
		flag = False

	if(not OAuthData.discord_channel):
		LOG.critical('"OAuthData.discord_channel"が定義されていません')
		flag = False

	if(not OAuthData.twitter_account_id):
		LOG.critical('"OAuthData.twitter_account_id"が定義されていません')
		flag = False

	if(not OAuthData.twitter_name or len(OAuthData.twitter_name) <= 0):
		LOG.critical('"OAuthData.twitter_name"が定義されていません')
		flag = False

	if not flag:
		LOG.info('Botを終了します')
		messagebox.showerror(title, "\"OAuthData.py\"に記述されていない項目があります。詳細はログを確認してください。\nBotを終了します。")
		exit()

# ログファイルの操作
def Ready_logfile():
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

# 前処理
os.system('title ' + title)
print("Botを起動しています . . .")
root = tk.Tk()
root.withdraw()

# ロガーの準備
Ready_logfile()

if os.path.isfile('LogConfig.json'):
	with open("LogConfig.json", "r", encoding = "utf-8") as f:
		config.dictConfig(load(f))
else:
	messagebox.showwarning(title, "\"LogConfig.json\"が見つかりませんでした。Botの実行は継続されますが、ログはファイルに出力されません。")

LOG = getLogger(__name__)
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(os.getcwd())

LOG.info(title)
LOG.info('--------------- START LOGGING ---------------')

# トークンデータの読み込み
try:
	import OAuthData
except ModuleNotFoundError as e:
	LOG.critical(e)
	messagebox.showerror(title, "\"OAuthData.py\"が見つかりません。Botを終了します。")
	exit()

# discord.pyとtwitterライブラリのインポート
InstallLib = list()

try:
	import discord
except ModuleNotFoundError as e:
	LOG.critical(e)
	InstallLib.append('discord.py')

try:
	import twitter
except ModuleNotFoundError as e:
	LOG.critical(e)
	InstallLib.append('twitter')

# ライブラリを一つでもインストールした場合再起動する
if len(InstallLib) > 0:
	AskInstall()
	os.system('start BOT_START.bat')
	exit()

CheckData()

client = discord.Client()

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
					LOG.info('ツイートが見つかりました')
					url = 'https://twitter.com/{user}/status/{tweetid}'.format(user = tweet['user']['screen_name'], tweetid = tweet['id'])
					await login_channel.send(url)

		# 原因不明のKeyErrorはログを吐かせて無視する
		except KeyError as ke:
			print(ke)
			LOG.warning('KeyErrorを無視しました')

		except Exception as e:
			LOG.error(e)

# Botの起動とDiscordサーバーへの接続
client.run(OAuthData.discord_token)

if __name__ != '__main__':
	exit()