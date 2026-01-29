# YouTube 频道配置
YOUTUBE_CHANNELS = {
    "UCSHZKyawb77ixDdsGog4iWA": "Lex Fridman",
    "UCbfYPyITQ-7l4upoX8nvctg": "Two Minute Papers",
    "UCNF5-lNi7Kqj2gYtGSz_GVQ": "AI Explained",
    "UCWN3xxRkmTPmbKwht9FuE5A": "Andrej Karpathy",
}

# 时长限制（秒）
MAX_DURATION_SECONDS = 30 * 60  # 30分钟

# 知名度权重
CHANNEL_WEIGHTS = {
    "Lex Fridman": 100,
    "Andrej Karpathy": 95,
    "Two Minute Papers": 85,
    "AI Explained": 80,
}

ENTITY_WEIGHTS = {
    "openai": 50, "gpt-5": 50, "gpt-4": 40, "gpt": 30,
    "anthropic": 45, "claude": 45,
    "google": 40, "deepmind": 40, "gemini": 40,
    "nvidia": 35, "meta": 30,
    "sam altman": 50, "altman": 40,
    "andrej karpathy": 45, "karpathy": 40,
    "dario amodei": 40, "amodei": 35,
    "jensen huang": 35, "ilya sutskever": 45,
    "scaling": 25, "transformer": 25, "agent": 25, "sota": 30,
}

# 实体识别模式
ENTITY_PATTERNS = [
    (r"openai", "OpenAI", "company"),
    (r"gpt-?[45o]", "GPT", "company"),
    (r"anthropic", "Anthropic", "company"),
    (r"claude", "Claude", "company"),
    (r"google|deepmind|gemini", "Google", "company"),
    (r"nvidia", "NVIDIA", "company"),
    (r"meta\s*ai|llama", "Meta AI", "company"),
    (r"sam\s*altman", "Sam Altman", "person"),
    (r"karpathy", "Karpathy", "person"),
    (r"dario", "Dario Amodei", "person"),
    (r"jensen", "Jensen Huang", "person"),
    (r"ilya", "Ilya Sutskever", "person"),
]
