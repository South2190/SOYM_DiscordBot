@echo off

rem ///////////////////////////////////////////////////////////////
rem
rem 				�I�x���I
rem
rem 		���̎��s�t�@�C���͏��������Ȃ��ł��������B
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
 set /p Slt=Python���C���X�g�[������Ă��Ȃ��悤�ł��B�C���X�g�[�����܂���?(y/n)^>

 if '%Slt%'=='y' goto PYINSTALL
 if '%Slt%'=='n' goto ERROR2

 goto ASK_PYINSTALL

:PYINSTALL
 start python
 mshta vbscript:execute("msgbox""Python���C���X�g�[����A�ēx�����`���[�����s���Ă��������B"",64,""SOYM_DiscordBot Launcher"":close")
 goto EXIT

:ERROR
 mshta vbscript:execute("msgbox""���s�t�@�C��""""main.py""""��������Ȃ�����Bot���N���ł��܂���B"",16,""SOYM_DiscordBot Launcher"":close")
 goto EXIT

:ERROR2
 mshta vbscript:execute("msgbox""Bot�𗘗p����ɂ�Python���C���X�g�[������K�v������܂��B�����`���[���I�����܂��B"",16,""SOYM_DiscordBot Launcher"":close")
 goto EXIT