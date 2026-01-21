#!/bin/bash

# セットアップスクリプト
# このスクリプトは設定ファイルの作成を支援します

echo "=========================================="
echo "通知表所見自動生成ツール - セットアップ"
echo "=========================================="
echo ""

# secrets.tomlファイルの存在確認
if [ -f ".streamlit/secrets.toml" ]; then
    echo "⚠️  .streamlit/secrets.toml は既に存在します。"
    read -p "上書きしますか？ (y/N): " answer
    if [ "$answer" != "y" ] && [ "$answer" != "Y" ]; then
        echo "セットアップをキャンセルしました。"
        exit 0
    fi
fi

# テンプレートからコピー
echo "📋 設定ファイルを作成しています..."
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

echo ""
echo "✅ 設定ファイルを作成しました: .streamlit/secrets.toml"
echo ""
echo "=========================================="
echo "次のステップ:"
echo "=========================================="
echo ""
echo "1. OpenAI APIキーを取得してください:"
echo "   https://platform.openai.com/api-keys"
echo ""
echo "2. .streamlit/secrets.toml ファイルを開いて、"
echo "   OPENAI_API_KEY に実際のAPIキーを設定してください"
echo ""
echo "3. アプリを起動:"
echo "   streamlit run app.py"
echo ""
echo "詳しい手順は SETUP_GUIDE.md を参照してください。"
echo ""
