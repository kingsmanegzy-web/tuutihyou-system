# セットアップガイド（初心者向け）

このガイドでは、通知表所見自動生成ツールを初めて使う方向けに、詳しい手順を説明します。

---

## 📋 目次

1. [OpenAI APIキーの取得](#1-openai-apiキーの取得)
2. [設定ファイルの作成](#2-設定ファイルの作成)
3. [アプリの実行](#3-アプリの実行)
4. [トラブルシューティング](#4-トラブルシューティング)

---

## 1. OpenAI APIキーの取得

### ステップ1-1: OpenAIアカウントにログイン（または新規登録）

1. ブラウザで以下のURLを開きます：
   - https://platform.openai.com/

2. アカウントをお持ちでない場合：
   - 「Sign up」をクリックして新規登録
   - メールアドレスとパスワードを設定
   - メール認証を完了

3. アカウントをお持ちの場合：
   - 「Log in」をクリックしてログイン

### ステップ1-2: APIキーを取得

1. ログイン後、右上のプロフィールアイコンをクリック
2. 「API keys」を選択
3. 「Create new secret key」をクリック
4. キー名を入力（例：「通知表所見ツール」）
5. 「Create secret key」をクリック
6. **重要**: 表示されたAPIキーをコピーします
   - ⚠️ このキーは後で表示されないため、必ずコピーしてください
   - 例: `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### ステップ1-3: クレジットを追加（初回のみ）

1. 左メニューから「Billing」を選択
2. 「Add payment method」をクリック
3. クレジットカード情報を入力
4. 初回は$5分（約750円相当）の無料クレジットが付与されます

---

## 2. 設定ファイルの作成

### ステップ2-1: テンプレートファイルをコピー

ターミナル（コマンドライン）を開いて、以下のコマンドを実行します：

```bash
cd /Users/higashiyukako/Documents/cursor/オリジナルシステム開発/tuutihyou.system
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

**Windowsの場合（コマンドプロンプト）:**
```cmd
cd C:\Users\あなたのユーザー名\Documents\cursor\オリジナルシステム開発\tuutihyou.system
copy .streamlit\secrets.toml.example .streamlit\secrets.toml
```

### ステップ2-2: 設定ファイルを編集

1. プロジェクトフォルダ内の `.streamlit` フォルダを開く
2. `secrets.toml` ファイルをテキストエディタで開く
   - メモ帳、VS Code、テキストエディットなど、どのエディタでもOK

3. ファイルの内容を以下のように編集：

```toml
# OpenAI APIキー（必須）
OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# アプリのURL（QRコード生成用、オプション）
# ローカルで使う場合は空欄のままでOK
APP_URL = ""

# デフォルト文字数（オプション、デフォルト: 200）
DEFAULT_CHARACTER_COUNT = 200

# OpenAIモデル名（オプション、デフォルト: gpt-3.5-turbo）
OPENAI_MODEL = "gpt-3.5-turbo"
```

4. **重要**: `OPENAI_API_KEY` の `"sk-xxxxxxxx..."` の部分を、ステップ1-2でコピーした実際のAPIキーに置き換えます

5. ファイルを保存

**注意**: 
- APIキーは `"` (ダブルクォート) で囲む必要があります
- ファイル名は必ず `secrets.toml` にしてください（`.toml` 拡張子が重要）

---

## 3. アプリの実行

### ステップ3-1: ターミナルでアプリを起動

ターミナル（コマンドライン）を開いて、以下のコマンドを実行します：

```bash
cd /Users/higashiyukako/Documents/cursor/オリジナルシステム開発/tuutihyou.system
streamlit run app.py
```

**Windowsの場合:**
```cmd
cd C:\Users\あなたのユーザー名\Documents\cursor\オリジナルシステム開発\tuutihyou.system
streamlit run app.py
```

### ステップ3-2: Streamlitの初回設定（初回のみ）

初回起動時、メール登録のプロンプトが表示される場合があります：

```
👋 Welcome to Streamlit!

If you'd like to receive helpful onboarding emails, news, offers, promotions,
and the occasional swag, please enter your email address below. Otherwise,
leave this field blank.

Email:  
```

**対応方法:**
- **メール登録をスキップする場合**: 何も入力せずに **Enterキー** を押す
- **メールアドレスを登録する場合**: メールアドレスを入力して **Enterキー** を押す

Enterキーを押すと、アプリが起動します。

### ステップ3-3: ブラウザでアプリを開く

1. コマンド実行後、自動的にブラウザが開きます
2. 開かない場合は、ターミナルに表示されているURLをコピーしてブラウザで開きます
   - 例: `http://localhost:8501`
   
**ターミナルに表示される例:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

### ステップ3-4: アプリの使い方

1. **キーワードを選択**
   - 「キーワードを選択」の欄から、児童の特徴を選択
   - 複数選択可能
   - ない場合は「カスタムキーワード」欄に入力

2. **文字数を確認**
   - サイドバーの「文字数」で目標文字数を確認（デフォルト200文字）

3. **所見を生成**
   - 「🎯 所見を生成」ボタンをクリック
   - 進捗バーが表示され、生成が完了します

4. **結果を確認・保存**
   - 生成された所見文を確認
   - 「📋 コピー」でコピー
   - 「💾 保存」で保存（児童名を入力すると管理しやすい）

5. **保存した所見を確認**
   - 「📋 保存した所見一覧」タブで確認・編集・削除が可能

---

## 4. トラブルシューティング

### エラー: "OpenAI APIキーが設定されていません"

**原因**: `secrets.toml` ファイルが正しく設定されていない

**解決方法**:
1. `.streamlit/secrets.toml` ファイルが存在するか確認
2. `OPENAI_API_KEY` が正しく設定されているか確認
3. APIキーが `"` (ダブルクォート) で囲まれているか確認
4. ファイルを保存し直す
5. アプリを再起動（ターミナルで `Ctrl+C` で停止してから再度 `streamlit run app.py`）

### エラー: "APIキーが正しくありません"

**原因**: APIキーが間違っている、または無効

**解決方法**:
1. OpenAIのサイトでAPIキーが有効か確認
2. 新しいAPIキーを生成して設定し直す
3. クレジットが残っているか確認（OpenAIのBillingページ）

### エラー: "リクエストが多すぎます"

**原因**: APIの利用制限に達した

**解決方法**:
1. 少し待ってから再度お試しください
2. OpenAIの利用制限を確認

### アプリが起動しない

**原因**: ポートが既に使用されている、または依存関係がインストールされていない

**解決方法**:
1. 依存関係を再インストール:
   ```bash
   pip install -r requirements.txt
   ```
2. 別のポートで起動:
   ```bash
   streamlit run app.py --server.port 8502
   ```

### QRコードが表示されない

**原因**: `APP_URL` が設定されていない

**解決方法**:
- ローカルで使う場合は問題ありません（QRコードは表示されませんが、機能は使えます）
- Streamlit Cloudにデプロイした場合は、デプロイ後のURLを `APP_URL` に設定してください

---

## 📞 サポート

問題が解決しない場合は、以下を確認してください：

1. エラーメッセージの全文
2. `secrets.toml` ファイルの内容（APIキー部分は伏せて）
3. ターミナルの出力

---

## 🎉 次のステップ

アプリが正常に動作したら：

1. **Streamlit Cloudにデプロイ**して、他の人と共有
2. **QRコードを生成**して配布
3. **よく使うキーワード**を登録して効率化

詳しい手順は `README.md` を参照してください。
