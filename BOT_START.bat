@echo off

rem ///////////////////////////////////////////////////////////////
rem
rem 				！警告！
rem
rem 		この実行ファイルは書き換えないでください。
rem
rem ///////////////////////////////////////////////////////////////

title SOYM_DiscordBot Launcher

cd %~dp0

if not exist main.py goto ERROR

python --version

if not '%ERRORLEVEL%'=='0' (
 cls
 goto ASK_PYINSTALL
)

python main.py

goto EXIT

:ASK_PYINSTALL
 powershell -Command "Add-Type -AssemblyName System.Windows.Forms;$result = [System.Windows.Forms.MessageBox]::Show(\"Pythonがインストールされていないようです。インストールしますか?\", 'SOYM_DiscordBot Launcher', 'YesNo', 'Question');exit $result;"

 if '%ERRORLEVEL%'=='6' (
  goto PYINSTALL
 ) else if '%ERRORLEVEL%'=='7' (
  goto ERROR2
 ) else (
  goto ERROR3
 )

:PYINSTALL
 wmic os get caption | findstr "10 11"
 if '%ERRORLEVEL%'=='0' (
  start python
 ) else (
  start https://www.python.org/
 )
 mshta vbscript:execute("msgbox""Pythonをインストール後、再度ランチャーを実行してください。"",64,""SOYM_DiscordBot Launcher"":close")
 goto EXIT

:ERROR
 mshta vbscript:execute("msgbox""実行ファイル""""main.py""""が見つからないためBotを起動できません。"",16,""SOYM_DiscordBot Launcher"":close")
 goto EXIT

:ERROR2
 mshta vbscript:execute("msgbox""Botを利用するにはPythonをインストールする必要があります。ランチャーを終了します。"",16,""SOYM_DiscordBot Launcher"":close")
 goto EXIT

:ERROR3
 mshta vbscript:execute("msgbox""このコンピューターはBotの動作要件を満たしていません。"",16,""SOYM_DiscordBot Launcher"":close")
 goto EXIT

:EXIT