Feature: Registro de conductores en acopio aeropuerto
  Como operador del aeropuerto
  Quiero registrar a los conductores mediante QR
  Para controlar el acceso y la trazabilidad

  Scenario: Registro exitoso de un conductor
    Given un conductor con placa "XYZ123" y id "driver_001"
    When el conductor llega al acopio y se genera el QR
    Then el QR contiene un JSON válido con la placa, id y timestamp

  Scenario: El QR contiene un hash de seguridad
    Given un conductor con placa "ABC456" y id "driver_002"
    When se genera el QR
    Then el QR incluye un campo hash para evitar duplicados