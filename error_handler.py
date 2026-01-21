"""
エラーハンドリングモジュール
技術的なエラーを教師向けの分かりやすいメッセージに変換
"""

from typing import Optional
import openai


def get_user_friendly_error(error: Exception) -> tuple[str, str]:
    """
    技術的なエラーを教師向けの分かりやすいメッセージに変換
    
    Args:
        error: 発生したエラー
        
    Returns:
        (エラーメッセージ, 解決方法)
    """
    error_type = type(error).__name__
    error_message = str(error)
    
    # OpenAI API関連のエラー
    if isinstance(error, openai.AuthenticationError):
        return (
            "⚠️ **APIキーが正しくありません**",
            "💡 解決方法: 開発者に連絡して、APIキーの設定を確認してください。"
        )
    
    if isinstance(error, openai.APIError):
        if "rate limit" in error_message.lower():
            return (
                "⚠️ **リクエストが多すぎます**",
                "💡 解決方法: 少し待ってから再度お試しください。"
            )
        elif "insufficient_quota" in error_message.lower():
            return (
                "⚠️ **APIの利用上限に達しました**",
                "💡 解決方法: 開発者に連絡してください。"
            )
        else:
            return (
                "⚠️ **APIでエラーが発生しました**",
                "💡 解決方法: しばらく待ってから再度お試しください。問題が続く場合は開発者に連絡してください。"
            )
    
    if isinstance(error, openai.APIConnectionError):
        return (
            "⚠️ **インターネット接続を確認してください**",
            "💡 解決方法: Wi-Fiがつながっているか確認してください。"
        )
    
    if isinstance(error, openai.APITimeoutError):
        return (
            "⚠️ **タイムアウトエラーが発生しました**",
            "💡 解決方法: しばらく待ってから再度お試しください。"
        )
    
    # ネットワーク関連のエラー
    if "Connection" in error_type or "connection" in error_message.lower():
        return (
            "⚠️ **インターネット接続を確認してください**",
            "💡 解決方法: Wi-Fiがつながっているか確認してください。"
        )
    
    if "Timeout" in error_type or "timeout" in error_message.lower():
        return (
            "⚠️ **タイムアウトエラーが発生しました**",
            "💡 解決方法: しばらく待ってから再度お試しください。"
        )
    
    # その他のエラー
    return (
        "⚠️ **エラーが発生しました**",
        f"💡 解決方法: エラー内容を開発者に連絡してください。\n\nエラー詳細: {error_message}"
    )


def handle_error(error: Exception, show_details: bool = False) -> None:
    """
    エラーを処理してStreamlitに表示
    
    Args:
        error: 発生したエラー
        show_details: 詳細を表示するかどうか
    """
    import streamlit as st
    
    error_msg, solution = get_user_friendly_error(error)
    
    st.error(error_msg)
    st.info(solution)
    
    if show_details:
        with st.expander("🔍 エラー詳細（開発者向け）"):
            st.code(str(error))
