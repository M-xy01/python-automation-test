import os
import threading

import yaml

_CFG = None
_LOCK = threading.Lock()


def get_config():
    global _CFG
    if _CFG is None:
        with _LOCK:
            if _CFG is None:
                path = os.path.join(os.path.dirname(__file__), "..", "config", "config.yaml")
                if not os.path.isfile(path):
                    raise FileNotFoundError(f"配置文件不存在: {path}")
                try:
                    with open(path, encoding="utf-8") as f:
                        _CFG = yaml.safe_load(f) or {}
                except yaml.YAMLError as e:
                    raise ValueError(f"配置文件格式错误: {path} - {e}")
    _expand_env(_CFG)
    return _CFG


def _expand_env(obj):
    import re
    if isinstance(obj, str):
        def repl(m):
            return os.environ.get(m.group(1), m.group(0))
        return re.sub(r'\$\{(\w+)\}', repl, obj)
    if isinstance(obj, dict):
        for k, v in obj.items():
            obj[k] = _expand_env(v)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            obj[i] = _expand_env(v)
    return obj
