# Streamlit Cloudへのデプロイガイド

他の先生にも使ってもらうため、Streamlit Cloudにデプロイして、どこからでもアクセスできるようにします。

---

## 📋 前提条件

1. **GitHubアカウント**（無料で作成可能）
   - https://github.com/ にアクセス
   - アカウントを作成（まだお持ちでない場合）

2. **Streamlit Cloudアカウント**（無料）
   - GitHubアカウントでログイン可能

---

## 🚀 デプロイ手順

### ステップ1: GitHubにリポジトリを作成

1. **GitHubにログイン**
   - https://github.com/ にアクセスしてログイン

2. **新しいリポジトリを作成**
   - 右上の「+」ボタン > 「New repository」をクリック
   - Repository name: `tuutihyou-system`（任意の名前）
   - Description: 「通知表所見自動生成ツール」
   - Public を選択（Streamlit CloudはPublicリポジトリのみ対応）
   - 「Add a README file」はチェックしない（既にREADMEがあるため）
   - 「Create repository」をクリック

---

### ステップ2: ローカルでGitを初期化してプッシュ

このステップでは、パソコンにあるファイルをGitHubにアップロードします。

#### 2-1: ターミナルを開く

**Macの場合:**
1. 画面の右上の虫眼鏡アイコン（🔍）をクリック
2. 「ターミナル」と入力
3. 「ターミナル」アプリをクリックして開く

**Windowsの場合:**
1. スタートメニューを開く
2. 「cmd」と入力
3. 「コマンドプロンプト」をクリックして開く

#### 2-2: プロジェクトのフォルダに移動する

ターミナルが開いたら、以下のコマンドを1つずつ入力して、Enterキーを押します。

```bash
cd /Users/higashiyukako/Documents/cursor/オリジナルシステム開発/tuutihyou.system
```

**説明:**
- `cd` は「フォルダを移動する」という意味です
- このコマンドで、プロジェクトのフォルダに移動します

**確認方法:**
- コマンドを実行すると、何も表示されなければ成功です
- エラーが出た場合は、フォルダの場所が違う可能性があります

#### 2-3: Gitがインストールされているか確認

以下のコマンドを入力してEnterキーを押します：

```bash
git --version
```

**結果:**
- `git version 2.x.x` のように表示されればOKです
- 「command not found」と表示された場合は、Gitをインストールする必要があります
  - Mac: Xcode Command Line Toolsをインストール（`xcode-select --install`）
  - Windows: https://git-scm.com/download/win からダウンロード

#### 2-4: Gitを初期化する

以下のコマンドを入力してEnterキーを押します：

```bash
git init
```

**説明:**
- このフォルダをGitで管理できるようにします
- 「Initialized empty Git repository...」と表示されれば成功です

#### 2-5: すべてのファイルを追加する

以下のコマンドを入力してEnterキーを押します：

```bash
git add .
```

**説明:**
- `.` は「このフォルダの中のすべてのファイル」という意味です
- すべてのファイルをGitに追加します
- 何も表示されなければ成功です

**注意:**
- コマンドは `git add .` だけです（`#` や他の文字は不要です）
- コピー&ペーストする場合は、コマンド部分だけをコピーしてください
- ターミナルに `@git` や変な表示が出た場合は、`Ctrl+C` を押してキャンセルし、もう一度入力してください

**トラブルシューティング:**
- もし `@git` や変な表示が出た場合：
  1. `Ctrl+C` を押してキャンセル
  2. 新しい行で `git add .` と入力（コピー&ペースト推奨）
  3. Enterキーを押す

#### 2-6: ファイルを保存する（コミット）

以下のコマンドを入力してEnterキーを押します：

```bash
git commit -m "Initial commit: 通知表所見自動生成ツール"
```

**説明:**
- `commit` は「保存する」という意味です
- `-m` の後は「保存するときのメモ」です
- 「X files changed...」のように表示されれば成功です

**確認方法:**
- ターミナルに「X files changed, Y insertions(+)」のように表示されれば成功です
- 例: `7 files changed, 1234 insertions(+)`
- この表示が出たら、次のステップ（2-7）に進めます

**まだ「Changes not staged for commit」と表示される場合:**
- ステップ2-5（`git add .`）を実行していない可能性があります
- もう一度 `git add .` を実行してから、`git commit` を実行してください

**エラーが出た場合:**
- 「Please tell me who you are」と表示されたら、以下のコマンドを実行してください：

```bash
git config --global user.name "あなたの名前"
git config --global user.email "あなたのメールアドレス"
```

