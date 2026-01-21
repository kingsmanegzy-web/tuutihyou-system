@echo off
REM セットアップスクリプト（Windows用）
REM このスクリプトは設定ファイルの作成を支援します

echo ==========================================
echo 通知表所見自動生成ツール - セットアップ
echo ==========================================
echo.

REM secrets.tomlファイルの存在確認
if exist ".streamlit\secrets.toml" (
    echo .streamlit\secrets.toml は既に存在します。
    set /p answer="上書きしますか？ (y/N): "
    if /i not "%answer%"=="y" (
        echo セットアップをキャンセルしました。
        exit /b 0
    )
)

REM テンプレートからコピー
echo 設定ファイルを作成しています...
copy .streamlit\secrets.toml.example .streamlit\secrets.toml >nul

echo.
echo 設定ファイルを作成しました: .streamlit\secrets.toml
echo.
echo ==========================================
echo 次のステップ:
echo ==========================================
echo.
echo 1. OpenAI APIキーを取得してください:
echo    https://platform.openai.com/api-keys
echo.
echo 2. .streamlit\secrets.toml ファイルを開いて、
echo    OPENAI_API_KEY に実際のAPIキーを設定してください
echo.
echo 3. アプリを起動:
echo    streamlit run app.py
echo.
echo 詳しい手順は SETUP_GUIDE.md を参照してください。
echo.
pause
