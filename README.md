# SOYM_DiscordBot
身内用Discordサーバー専用Bot。~~結構無理矢理なソースコードだけど割としっかり動いてるから見逃してくれ~~

## 機能・用途
- Twitterのオンゲキ公式アカウント([@ongeki_official](https://twitter.com/ongeki_official))からのツイートをリアルタイムで取得し、新曲追加に関するツイートのURLをDiscordの特定チャンネルに送信する。

## ツイートの抽出条件
基本的には一つのツイートの本文に含まれているワードにて判定を行っている。
- 「追加」というワードが含まれていた際、「新曲」もしくは「楽曲」というワードも同時に含まれていた場合。
- 「一挙公開」というワードが含まれていた場合。
- 「LUNATIC」というワードが含まれていた場合。

## 既知のバグ等
- 過去にオンゲキ公式アカウントからツイートされたことのある新曲追加ツイートにて、現状のコードだと抽出が不可能なツイートが存在する。

## 今後実装予定の機能
こちらに記載されているもの以外でも、要望があったものの中で実現可能なものは実装する。
- コマンド操作機能。コマンドを入力することでBotの設定を操作したりすることができるようにする「予定」。あくまで「予定」。

## 変更履歴
RC版などの細かなマイナーバージョンについては記載しない。
- v1.0.0
  - 初版