**入力する内容:**

1. **「あなたの名前」の部分:**
   - GitHubに登録した名前、または表示したい名前を入力
   - 例: `"田中太郎"` または `"Tanaka Taro"` または `"tanaka"`
   - 日本語でも英語でもOKです
   - 実際の例: `git config --global user.name "田中太郎"`

2. **「あなたのメールアドレス」の部分:**
   - **GitHubに登録したメールアドレス**を入力
   - GitHubにログインするときに使うメールアドレスです
   - 例: `"tanaka@example.com"`
   - 実際の例: `git config --global user.email "tanaka@example.com"`

**GitHubのメールアドレスを確認する方法:**
1. GitHubにログイン
2. 右上のプロフィールアイコンをクリック
3. 「Settings」をクリック
4. 左メニューの「Emails」をクリック
5. 表示されているメールアドレスをコピー

**注意:**
- メールアドレスは `"` (ダブルクォート) で囲む必要があります
- 名前も `"` (ダブルクォート) で囲む必要があります
- 実際のコマンド例:

```bash
# 例1: 日本語の名前の場合
git config --global user.name "田中太郎"
git config --global user.email "tanaka@example.com"

# 例2: 英語の名前の場合
git config --global user.name "Tanaka Taro"
git config --global user.email "tanaka@example.com"

# 例3: ユーザー名の場合
git config --global user.name "tanaka"
git config --global user.email "tanaka@example.com"
```

その後、もう一度 `git commit` を実行してください。

#### 2-7: GitHubのリポジトリと接続する

ステップ1で作成したGitHubリポジトリのURLを確認します。

1. GitHubのリポジトリページを開く
2. 緑色の「Code」ボタンをクリック
3. 「HTTPS」タブが選択されていることを確認
4. 表示されているURLをコピー（例: `https://github.com/あなたのユーザー名/tuutihyou-system.git`）

以下のコマンドを入力します（`あなたのユーザー名` の部分を実際のユーザー名に置き換えてください）：

```bash
git remote add origin https://github.com/あなたのユーザー名/tuutihyou-system.git
```

**例:**
- ユーザー名が `tanaka` の場合: `git remote add origin https://github.com/tanaka/tuutihyou-system.git`
- リポジトリ名が `shoken-tool` の場合: `git remote add origin https://github.com/tanaka/shoken-tool.git`

**説明:**
- `remote add origin` は「GitHubのリポジトリと接続する」という意味です
- 何も表示されなければ成功です

**エラーが出た場合:**
- 「remote origin already exists」と表示されたら、以下のコマンドで削除してから再度追加してください：

```bash
git remote remove origin
git remote add origin https://github.com/あなたのユーザー名/tuutihyou-system.git
```

#### 2-8: メインブランチを設定する

以下のコマンドを入力してEnterキーを押します：

```bash
git branch -M main
```

**説明:**
- ブランチ名を `main` に設定します
- 何も表示されなければ成功です

#### 2-9: GitHubにアップロードする（プッシュ）

以下のコマンドを入力してEnterキーを押します：

```bash
git push -u origin main
```

**説明:**
- `push` は「アップロードする」という意味です
- ファイルをGitHubにアップロードします

**初回の場合:**
- GitHubのユーザー名とパスワード（またはトークン）を求められる場合があります
- ユーザー名を入力してEnterキー
- パスワードを入力してEnterキー（画面には表示されませんが、入力されています）

**パスワードが求められた場合:**
- 通常のパスワードではなく、「Personal Access Token」が必要な場合があります
- 以下の手順でトークンを作成してください：
  1. GitHubにログイン
  2. 右上のプロフィールアイコン > 「Settings」
  3. 左メニューの「Developer settings」
  4. 「Personal access tokens」> 「Tokens (classic)」
  5. 「Generate new token」> 「Generate new token (classic)」
  6. Note: 「Streamlit Cloud」と入力
  7. 「repo」にチェック
  8. 「Generate token」をクリック
  9. 表示されたトークンをコピー（後で表示されないので注意）
  10. パスワードの代わりに、このトークンを貼り付け

**成功した場合:**
- 「Enumerating objects...」のように表示され、最後に「To https://github.com/...」と表示されれば成功です
- GitHubのリポジトリページを更新すると、ファイルが表示されているはずです

---

## 📝 コマンド一覧（コピー&ペースト用）

以下を順番に実行してください：

