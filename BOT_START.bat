@echo off

rem ///////////////////////////////////////////////////////////////
rem
rem 				！警告！
rem
rem 		この実行ファイルは書き換えないでください。
rem
rem ///////////////////////////////////////////////////////////////

title SOYM_DiscordBot Launcher

python --version

if not '%ERRORLEVEL%'=='0' (
 cls
 goto ASK_PYINSTALL
)

:MAIN
 cd %~dp0

 if exist main.py (
  python main.py
  goto EXIT
 ) else (
  goto ERROR
 )

:ASK_PYINSTALL
 set Slt=nul
 set /p Slt=Pythonがインストールされていないようです。インストールしますか?(y/n)^>

 if '%Slt%'=='y' goto PYINSTALL
 if '%Slt%'=='n' goto ERROR2

 goto ASK_PYINSTALL

:PYINSTALL
 start python
 mshta vbscript:execute("msgbox""Pythonをインストール後、再度ランチャーを実行してください。"",64,""SOYM_DiscordBot Launcher"":close")
 goto EXIT

:ERROR
 mshta vbscript:execute("msgbox""実行ファイル""""main.py""""が見つからないためBotを起動できません。"",16,""SOYM_DiscordBot Launcher"":close")
 goto EXIT

:ERROR2
 mshta vbscript:execute("msgbox""Botを利用するにはPythonをインストールする必要があります。ランチャーを終了します。"",16,""SOYM_DiscordBot Launcher"":close")
 goto EXIT