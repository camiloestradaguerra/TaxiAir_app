import streamlit as st
import requests
import time

# Llaves de sandbox Wompi
WOMPI_PUBLIC_KEY = 'pub_test_Q5yS9s9vG9eecmS7mN6F93C6X3H9K'
# Para polling no necesitas la privada en el frontend

st.title("Simulador de Pago QR Wompi (Bancolombia/Nequi)")

st.info("Completa los datos y genera un QR interoperable para pago con Nequi/Bancolombia. Luego paga y consulta el estado.")

with st.form("form_pago"):
    nombre = st.text_input("Nombre del pasajero", "")
    referencia = st.text_input("Referencia del viaje", "Viaje_001")
    monto = st.number_input("Valor del viaje (COP)", min_value=1000, value=1000, step=1000)
    submit = st.form_submit_button("Generar QR de pago")

if submit and nombre and referencia and monto:
    st.session_state['generado'] = False
    st.session_state['transaction_id'] = None
    st.session_state['checkout_url'] = None
    st.session_state['qr_url'] = None
    # Crear transacción en Wompi
    url = "https://sandbox.wompi.co/v1/transactions"
    data = {
        "amount_in_cents": int(monto) * 100,
        "currency": "COP",
        "customer_email": f"{nombre.lower().replace(' ','.')}@mail.com",
        "reference": referencia,
        "payment_method": {
            "type": "QR",
            "provider": "BANCOLOMBIA"
        }
    }
    headers = {"Authorization": f"Bearer {WOMPI_PUBLIC_KEY}", "Content-Type": "application/json"}
    r = requests.post(url, json=data, headers=headers)
    if r.status_code == 201:
        resp = r.json()
        st.session_state['generado'] = True
        st.session_state['transaction_id'] = resp['data']['id']
        st.session_state['checkout_url'] = resp['data']['payment_method']['extra']['async_payment_url']
        st.session_state['qr_url'] = resp['data']['payment_method']['extra']['qr_url']
        st.success("Transacción creada. Escanea el QR para pagar.")
    else:
        st.error(f"Error creando transacción: {r.text}")

if st.session_state.get('generado', False):
    st.markdown(f"**Referencia:** {referencia}")
    st.markdown(f"**Monto:** ${monto:,.0f} COP")
    st.image(st.session_state['qr_url'], caption="Escanea con Nequi/Bancolombia")
    st.markdown(f"[Abrir pago en app bancaria]({st.session_state['checkout_url']})")
    st.info("Realiza el pago y luego consulta el estado.")
    if st.button("Consultar estado del pago"):
        tid = st.session_state['transaction_id']
        url = f"https://sandbox.wompi.co/v1/transactions/{tid}"
        r = requests.get(url)
        if r.status_code == 200:
            status = r.json()['data']['status']
            st.markdown(f"**Estado actual:** {status}")
            if status == "APPROVED":
                st.success("¡Pago aprobado! El pasajero puede abordar.")
            elif status == "DECLINED":
                st.error("Pago rechazado. Intenta de nuevo.")
            else:
                st.warning("Pago pendiente o en proceso.")
        else:
            st.error(f"Error consultando estado: {r.text}")
