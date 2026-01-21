"""
データベースモジュール
SQLiteを使用して所見データとキーワード履歴を管理
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import os


class Database:
    """データベース管理クラス"""
    
    def __init__(self, db_path: str = "tuutihyou.db"):
        """
        データベースを初期化
        
        Args:
            db_path: データベースファイルのパス
        """
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """データベース接続を取得"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 辞書形式で結果を取得
        return conn
    
    def init_database(self):
        """データベースとテーブルを初期化"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 所見テーブル
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS shoken (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT,
                class_name TEXT,
                keywords TEXT,
                content TEXT,
                character_count INTEGER,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        
        # 既存のテーブルにclass_nameカラムを追加（マイグレーション）
        try:
            cursor.execute("ALTER TABLE shoken ADD COLUMN class_name TEXT")
        except sqlite3.OperationalError:
            # カラムが既に存在する場合はエラーを無視
            pass
        
        # キーワード履歴テーブル
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS keyword_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT,
                usage_count INTEGER DEFAULT 1,
                last_used_at TEXT,
                created_at TEXT
            )
        """)
        
        # 設定テーブル
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    # 所見関連メソッド
    
    def save_shoken(self, student_name: str, keywords: List[str], 
                   content: str, character_count: int, class_name: str = "") -> int:
        """
        所見を保存
        
        Args:
            student_name: 児童名
            keywords: キーワードリスト
            content: 所見内容
            character_count: 文字数
            class_name: クラス名（学年・組、例: "3年1組"）
            
        Returns:
            保存された所見のID
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        keywords_json = json.dumps(keywords, ensure_ascii=False)
        
        cursor.execute("""
            INSERT INTO shoken 
            (student_name, class_name, keywords, content, character_count, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (student_name, class_name, keywords_json, content, character_count, now, now))
        
        shoken_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return shoken_id
    
    def get_all_shoken(self) -> List[Dict]:
        """
        すべての所見を取得
        
        Returns:
            所見のリスト
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, student_name, class_name, keywords, content, character_count, 
                   created_at, updated_at
            FROM shoken
            ORDER BY created_at DESC
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        result = []
        for row in rows:
            result.append({
                'id': row['id'],
                'student_name': row['student_name'],
                'class_name': row['class_name'] if row['class_name'] else "",
                'keywords': json.loads(row['keywords']) if row['keywords'] else [],
                'content': row['content'],
                'character_count': row['character_count'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            })
        
        return result
    
    def get_shoken_by_class(self, class_name: str) -> List[Dict]:
        """
        指定クラスの所見を取得
        
        Args:
            class_name: クラス名
            
        Returns:
            所見のリスト
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, student_name, class_name, keywords, content, character_count, 
                   created_at, updated_at
            FROM shoken
            WHERE class_name = ?
            ORDER BY student_name, created_at DESC
        """, (class_name,))
        
        rows = cursor.fetchall()
        conn.close()
        
        result = []
        for row in rows:
            result.append({
                'id': row['id'],
                'student_name': row['student_name'],
                'class_name': row['class_name'] if row['class_name'] else "",
                'keywords': json.loads(row['keywords']) if row['keywords'] else [],
                'content': row['content'],
                'character_count': row['character_count'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            })
        
        return result
    
    def get_all_classes(self) -> List[str]:
        """
        すべてのクラス名を取得
        
        Returns:
            クラス名のリスト（重複なし）
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT DISTINCT class_name
            FROM shoken
            WHERE class_name IS NOT NULL AND class_name != ''
            ORDER BY class_name
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        return [row['class_name'] for row in rows]
    
    def get_shoken(self, shoken_id: int) -> Optional[Dict]:
        """
        指定IDの所見を取得
        
        Args:
            shoken_id: 所見ID
            
        Returns:
            所見データ（存在しない場合はNone）
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, student_name, class_name, keywords, content, character_count, 
                   created_at, updated_at
            FROM shoken
            WHERE id = ?
        """, (shoken_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row['id'],
                'student_name': row['student_name'],
                'class_name': row['class_name'] if row['class_name'] else "",
                'keywords': json.loads(row['keywords']) if row['keywords'] else [],
                'content': row['content'],
                'character_count': row['character_count'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
        return None
    
    def update_shoken(self, shoken_id: int, student_name: str, 
                     keywords: List[str], content: str, character_count: int, class_name: str = ""):
        """
        所見を更新
        
        Args:
            shoken_id: 所見ID
            student_name: 児童名
            keywords: キーワードリスト
            content: 所見内容
            character_count: 文字数
            class_name: クラス名
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        keywords_json = json.dumps(keywords, ensure_ascii=False)
        
        cursor.execute("""
            UPDATE shoken
            SET student_name = ?, class_name = ?, keywords = ?, content = ?, 
                character_count = ?, updated_at = ?
            WHERE id = ?
        """, (student_name, class_name, keywords_json, content, character_count, now, shoken_id))
        
        conn.commit()
        conn.close()
    
    def delete_shoken(self, shoken_id: int):
        """
        所見を削除
        
        Args:
            shoken_id: 所見ID
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM shoken WHERE id = ?", (shoken_id,))
        
        conn.commit()
        conn.close()
    
    # キーワード履歴関連メソッド
    
    def add_keyword_history(self, keywords: List[str]):
        """
        キーワード履歴を追加（使用回数をカウント）
        
        Args:
            keywords: キーワードリスト
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        for keyword in keywords:
            # 既存のキーワードを確認
            cursor.execute("""
                SELECT id, usage_count FROM keyword_history WHERE keyword = ?
            """, (keyword,))
            
            row = cursor.fetchone()
            
            if row:
                # 既存の場合は使用回数を増やす
                cursor.execute("""
                    UPDATE keyword_history
                    SET usage_count = usage_count + 1, last_used_at = ?
                    WHERE keyword = ?
                """, (now, keyword))
            else:
                # 新規の場合は追加
                cursor.execute("""
                    INSERT INTO keyword_history (keyword, usage_count, last_used_at, created_at)
                    VALUES (?, ?, ?, ?)
                """, (keyword, 1, now, now))
        
        conn.commit()
        conn.close()
    
    def get_popular_keywords(self, limit: int = 10) -> List[Dict]:
        """
        よく使われるキーワードを取得
        
        Args:
            limit: 取得件数
            
        Returns:
            キーワードのリスト（使用回数順）
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT keyword, usage_count, last_used_at
            FROM keyword_history
            ORDER BY usage_count DESC, last_used_at DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        result = []
        for row in rows:
            result.append({
                'keyword': row['keyword'],
                'usage_count': row['usage_count'],
                'last_used_at': row['last_used_at']
            })
        
        return result
    
    # 設定関連メソッド
    
    def get_setting(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        設定値を取得
        
        Args:
            key: 設定キー
            default: デフォルト値
            
        Returns:
            設定値（存在しない場合はdefault）
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return row['value']
        return default
    
    def set_setting(self, key: str, value: str):
        """
        設定値を保存
        
        Args:
            key: 設定キー
            value: 設定値
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO settings (key, value)
            VALUES (?, ?)
        """, (key, value))
        
        conn.commit()
        conn.close()
