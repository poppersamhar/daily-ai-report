import requests
import re
import json
import os


class DeepSeekClient:
    """DeepSeek API 客户端"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY", "")
        self.base_url = "https://api.deepseek.com/chat/completions"

    def call(self, prompt: str, temperature: float = 0.7) -> str:
        """调用 DeepSeek API"""
        if not self.api_key:
            print("    [警告] 未配置 DEEPSEEK_API_KEY")
            return ""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature
        }

        try:
            resp = requests.post(
                self.base_url,
                headers=headers,
                json=data,
                timeout=60
            )
            result = resp.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"    [错误] DeepSeek API 调用失败: {e}")
            return ""

    def call_json(self, prompt: str, temperature: float = 0.7) -> dict:
        """调用 API 并解析 JSON 响应"""
        result = self.call(prompt, temperature)
        if not result:
            return {}

        try:
            # 清理 markdown 标记
            result = re.sub(r'```json\s*', '', result)
            result = re.sub(r'```\s*', '', result)
            return json.loads(result.strip())
        except json.JSONDecodeError as e:
            print(f"    [错误] JSON 解析失败: {e}")
            return {}


# 全局实例
_client = None


def get_client() -> DeepSeekClient:
    """获取全局客户端实例"""
    global _client
    if _client is None:
        _client = DeepSeekClient()
    return _client
