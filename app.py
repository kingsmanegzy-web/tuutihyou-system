"""
通知表所見自動生成ツール - メインアプリ
"""

import streamlit as st
import database
import config
import openai_client
import qr_generator
import error_handler
from typing import List

# ページ設定
st.set_page_config(
    page_title="通知表所見自動生成ツール",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# データベース初期化
@st.cache_resource
def init_db():
    """データベースを初期化（キャッシュ）"""
    return database.Database()

db = init_db()

# セッション状態の初期化
if 'generated_shoken' not in st.session_state:
    st.session_state.generated_shoken = None
if 'keywords' not in st.session_state:
    st.session_state.keywords = []
if 'character_count' not in st.session_state:
    st.session_state.character_count = config.get_default_character_count()
if 'grade_level' not in st.session_state:
    st.session_state.grade_level = "低学年"
if 'multiselect_key' not in st.session_state:
    st.session_state.multiselect_key = 0

# サイドバー
with st.sidebar:
    st.header("📱 アプリの共有")
    
    # QRコード表示
    app_url = config.get_app_url()
    
    # ローカル環境の場合の処理
    # 注意: ローカル環境では、同じWi-Fiネットワーク内のデバイスからのみアクセス可能です
    # 他の先生にも使ってもらうには、Streamlit Cloudにデプロイしてください
    if not app_url or app_url == "https://your-app-name.streamlit.app":
        # セッション状態にNetwork URLを保存（ユーザーが入力可能）
        if 'network_url' not in st.session_state:
            # 自動取得を試みる
            try:
                import socket
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                local_ip = s.getsockname()[0]
                s.close()
                st.session_state.network_url = f"http://{local_ip}:8501"
            except:
                st.session_state.network_url = ""
        
        # Network URLを手動入力できるようにする
        st.subheader("📱 ローカル環境での共有")
        st.caption("ターミナルに表示される「Network URL」を入力してください")
        
        network_url_input = st.text_input(
            "Network URL",
            value=st.session_state.network_url,
            placeholder="例: http://192.168.1.100:8501",
            help="Streamlit起動時にターミナルに表示される「Network URL」をコピーして貼り付けてください"
        )
        
        if network_url_input:
            st.session_state.network_url = network_url_input
            app_url = network_url_input
        else:
            app_url = None
    
    # QRコードを生成（URLが有効な場合）
    if app_url and app_url != "https://your-app-name.streamlit.app":
        try:
            qr_img = qr_generator.get_qr_code_numpy(app_url)
            # QRコード画像を表示
            st.image(qr_img, caption="📱 このQRコードをスキャンしてアクセス", use_container_width=False)
        except Exception as e:
            st.error(f"QRコードの生成に失敗しました: {str(e)}")
            # フォールバック: PIL Imageを直接使用
            try:
                qr_img_pil = qr_generator.get_qr_code_image(app_url)
                st.image(qr_img_pil, caption="📱 このQRコードをスキャンしてアクセス", use_container_width=False)
            except Exception as e2:
                st.error(f"QRコードの表示に失敗しました: {str(e2)}")
        
        # URL表示（コピー可能に）
        st.markdown(f"**QRコードに含まれるURL:** `{app_url}`")
        
        # URL検証
        if app_url.startswith("http://") or app_url.startswith("https://"):
            # テスト用リンク
            st.markdown(f"[🔗 このURLをPCのブラウザでテストする]({app_url})")
            
            # デバッグ情報
            with st.expander("🔍 アクセスできない場合の確認事項"):
                st.markdown(f"""
                **現在のURL:** `{app_url}`
                
                **確認手順:**
                
                1. **PCのブラウザでURLを開く**
                   - 上記の「このURLをPCのブラウザでテストする」をクリック
                   - PCのブラウザで開けない場合は、URLが間違っているか、Streamlitが起動していません
                
                2. **スマホとPCが同じWi-Fiに接続されているか確認**
                   - スマホのWi-Fi設定を確認
                   - PCと同じWi-Fiネットワークに接続されている必要があります
                
                3. **StreamlitがNetwork URLで起動しているか確認**
                   - ターミナルに「Network URL: http://192.168.x.x:8501」が表示されているか確認
                   - 表示されていない場合は、Streamlitを再起動してください
                
                4. **ファイアウォールの設定を確認**
                   - Mac: システム設定 > ネットワーク > ファイアウォール > オプション
                   - ポート8501が許可されているか確認
                   - または、一時的にファイアウォールを無効にしてテスト
                
                5. **スマホのブラウザで直接URLを入力**
                   - QRコードではなく、スマホのブラウザに直接URLを入力してアクセスできるか確認
                   - 例: `http://192.168.128.172:8501`
                
                6. **Streamlitの起動オプションを確認**
                   - ターミナルで `streamlit run app.py --server.address 0.0.0.0` で起動すると、ネットワークからのアクセスが確実に有効になります
                """)
        else:
            st.warning(f"⚠️ URLの形式が正しくありません: `{app_url}`")
            st.info("URLは `http://` または `https://` で始まる必要があります。")
        
        # 高解像度QRコードのダウンロード
        qr_bytes = qr_generator.get_qr_code_bytes(app_url, high_resolution=True)
        st.download_button(
            label="📥 QRコードをダウンロード（印刷用）",
            data=qr_bytes,
            file_name="tuutihyou-qrcode.png",
            mime="image/png"
        )
        
        # ローカル環境の場合の注意書き
        if "localhost" not in app_url and "127.0.0.1" not in app_url:
            st.warning("⚠️ **ローカル環境です** - 同じWi-Fiネットワーク内のデバイスからのみアクセス可能です。")
            st.info("💡 **他の先生にも使ってもらうには**: Streamlit Cloudにデプロイしてください。詳しくは `DEPLOY_GUIDE.md` を参照してください。")
            with st.expander("ℹ️ アクセスできない場合の確認事項"):
                st.markdown("""
                1. **スマホとPCが同じWi-Fiネットワークに接続されているか確認**
                   - スマホとPCが同じWi-Fiに接続されている必要があります
                
                2. **ファイアウォールの設定を確認**
                   - Mac: システム設定 > ネットワーク > ファイアウォール
                   - Windows: コントロールパネル > ファイアウォール
                   - ポート8501が許可されているか確認
                
                3. **StreamlitがNetwork URLで起動しているか確認**
                   - ターミナルに「Network URL: http://192.168.x.x:8501」が表示されているか確認
                   - 表示されていない場合は、Streamlitを再起動してください
                
                4. **URLが正しいか確認**
                   - 上記の「このURLをテストする」リンクをクリックして、PCのブラウザで開けるか確認
                   - 開けない場合は、URLが間違っている可能性があります
                """)
        else:
            st.warning("⚠️ localhostのため、同じPCからのみアクセス可能です。")
    else:
        if not app_url or app_url == "https://your-app-name.streamlit.app":
            st.info("💡 ローカル環境では、上記の「Network URL」を入力してください。")
        else:
            st.info("🔗 アプリのURLを設定すると、QRコードが表示されます")
            st.caption("`.streamlit/secrets.toml` の `APP_URL` にURLを設定してください")
    
    st.divider()
    
    # 設定
    st.header("⚙️ 設定")
    grade_level = st.selectbox(
        "学年",
        options=["低学年", "中学年", "高学年"],
        index=["低学年", "中学年", "高学年"].index(st.session_state.grade_level) if st.session_state.grade_level in ["低学年", "中学年", "高学年"] else 0,
        help="学年に応じて表現が変わります"
    )
    st.session_state.grade_level = grade_level
    
    character_count = st.number_input(
        "文字数",
        min_value=50,
        max_value=500,
        value=st.session_state.character_count,
        step=10,
        help="生成する所見文の目標文字数"
    )
    st.session_state.character_count = character_count

# メインコンテンツ
st.title("📝 通知表所見自動生成ツール")
st.caption("キーワードを入力して、自然な日本語の所見文を自動生成します")

# 設定の検証
is_valid, error_msg = config.validate_config()
if not is_valid:
    st.error(f"⚠️ {error_msg}")
    st.info("💡 `.streamlit/secrets.toml` ファイルに `OPENAI_API_KEY` を設定してください。")
    st.stop()

# タブ
tab1, tab2 = st.tabs(["📝 所見を生成", "📋 保存した所見一覧"])

with tab1:
    st.header("所見を生成")
    
    # よく使うキーワードを取得
    popular_keywords = db.get_popular_keywords(limit=15)
    popular_keyword_list = [kw['keyword'] for kw in popular_keywords]
    
    # プリセットキーワード
    preset_keywords = [
        "積極的", "協調性", "集中力", "創造性", "責任感", "思いやり",
        "好奇心", "探究心", "表現力", "判断力", "思考力", "判断力",
        "コミュニケーション", "リーダーシップ", "自主性", "主体性"
    ]
    
    # すべてのキーワード候補
    all_keywords = list(set(preset_keywords + popular_keyword_list))
    
    # セッション状態のキーワードをフィルタリング（選択肢に含まれるもののみ）
    valid_default_keywords = [
        kw for kw in st.session_state.keywords 
        if kw in all_keywords
    ]
    
    # キーワード選択
    st.subheader("キーワードを選択")
    selected_keywords = st.multiselect(
        "児童の特徴・キーワードを選択してください",
        options=all_keywords,
        default=valid_default_keywords,
        key=f"keyword_select_{st.session_state.multiselect_key}",
        help="複数選択可能です"
    )
    
    # 選択が変更されたらセッション状態を更新（連続選択を可能にする）
    if selected_keywords != st.session_state.keywords:
        st.session_state.keywords = selected_keywords
    
    # カスタムキーワード入力
    custom_keyword = st.text_input(
        "カスタムキーワードを追加（カンマ区切りで複数入力可能）",
        placeholder="例: 読書好き, 計算が得意",
        help="よく使うキーワードにない場合は、ここに入力してください"
    )
    
    # カスタムキーワードを追加
    if custom_keyword:
        custom_list = [kw.strip() for kw in custom_keyword.split(',') if kw.strip()]
        selected_keywords.extend(custom_list)
    
    # セッション状態を更新（選択が変更された場合のみ）
    if set(selected_keywords) != set(st.session_state.keywords):
        st.session_state.keywords = selected_keywords
    
    # クラス名と児童名の入力
    col1, col2 = st.columns(2)
    
    with col1:
        class_name = st.text_input(
            "クラス名（学年・組）",
            placeholder="例: 3年1組",
            help="保存時に使用されます。クラス単位で管理できます。"
        )
    
    with col2:
        student_name = st.text_input(
            "児童名",
            placeholder="例: 山田太郎",
            help="保存時に使用されます"
        )
    
    # 生成ボタン
    if st.button("🎯 所見を生成", type="primary", use_container_width=True):
        if not selected_keywords:
            st.warning("⚠️ キーワードを1つ以上選択してください")
        else:
            try:
                # 進捗表示
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # ステップ1: キーワード解析
                status_text.text("📝 キーワードを解析中...")
                progress_bar.progress(20)
                
                # ステップ2: 文章生成
                status_text.text("✍️ 文章を生成中...")
                progress_bar.progress(50)
                
                # OpenAI API呼び出し
                client = openai_client.OpenAIClient()
                generated_text = client.generate_shoken(
                    selected_keywords,
                    st.session_state.character_count,
                    st.session_state.grade_level
                )
                
                # ステップ3: 文字数調整
                status_text.text("📏 文字数を調整中...")
                progress_bar.progress(80)
                
                # ステップ4: 完成
                status_text.text("✅ 完成しました！")
                progress_bar.progress(100)
                
                st.session_state.generated_shoken = generated_text
                
                # キーワード履歴を保存
                db.add_keyword_history(selected_keywords)
                
                # 進捗バーを非表示
                progress_bar.empty()
                status_text.empty()
                
            except Exception as e:
                error_handler.handle_error(e, show_details=True)
                st.session_state.generated_shoken = None
    
    # 生成結果の表示
    if st.session_state.generated_shoken:
        st.divider()
        st.subheader("生成された所見")
        
        # 文字数表示
        char_count = len(st.session_state.generated_shoken)
        st.caption(f"文字数: {char_count}文字")
        
        # 所見文表示
        st.text_area(
            "所見文",
            value=st.session_state.generated_shoken,
            height=200,
            label_visibility="collapsed"
        )
        
        # ボタン
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📋 コピー", use_container_width=True):
                st.write("```\n" + st.session_state.generated_shoken + "\n```")
                st.success("✅ コピーしました！上記のテキストを選択してコピーしてください")
        
        with col2:
            if st.button("💾 保存", use_container_width=True):
                try:
                    db.save_shoken(
                        student_name or "未設定",
                        st.session_state.keywords,
                        st.session_state.generated_shoken,
                        char_count,
                        class_name or ""
                    )
                    st.success("✅ 保存しました！")
                    st.rerun()
                except Exception as e:
                    error_handler.handle_error(e, show_details=True)
                    st.error("⚠️ 保存に失敗しました。エラー内容を確認してください。")
        
        with col3:
            if st.button("🔄 再生成", use_container_width=True):
                st.session_state.generated_shoken = None
                st.rerun()

with tab2:
    st.header("保存した所見一覧")
    
    # 所見一覧を取得
    shoken_list = db.get_all_shoken()
    
    if not shoken_list:
        st.info("📝 まだ保存された所見がありません。所見を生成して保存してください。")
    else:
        st.caption(f"全{len(shoken_list)}件の所見が保存されています")
        
        for shoken in shoken_list:
            # クラス名を表示
            display_name = f"📝 {shoken['student_name']}"
            if shoken['class_name']:
                display_name += f" ({shoken['class_name']})"
            display_name += f" - {shoken['created_at'][:10]}"
            
            with st.expander(display_name):
                if shoken['class_name']:
                    st.write(f"**クラス:** {shoken['class_name']}")
                st.write(f"**キーワード:** {', '.join(shoken['keywords'])}")
                st.write(f"**文字数:** {shoken['character_count']}文字")
                st.write(f"**作成日時:** {shoken['created_at']}")
                st.divider()
                st.text_area(
                    "所見文",
                    value=shoken['content'],
                    height=150,
                    key=f"shoken_{shoken['id']}",
                    label_visibility="collapsed"
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📋 コピー", key=f"copy_{shoken['id']}"):
                        st.write("```\n" + shoken['content'] + "\n```")
                        st.success("✅ コピーしました！")
                with col2:
                    if st.button("🗑️ 削除", key=f"delete_{shoken['id']}"):
                        db.delete_shoken(shoken['id'])
                        st.success("✅ 削除しました！")
                        st.rerun()
