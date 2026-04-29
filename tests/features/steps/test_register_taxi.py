import json
import hashlib
import time
from behave import given, when, then

@given('un conductor con placa "{placa}" y id "{id_conductor}"')
def step_given_conductor(context, placa, id_conductor):
    context.placa = placa
    context.id_conductor = id_conductor
    context.timestamp = int(time.time())

@when('el conductor llega al acopio y se genera el QR')
def step_when_generate_qr(context):
    data = {
        "v": 1,
        "p": context.placa,
        "u": context.id_conductor,
        "t": context.timestamp
    }
    context.qr_json = json.dumps(data)

@then('el QR contiene un JSON válido con la placa, id y timestamp')
def step_then_validate_qr(context):
    qr_data = json.loads(context.qr_json)
    assert qr_data["p"] == context.placa
    assert qr_data["u"] == context.id_conductor
    assert isinstance(qr_data["t"], int)
    assert qr_data["v"] == 1

@when('se genera el QR')
def step_when_generate_qr_with_hash(context):
    data = {
        "v": 1,
        "p": context.placa,
        "u": context.id_conductor,
        "t": context.timestamp
    }
    # Hash simple para demo (en producción usar JWT)
    hash_str = f"{data['p']}{data['u']}{data['t']}"
    data["hash"] = hashlib.sha256(hash_str.encode()).hexdigest()
    context.qr_json = json.dumps(data)

@then('el QR incluye un campo hash para evitar duplicados')
def step_then_validate_hash(context):
    qr_data = json.loads(context.qr_json)
    assert "hash" in qr_data
    assert len(qr_data["hash"]) == 64
