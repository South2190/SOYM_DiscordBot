@echo off

rem ///////////////////////////////////////////////////////////////
rem
rem 				�I�x���I
rem
rem 		���̎��s�t�@�C���͏��������Ȃ��ł��������B
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
 powershell -Command "Add-Type -AssemblyName System.Windows.Forms;$result = [System.Windows.Forms.MessageBox]::Show(\"Python���C���X�g�[������Ă��Ȃ��悤�ł��B�C���X�g�[�����܂���?\", 'SOYM_DiscordBot Launcher', 'YesNo', 'Question');exit $result;"

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
 mshta vbscript:execute("msgbox""Python���C���X�g�[����A�ēx�����`���[�����s���Ă��������B"",64,""SOYM_DiscordBot Launcher"":close")
 goto EXIT

:ERROR
 mshta vbscript:execute("msgbox""���s�t�@�C��""""main.py""""��������Ȃ�����Bot���N���ł��܂���B"",16,""SOYM_DiscordBot Launcher"":close")
 goto EXIT

:ERROR2
 mshta vbscript:execute("msgbox""Bot�𗘗p����ɂ�Python���C���X�g�[������K�v������܂��B�����`���[���I�����܂��B"",16,""SOYM_DiscordBot Launcher"":close")
 goto EXIT

:ERROR3
 mshta vbscript:execute("msgbox""���̃R���s���[�^�[��Bot�̓���v���𖞂����Ă��܂���B"",16,""SOYM_DiscordBot Launcher"":close")
 goto EXIT

:EXIT