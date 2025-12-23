import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

MAIN_QUEUE = "atp:queue:default"
DLQ = "atp:queue:dlq"
DELAYED_QUEUE = "atp:delayed"  # Sorted set for delayed/retries

MAX_RETRIES = 5
BASE_BACKOFF = 10  # seconds, exponential: 10, 20, 40...