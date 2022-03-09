# ///////////////////////////////////////////////////////////////
#
#				！警告！
#
#		この実行ファイルは書き換えないでください。
#
# ///////////////////////////////////////////////////////////////

# 各種ライブラリのインポート
#import configparser
import importlib
import json
import os
import requests
import sys
import tkinter as tk
import tkinter.simpledialog as simpledialog
from datetime import datetime
from json import load
from logging import getLogger, config
from pip._internal import main as _main
from tkinter import messagebox

title = 'SOYM_DiscordBot version2.0.0.220309'

# ライブラリのインポートを行う
# ライブラリが存在しない場合インストールを行う
def _import(module, ver=None):
	try:
		globals()['tweepy'] = importlib.import_module(module)
	except ImportError:
		try:
			if ver is None:
				_main(['install', module])
			else:
				_main(['install', '{}=={}'.format(module, ver)])
			globals()['tweepy'] = importlib.import_module(module)
		except:
			LOG.critical("can't import: {}".format(module))
			return False
	return True

# BotSettings.pyにアクセストークンが定義されているかどうかを確認する
# 定義されていない項目がある場合、Botを終了する
def CheckData():
	flag = True

	if(not BotSettings.consumer_key or len(BotSettings.consumer_key) <= 0):
		LOG.critical('"BotSettings.consumer_key"が定義されていません')
		flag = False

	if(not BotSettings.consumer_secret or len(BotSettings.consumer_secret) <= 0):
		LOG.critical('"BotSettings.consumer_secret"が定義されていません')
		flag = False

	if(not BotSettings.access_token or len(BotSettings.access_token) <= 0):
		LOG.critical('"BotSettings.access_token"が定義されていません')
		flag = False

	if(not BotSettings.access_token_secret or len(BotSettings.access_token_secret) <= 0):
		LOG.critical('"BotSettings.access_token_secret"が定義されていません')
		flag = False

	if(not BotSettings.discord_bot_name or len(BotSettings.discord_bot_name) <= 0):
		LOG.critical('"BotSettings.discord_bot_name"が定義されていません')
		flag = False

	if(not BotSettings.webhook_uri or len(BotSettings.webhook_uri) <= 0):
		LOG.critical('"BotSettings.webhook_uri"が定義されていません')
		flag = False

	if(not BotSettings.icon_uri or len(BotSettings.icon_uri) <= 0):
		LOG.critical('"BotSettings.icon_uri"が定義されていません')
		flag = False

	if(not BotSettings.twitter_account_id):
		LOG.critical('"BotSettings.twitter_account_id"が定義されていません')
		flag = False

	if not flag:
		LOG.info('Botを終了します')
		messagebox.showerror(title, "\"BotSettings.py\"に記述されていない項目があります。詳細はログを確認してください。\nBotを終了します。")
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
	messagebox.showwarning(title, "\"LogConfig.json\"が見つかりませんでした。Botの実行は継続されますが、ログは出力されません。")

LOG = getLogger(__name__)
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(os.getcwd())

LOG.info(title)
LOG.info('--------------- START LOGGING ---------------')

# トークンデータの読み込み
try:
	import BotSettings
except ModuleNotFoundError as e:
	LOG.critical(e)
	messagebox.showerror(title, "\"BotSettings.py\"が見つかりません。Botを終了します。")
	exit()

ImportLibResult = _import('tweepy')
if ImportLibResult:
	LOG.info("モジュール\"tweepy\"のインポートに成功しました")
else:
	messagebox.showerror(title, "モジュール\"tweepy\"がインストールできませんでした。Botを終了します。")

#tweepyがリアルタイムでツイートを取得する
class StreamListener(tweepy.Stream):
	# 対象のユーザーが新規にツイートをするたびにこの関数が走る
	def on_status(self, status):
		# ツイートの全文を取得する
		if 'extended_tweet' in status._json:
			text = status._json['extended_tweet']['full_text']
			IsExtended = True
		elif 'extended_tweet' not in status._json:
			text = status.text
			IsExtended = False
			
		tweet_type = self.check_tweet_type(status)

		# リツイートやリプライだった場合は内容を表示し終了(ログには出力しない)
		if tweet_type != 'normal_tweet':
			tl = '({time} tweetID:{id}) [@{username}]:{text}\n'.format(time=datetime.now().strftime("%Y/%m/%d %H:%M:%S"), id = status.id, username = status.user.screen_name, text = text)
			print(tl)
			return

		# ツイートをログに出力する
		tl = '(tweetID:{id}, IsExtended:{ext}) [@{username}]:{text}\n'.format(id = status.id, ext = IsExtended, username = status.user.screen_name, text = text)
		LOG.debug(tl)

		# 新曲通知ツイートかどうかを判定する
		if any(
			['追加' in text and any(
				['新曲' in text,
				'楽曲' in text,
				'LUNATIC' in text]
			),
			'一挙公開' in text,
			'追加曲公開' in text]
		):
			LOG.info('ツイートが見つかりました')
			url = 'https://twitter.com/{user}/status/{tweetid}'.format(user = status.user.screen_name, tweetid = status.id)
			LOG.debug(url)

			main_content = {
				'username': BotSettings.discord_bot_name,
				'avatar_url': BotSettings.icon_uri,
				'content': url
			}
			headers = {'Content-Type': 'application/json'}
			response = requests.post(BotSettings.webhook_uri, json.dumps(main_content), headers=headers)

	def on_error(self, status_code):
		LOG.error(f"status:{status_code}")
		return True

	def on_warning(self, notice):
		LOG.warning(notice.message)
		return

	def on_exception(self, exception):
		LOG.error(exception)
		return

	# ツイートの種類をチェック（リツイート or リプライ or 通常のツイート）
	def check_tweet_type(self, status):
		# JSON内のキーに「retweeted_status」があればリツイート
		if 'retweeted_status' in status._json.keys():
			return 'retweet'

		# 「in_reply_to_user_id」がNoneでなかった場合はリプライ
		elif status.in_reply_to_user_id != None:
			return 'reply'

		# それ以外は通常のツイート
		else:
			return 'normal_tweet'

CheckData()

# Listenerの宣言
twitter_stream = StreamListener(BotSettings.consumer_key, BotSettings.consumer_secret, BotSettings.access_token, BotSettings.access_token_secret)

LOG.info('ツイートの受信を開始します')

# 絞り込み条件で特定ユーザーからのツイートのみ取得
twitter_stream.filter(follow = [BotSettings.twitter_account_id])

if __name__ != '__main__':
	exit()