from datetime import datetime
from collections import deque

# Maintain a rolling window of up to 100 points in memory
_history_logs = deque(maxlen=100)

def append_history(traffic: float, waste: float):
    now = datetime.now()
    time_label = f"{now.hour:02d}:{now.minute:02d}:{now.second:02d}"
    _history_logs.append({
        "time": time_label,
        "traffic": traffic,
        "waste": waste
    })

def get_history_trends(limit=15):
    """
    Returns exact required format:
    { "timestamps": [...], "traffic": [...], "waste": [...] }
    """
    recent_logs = list(_history_logs)[-limit:]
    
    if len(recent_logs) < 5:
        return {
            "timestamps": ["00:00", "00:01", "00:02", "00:03", "00:04"],
            "traffic": [50, 50, 50, 50, 50],
            "waste": [50, 50, 50, 50, 50]
        }
    
    return {
        "timestamps": [log["time"] for log in recent_logs],
        "traffic": [log["traffic"] for log in recent_logs],
        "waste": [log["waste"] for log in recent_logs]
    }