```bash
# 1. フォルダに移動
cd /Users/higashiyukako/Documents/cursor/オリジナルシステム開発/tuutihyou.system

# 2. Gitを初期化
git init

# 3. ファイルを追加
git add .

# 4. 保存（コミット）
git commit -m "Initial commit: 通知表所見自動生成ツール"

# 5. GitHubと接続（あなたのユーザー名に置き換えてください）
git remote add origin https://github.com/あなたのユーザー名/tuutihyou-system.git

# 6. メインブランチを設定
git branch -M main

# 7. GitHubにアップロード
git push -u origin main
```

---

## ❓ よくある質問

### Q: コマンドを間違えて入力してしまった

**A:** `Ctrl+C` を押すと、コマンドをキャンセルできます。もう一度正しいコマンドを入力してください。

### Q: 「command not found」と表示される

**A:** Gitがインストールされていない可能性があります。上記の「2-3: Gitがインストールされているか確認」を参照してください。

### Q: 「Permission denied」と表示される

**A:** フォルダの場所が間違っている可能性があります。`pwd` コマンドで現在の場所を確認してください。

### Q: パスワードを求められたが、入力できない

**A:** パスワードは画面に表示されませんが、入力されています。入力が終わったらEnterキーを押してください。

### Q: すべてのコマンドを実行したが、GitHubにファイルが表示されない

**A:** 
1. GitHubのリポジトリページを更新（F5キー）してみてください
2. エラーメッセージがないか確認してください
3. `git status` コマンドで状態を確認してください

---

### ステップ3: Streamlit Cloudでアプリをデプロイ

1. **Streamlit Cloudにアクセス**
   - https://streamlit.io/cloud にアクセス
   - 「Sign up」または「Log in」をクリック
   - GitHubアカウントでログイン

2. **新しいアプリを作成**
   - 「New app」ボタンをクリック
   - **Repository**: ステップ1で作成したリポジトリを選択
   - **Branch**: `main` を選択
   - **Main file path**: `app.py` を入力
   - **App URL**: 自動生成されます（例: `tuutihyou-system`）
   - 「Deploy!」をクリック

3. **デプロイの完了を待つ**
   - 数分かかります
   - デプロイが完了すると、アプリのURLが表示されます
   - 例: `https://tuutihyou-system.streamlit.app`

---

### ステップ4: OpenAI APIキーを設定

現在、アプリに「OpenAI APIキーが設定されていません」というエラーが表示されています。これを解決するために、Streamlit CloudのSecretsにAPIキーを設定します。

#### 4-1: Streamlit Cloudのダッシュボードを開く

1. **アプリの右上の「Manage app」ボタンをクリック**
   - 画面の右下に「Manage app」というボタンがあります
   - または、https://share.streamlit.io/ にアクセスして、デプロイしたアプリを選択

2. **「Settings」をクリック**
   - 左メニューまたは上部のタブから「Settings」を選択

#### 4-2: Secretsを設定

1. **左メニューから「Secrets」を選択**
   - 「Settings」ページの左側に「Secrets」というメニューがあります

2. **Secretsエディタに以下の内容を入力**

**重要: 以下の形式を正確にコピー&ペーストしてください**

```toml
OPENAI_API_KEY = "your-openai-api-key-here"
APP_URL = "https://tuutihyou-system-5tb77yyxm3imubsmmjagb3.streamlit.app"
DEFAULT_CHARACTER_COUNT = 200
OPENAI_MODEL = "gpt-3.5-turbo"
```

**入力の注意点:**
- 各行の最後に改行を入れてください（最後の行も含む）
- `your-openai-api-key-here` の部分を、実際のOpenAI APIキーに置き換えてください
- APIキーは `"` (ダブルクォート) で囲む必要があります
- APIキーに改行が含まれていないか確認してください（1行である必要があります）
- `APP_URL` の部分を、実際のアプリのURLに置き換えてください
  - 現在のURL: `https://tuutihyou-system-5tb77yyxm3imubsmmjagb3.streamlit.app`
  - このURLは、ブラウザのアドレスバーに表示されています

**「Invalid format」エラーが出る場合の対処法:**

1. **すべての内容を削除して、最初から入力し直す**
   - Secretsエディタの内容をすべて選択（Ctrl+A または Cmd+A）
   - 削除（Deleteキー）
   - 以下の形式を1行ずつ正確に入力

2. **APIキーが長い場合の確認**
   - APIキーは1行である必要があります
   - 改行が入っていないか確認してください
   - コピー&ペーストの際に、余分なスペースや改行が入っていないか確認

