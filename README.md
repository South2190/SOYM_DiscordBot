# SOYM_DiscordBot

[![](https://img.shields.io/github/v/release/South2190/SOYM_DiscordBot)](https://github.com/South2190/SOYM_DiscordBot/releases)

身内用Discordサーバー専用Bot。

こちらのBotはWindows向けに開発しているため、他の環境だと動作しません。暇があればLinux、Macにも対応したいとは思ってますがいつになるか分かりません。

## 機能・用途

- Twitterのオンゲキ公式アカウント([@ongeki_official](https://twitter.com/ongeki_official))からのツイートをリアルタイムで取得し、新曲追加に関するツイートのURLをDiscordの特定チャンネルに送信します。

## 使い方
以下のものを準備し、同梱の`BotSettings.py`に書き込んでください。

- TwitterのBotとAPI、アクセストークン等
- DiscordのWebhook URL
- アイコンに使用したい画像のURL

`BOT_START.bat`をダブルクリックで実行してください。
起動時、PythonまたはBotの動作に必要なライブラリをインストールするよう求められた場合は画面の指示に従ってインストールしてください。インストールしないとBotが動きません。

## ツイートの抽出条件
基本的には一つのツイートの本文に含まれているワードにて判定を行っています。

- `追加`というワードが含まれていた際、`新曲`もしくは`楽曲`、`LUNATIC`というワードも同時に含まれていた場合
- `一挙公開`というワードが含まれていた場合
- `追加曲公開`というワードが含まれていた場合

## 既知のバグ等

- 過去にオンゲキ公式アカウントからツイートされたことのある新曲追加ツイートにて、現状のコードだと抽出が不可能なツイートが存在する。

## 今後実装予定の機能または変更点
こちらに記載されているもの以外でも、要望があったものの中で実現可能なものは実装します。

- コマンド操作機能。コマンドを入力することでBotの設定を操作したりすることができるようにする「予定」。あくまで「予定」。
- ini形式のBotの設定ファイルの追加

## 更新履歴
- [changelog.md](https://github.com/South2190/SOYM_DiscordBot/blob/master/changelog.md)
