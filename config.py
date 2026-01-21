"""
設定管理モジュール
環境変数やStreamlit secretsから設定を読み込む
"""

import os
import streamlit as st
from typing import Optional


def get_openai_api_key() -> Optional[str]:
    """
    OpenAI APIキーを取得
    
    Returns:
        APIキー（存在しない場合はNone）
    """
    # Streamlit secretsから取得を試みる
    try:
        if hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets:
            return st.secrets['OPENAI_API_KEY']
    except:
        pass
    
    # 環境変数から取得を試みる
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        return api_key
    
    return None


def get_app_url() -> str:
    """
    アプリのURLを取得（Streamlit Cloudの場合）
    
    Returns:
        アプリのURL（ローカルの場合は空文字列）
    """
    try:
        if hasattr(st, 'secrets') and 'APP_URL' in st.secrets:
            return st.secrets['APP_URL']
    except:
        pass
    
    # 環境変数から取得を試みる
    app_url = os.getenv('APP_URL', '')
    return app_url


def get_default_character_count() -> int:
    """
    デフォルトの文字数を取得
    
    Returns:
        デフォルト文字数（デフォルト200文字）
    """
    try:
        if hasattr(st, 'secrets') and 'DEFAULT_CHARACTER_COUNT' in st.secrets:
            return int(st.secrets['DEFAULT_CHARACTER_COUNT'])
    except:
        pass
    
    # 環境変数から取得を試みる
    default_count = os.getenv('DEFAULT_CHARACTER_COUNT', '200')
    try:
        return int(default_count)
    except:
        return 200


def get_openai_model() -> str:
    """
    OpenAIモデル名を取得
    
    Returns:
        モデル名（デフォルト: gpt-3.5-turbo）
    """
    try:
        if hasattr(st, 'secrets') and 'OPENAI_MODEL' in st.secrets:
            return st.secrets['OPENAI_MODEL']
    except:
        pass
    
    # 環境変数から取得を試みる
    model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    return model


def validate_config() -> tuple[bool, Optional[str]]:
    """
    設定の妥当性を検証
    
    Returns:
        (有効かどうか, エラーメッセージ)
    """
    api_key = get_openai_api_key()
    if not api_key:
        return False, "OpenAI APIキーが設定されていません。設定を確認してください。"
    
    return True, None
