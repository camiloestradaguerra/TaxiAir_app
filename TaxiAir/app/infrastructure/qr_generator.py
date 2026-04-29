import json
import hashlib
from urllib.parse import quote

def generate_qr_json(placa: str, id_conductor: str, timestamp: int, include_hash: bool = False) -> dict:
    data = {
        "v": 1,
        "p": placa,
        "u": id_conductor,
        "t": timestamp
    }
    if include_hash:
        hash_str = f"{placa}{id_conductor}{timestamp}"
        data["hash"] = hashlib.sha256(hash_str.encode()).hexdigest()
    return data

def generate_qr_url(qr_json: dict) -> str:
    # Usar API pública para demo
    data_str = json.dumps(qr_json, separators=(",", ":"))
    url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={quote(data_str)}"
    return url
