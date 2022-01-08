@echo off
REM Copyright (c) 2012-2020, EnterpriseDB Corporation.  All rights reserved
REM PostgreSQL server psql runner script for Windows

for /f "delims=" %%a in ('chcp ^|find /c "932"') do @ SET CLIENTENCODING_JP=%%a
if "%CLIENTENCODING_JP%"=="1" SET PGCLIENTENCODING=SJIS
if "%CLIENTENCODING_JP%"=="1" SET /P PGCLIENTENCODING="Client Encoding [%PGCLIENTENCODING%]: "

REM Run psql
"C:\Program Files\PostgreSQL\14\bin\psql.exe" -h localhost -U postgres -d postgres -p 5432

pause