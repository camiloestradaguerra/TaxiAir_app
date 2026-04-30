import streamlit as st

import requests
import random
import time
import json
from urllib.parse import quote


st.title("Simulación de Llegada de Viajeros y Asignación de Taxi (QR + Pago Wompi)")

# Todos los viajeros serán asignados al taxi TXM960
placa_taxi = "TXM960"
id_conductor = "driver_TXM960"
viajeros = [f"viajero_{n:03d}" for n in range(1, 6)]

if 'resultados' not in st.session_state:
    st.session_state['resultados'] = []

if st.button("Simular llegada de 5 viajeros"):
    st.session_state['resultados'] = []
    # Registrar el taxi TXM960 solo una vez
    payload_taxi = {"placa": placa_taxi, "id_conductor": id_conductor}
    r_taxi = requests.post("http://localhost:8000/drivers/register", json=payload_taxi)
    for i in range(5):
        viajero = viajeros[i]
        # Generar string EMVCo Bancolombia QR para pago de 25000 COP
        referencia = f"Viaje_{i+1:03d}"
        emvco_str = (
            "00020101021226500010com.bancolombia.transferencia52040000"
            "5303170540825000.005802CO5905Trans6007Medellin6304"
        )
        # Si quieres personalizar la referencia, puedes agregarla al string según el estándar
        qr_url_pago = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={quote(emvco_str)}"
        # Simular pago: 1 viajero falla
        pago_exitoso = (i != 2)
        pago_status = "APROBADO" if pago_exitoso else "FALLÓ"
        wompi_status = "APPROVED" if pago_exitoso else "REJECTED"
        st.session_state['resultados'].append({
            "viajero": viajero,
            "placa": placa_taxi,
            "id_conductor": id_conductor,
            "qr_url": qr_url_pago,
            "qr_json": emvco_str,
            "pago_status": pago_status,
            "wompi_status": wompi_status
        })

for res in st.session_state['resultados']:
    st.subheader(f"Viajero {res['viajero']} asignado a taxi {res['placa']} ({res['id_conductor']})")
    if res["qr_url"]:
        st.image(res["qr_url"], caption="QR de pago Bancolombia por $25.000 COP")
        st.code(res["qr_json"], language="text")
    st.markdown(f"**Estado de pago Wompi:** {res['pago_status']}")
    if res["pago_status"] == "FALLÓ":
        st.error("El viajero no puede abordar: pago de tasa aeroportuaria rechazado.")
    elif res["pago_status"] == "APROBADO":
        st.success("Abordaje permitido.")
    else:
        st.warning("Error en el registro del taxi.")
