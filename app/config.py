from dataclasses import dataclass
import os


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    app_host: str = os.getenv("APP_HOST", "127.0.0.1")
    app_port: int = int(os.getenv("APP_PORT", "3200"))
    allow_visitor_free_text: bool = _env_bool("ALLOW_VISITOR_FREE_TEXT", False)
    store_visitor_input: bool = _env_bool("STORE_VISITOR_INPUT", False)
    model_enabled: bool = False


settings = Settings()
