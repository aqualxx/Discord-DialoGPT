@echo off
CALL env\Scripts\activate.bat && cls
echo Starting chat bot...
python test_cli.py --bots=1
PAUSE