# 各種ライブラリを読み込む
import BotSettings
import json
import requests

while(True):
	message = input('メッセージを入力(exitで終了)>')

	if message == 'exit':
		exit()

	content = {
		'username': BotSettings.discord_bot_name,
		'avatar_url': BotSettings.icon_uri,
		'content': message
	}
	headers = {'Content-Type': 'application/json'}
	response = requests.post(BotSettings.webhook_uri, json.dumps(content), headers=headers)