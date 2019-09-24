@echo off

echo ======================================================

echo [*] 所有盘符下的有趣文件

@For /F "Skip=1" %%i in ('Wmic Logicaldisk Where "DriveType=3" Get Name') Do cd %%i&&%%i&&dir /s *pass* == *vnc* == *.config*


echo ======================================================

echo [*] 所以盘符下文件中包含password关键字的


@For /F "Skip=1" %%i in ('Wmic Logicaldisk Where "DriveType=3" Get Name') Do cd %%i&&%%i&&findstr /si password *.xml *.ini *.txt *.config

echo ======================================================

echo [*] 所以盘符下文件中包含密码关键字的
@For /F "Skip=1" %%i in ('Wmic Logicaldisk Where "DriveType=3" Get Name') Do cd %%i&&%%i&&findstr /si 密码 *.xml *.ini *.txt *.config

echo ======================================================

echo [*] 所以盘符下文件中包含账号关键字的
@For /F "Skip=1" %%i in ('Wmic Logicaldisk Where "DriveType=3" Get Name') Do cd %%i&&%%i&&findstr /si 账号 *.xml *.ini *.txt *.config

echo ======================================================

echo [*] 所以盘符下文件中包含Password关键字的
@For /F "Skip=1" %%i in ('Wmic Logicaldisk Where "DriveType=3" Get Name') Do cd %%i&&%%i&&findstr /si Password *.xml *.ini *.txt *.config

