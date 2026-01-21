"""
QRコード生成モジュール
アプリのURLからQRコードを生成
"""

import qrcode
from PIL import Image
import io
import numpy as np
from typing import Optional
import config


def generate_qr_code(url: str, box_size: int = 10, border: int = 4) -> Image.Image:
    """
    QRコードを生成
    
    Args:
        url: QRコードに含めるURL
        box_size: QRコードのセルサイズ
        border: ボーダーのサイズ
        
    Returns:
        QRコード画像
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=border,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    return img


def get_qr_code_image(url: Optional[str] = None) -> Image.Image:
    """
    アプリのQRコード画像を取得
    
    Args:
        url: アプリのURL（Noneの場合は設定から取得）
        
    Returns:
        QRコード画像
    """
    if url is None:
        url = config.get_app_url()
    
    # URLが設定されていない場合は、現在のURLを取得を試みる
    if not url:
        import streamlit as st
        try:
            # Streamlit Cloudの場合
            if hasattr(st, 'config') and hasattr(st.config, 'server'):
                server_config = st.config.server
                if hasattr(server_config, 'baseUrlPath'):
                    base_path = server_config.baseUrlPath
                    # 実際のURLを構築（簡易版）
                    # 本番環境では適切なURLを設定する必要がある
                    url = f"https://your-app-name.streamlit.app{base_path}"
        except:
            pass
    
    # URLがまだない場合はプレースホルダー
    if not url:
        url = "https://tuutihyou-app.streamlit.app"
    
    return generate_qr_code(url)


def get_qr_code_numpy(url: Optional[str] = None) -> np.ndarray:
    """
    アプリのQRコード画像をnumpy配列で取得（Streamlit表示用）
    
    Args:
        url: アプリのURL（Noneの場合は設定から取得）
        
    Returns:
        QRコード画像のnumpy配列（RGB形式）
    """
    img = get_qr_code_image(url)
    # RGBモードに変換（Streamlit表示用）
    if img.mode != 'RGB':
        img = img.convert('RGB')
    return np.array(img)


def get_high_resolution_qr_code(url: Optional[str] = None, 
                                size: tuple[int, int] = (800, 800)) -> Image.Image:
    """
    高解像度のQRコードを生成（印刷用）
    
    Args:
        url: アプリのURL
        size: 画像サイズ
        
    Returns:
        高解像度QRコード画像
    """
    qr_img = get_qr_code_image(url)
    high_res_img = qr_img.resize(size, Image.Resampling.LANCZOS)
    return high_res_img


def get_qr_code_bytes(url: Optional[str] = None, 
                      high_resolution: bool = False) -> bytes:
    """
    QRコード画像をバイト列で取得（ダウンロード用）
    
    Args:
        url: アプリのURL
        high_resolution: 高解像度版を生成するか
        
    Returns:
        画像のバイト列
    """
    if high_resolution:
        img = get_high_resolution_qr_code(url)
    else:
        img = get_qr_code_image(url)
    
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()
