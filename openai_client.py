"""
OpenAI API連携モジュール
所見文の生成を行う
"""

from typing import List, Optional
import openai
from openai import OpenAI
import config
import error_handler


class OpenAIClient:
    """OpenAI APIクライアント"""
    
    def __init__(self):
        """クライアントを初期化"""
        api_key = config.get_openai_api_key()
        if not api_key:
            raise ValueError("OpenAI APIキーが設定されていません")
        
        self.client = OpenAI(api_key=api_key)
        self.model = config.get_openai_model()
    
    def generate_shoken(self, keywords: List[str], target_length: int = 200, grade_level: str = "低学年") -> str:
        """
        所見文を生成
        
        Args:
            keywords: キーワードリスト
            target_length: 目標文字数
            grade_level: 学年（"低学年"、"中学年"、"高学年"）
            
        Returns:
            生成された所見文
        """
        # プロンプトを構築
        keywords_text = "、".join(keywords) if keywords else "一般的な特徴"
        
        # 学年に応じた表現のガイド
        grade_guidance = self._get_grade_guidance(grade_level)
        
        prompt = f"""小学校の通知表の所見文を作成してください。

学年: {grade_level}
児童の特徴・キーワード: {keywords_text}

【所見の構成】
以下の4つのセクションで構成してください：

①書き出し（全体の様子）
子どもの学校生活全般での雰囲気を描写してください。

②学習面の様子
各教科の取り組みの様子を具体的に描写してください。具体的な授業場面や学習内容を含めると良いでしょう。

③生活面の様子
あいさつや掃除・係活動・人間関係など、生活面での様子を具体的に描写してください。

④今後の期待
今後に向けた目標や期待を温かく伝えてください。

【要件】
- 文字数は約{target_length}文字程度（{target_length - 20}文字から{target_length + 20}文字の範囲）
- 具体的で温かみのある表現を使用
- 否定的な表現は避け、前向きな表現を心がける
- 4つのセクションを自然につなげて、一つの文章として完成させる

【表現のポイント】
- 「〜な姿が見られます」「〜な姿が見られ、感心します」などの自然な表現を使用
- 「〜ところが素敵です」「〜ことが素晴らしいです」などの温かい表現を使用
- 「称賛します」などの硬い表現は避ける
- 児童の成長や努力を具体的に描写する
- 教師が温かく見守っている印象を与える表現にする

{grade_guidance}

所見文:"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """あなたは経験豊富な小学校教師です。児童の成長を温かく見守り、適切な所見文を作成します。

所見文は必ず以下の4つのセクションで構成してください：
①書き出し（全体の様子）
②学習面の様子
③生活面の様子
④今後の期待

各セクションを自然につなげて、一つの文章として完成させてください。

表現において、以下を積極的に使用してください：
- 「〜な姿が見られます」「〜な姿が見られ、感心します」
- 「〜ところが素敵です」「〜ことが素晴らしいです」
- 「〜に取り組む姿が印象的です」「〜を大切にしています」
- 「〜ができるようになりました」「〜を意識して取り組んでいます」

避けるべき表現：
- 「称賛します」「賞賛します」などの硬い表現
- 過度に形式的な表現

温かく、自然で、児童の成長を具体的に描写する所見文を作成してください。"""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            generated_text = response.choices[0].message.content.strip()
            
            # 文字数調整
            adjusted_text = self._adjust_length(generated_text, target_length)
            
            return adjusted_text
            
        except Exception as e:
            error_handler.handle_error(e)
            raise
    
    def _adjust_length(self, text: str, target_length: int) -> str:
        """
        文字数を調整
        
        Args:
            text: 元のテキスト
            target_length: 目標文字数
            
        Returns:
            調整されたテキスト
        """
        current_length = len(text)
        
        # 目標文字数の範囲内ならそのまま返す
        if target_length - 20 <= current_length <= target_length + 20:
            return text
        
        # 短すぎる場合は補足を追加
        if current_length < target_length - 20:
            # もう一度生成を試みる（簡易版：末尾に補足）
            # 実際の実装では、プロンプトを調整して再生成する方が良い
            return text
        
        # 長すぎる場合は要約
        if current_length > target_length + 20:
            # 文の区切りで切り詰める
            sentences = text.split('。')
            result = ""
            for sentence in sentences:
                if sentence:
                    if len(result + sentence + '。') <= target_length + 20:
                        result += sentence + '。'
                    else:
                        break
            
            if result:
                return result
            else:
                # フォールバック：文字数で切り詰め
                return text[:target_length + 20] + '...'
        
        return text
    
    def _get_grade_guidance(self, grade_level: str) -> str:
        """
        学年に応じた表現のガイドを取得
        
        Args:
            grade_level: 学年
            
        Returns:
            ガイドテキスト
        """
        if grade_level == "低学年":
            return """【低学年向けの表現】
- 「入学して間もない頃は〜でしたが、今では〜」などの成長の過程を描写
- 「〜しようとする姿」「〜できるようになってきました」など、成長を感じられる表現
- 「自分でできた！」という前向きな体験を大切にする表現
- 具体的な場面（ひらがなの練習、ランドセルの片付けなど）を含める"""
        
        elif grade_level == "中学年":
            return """【中学年向けの表現】
- 「新しい教科や学習内容にも積極的に取り組み」など、学習への意欲を表現
- 「自分から学ぼうとする姿」「探求心を活かし」など、主体的な学びを描写
- 「自分で時間を見ながら行動」「目標を立てて努力」など、自律性を表現
- 具体的な学習内容（理科の観察、算数のグラフなど）や活動（給食当番、グループ活動など）を含める"""
        
        elif grade_level == "高学年":
            return """【高学年向けの表現】
- 「意欲を持って取り組み」「チャレンジ精神がしっかりと育っています」など、高学年らしい意欲を表現
- 「リーダーの自覚を持って」「責任を持って取り組んでいます」など、リーダーシップを描写
- 「自分で考えて工夫・努力ができる才能」など、高学年としての成長を表現
- 具体的な活動（委員会活動、作品づくり、掃除活動など）を含める
- 卒業後への期待も含める（高学年の場合）"""
        
        else:
            return ""