3. **引用符の確認**
   - すべての値は `"` (ダブルクォート) で囲む必要があります
   - シングルクォート `'` は使えません

4. **正しい形式の例（コピー&ペースト用）:**

```
OPENAI_API_KEY = "sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
APP_URL = "https://tuutihyou-system-5tb77yyxm3imubsmmjagb3.streamlit.app"
DEFAULT_CHARACTER_COUNT = 200
OPENAI_MODEL = "gpt-3.5-turbo"
```

**入力手順（推奨）:**
1. Secretsエディタを開く
2. 既存の内容をすべて削除（Ctrl+A → Delete）
3. 上記の形式を1行ずつ入力（またはコピー&ペースト）
4. APIキーの部分だけを実際のキーに置き換える
5. 各行の最後にEnterキーを押して改行を入れる
6. 「Save changes」をクリック

#### 4-3: 保存

1. **「Save」ボタンをクリック**
   - 画面の下部または右上に「Save」ボタンがあります

2. **アプリが自動的に再デプロイされます**
   - 数秒から1分程度かかります
   - 再デプロイが完了すると、エラーが消えてアプリが正常に動作します

#### 4-4: OpenAI APIキーを取得する方法（まだ取得していない場合）

1. **OpenAIのサイトにアクセス**
   - https://platform.openai.com/api-keys

2. **ログイン**
   - OpenAIアカウントでログイン（アカウントがない場合は新規登録）

3. **APIキーを取得**
   - 「Create new secret key」をクリック
   - キー名を入力（例：「通知表所見ツール」）
   - 「Create secret key」をクリック
   - 表示されたAPIキーをコピー（後で表示されないので注意）

4. **クレジットを追加（初回のみ）**
   - 左メニューの「Billing」を選択
   - 「Add payment method」をクリック
   - クレジットカード情報を入力
   - 初回は$5分（約750円相当）の無料クレジットが付与されます

---

### ステップ5: アプリの動作確認

1. **アプリのURLにアクセス**
   - 例: `https://tuutihyou-system.streamlit.app`
   - ブラウザで開いて動作確認

2. **QRコードを確認**
   - サイドバーにQRコードが表示されるはずです
   - QRコードをスマホでスキャンして、アクセスできるか確認

---

## ✅ デプロイ完了後の確認事項

- [ ] アプリが正常に表示される
- [ ] キーワードを選択して所見を生成できる
- [ ] QRコードが表示される
- [ ] スマホでQRコードをスキャンしてアクセスできる
- [ ] 他の先生のスマホからもアクセスできる

---

## 🔄 コードを更新する場合

コードを更新したら、以下のコマンドでGitHubにプッシュします：

```bash
# 変更をステージング
git add .

# コミット
git commit -m "更新内容の説明"

# GitHubにプッシュ
git push
```

Streamlit Cloudが自動的に再デプロイします（数分かかります）。

---

## 🆘 トラブルシューティング

### デプロイが失敗する

**原因**: 依存関係が不足している可能性

**解決方法**:
- `requirements.txt` にすべての依存関係が含まれているか確認
- Streamlit Cloudのログを確認（「Logs」タブ）

### QRコードが表示されない

**原因**: `APP_URL` が正しく設定されていない

**解決方法**:
- Streamlit Cloudの「Settings」> 「Secrets」で `APP_URL` を確認
- アプリのURLと一致しているか確認

### OpenAI APIエラー

**原因**: APIキーが正しく設定されていない

**解決方法**:
- Streamlit Cloudの「Settings」> 「Secrets」で `OPENAI_API_KEY` を確認
- APIキーが正しいか確認

---

## 📱 QRコードの共有

デプロイが完了したら：

1. **QRコードをダウンロード**
   - アプリのサイドバーから「QRコードをダウンロード（印刷用）」をクリック

2. **QRコードを配布**
   - メールで送付
   - 会議資料に印刷
   - 掲示板に貼り付け

3. **URLを直接共有**
   - 例: `https://tuutihyou-system.streamlit.app`
   - メールやメッセージで共有

---

## 💡 ヒント

- **アプリのURLを短くする**: Streamlit Cloudの「Settings」で「App URL」を変更できます
- **カスタムドメイン**: 独自ドメインを設定することも可能（有料プラン）
- **アクセス制限**: 現在はPublicリポジトリのみ対応（将来的にPrivateリポジトリも対応予定）

---

## 🎉 完了

これで、どこからでもアクセスできる通知表所見自動生成ツールが完成しました！

他の先生は、QRコードをスキャンするか、URLを開くだけで使えます。
