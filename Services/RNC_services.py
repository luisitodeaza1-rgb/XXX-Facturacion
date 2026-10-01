import requests


# ============================================================
# CONFIGURACIÓN
# ============================================================

DGAPI_URL = "http://127.0.0.1:8001"


# ============================================================
# CONSULTA DE RNC
# ============================================================

def consultar_rnc(rnc):
    """
    Consulta la información de un RNC a través de DGAPI.

    Args:
        rnc (str): Número de RNC a consultar.

    Returns:
        dict | None:
            Diccionario con la información del contribuyente
            si el RNC fue encontrado.
            None si el RNC no existe.

    Raises:
        ValueError:
            Si el RNC está vacío o contiene caracteres inválidos.

        RuntimeError:
            Si no es posible comunicarse con DGAPI o
            la respuesta recibida no es válida.
    """

    # --------------------------------------------------------
    # Limpiar y validar RNC
    # --------------------------------------------------------

    rnc = str(rnc).replace("-", "").replace(" ", "").strip()

    if not rnc:
        raise ValueError("Debe introducir un RNC.")

    if not rnc.isdigit():
        raise ValueError(
            "El RNC debe contener solamente números."
        )

    # --------------------------------------------------------
    # Consultar DGAPI
    # --------------------------------------------------------

    url = f"{DGAPI_URL}/rnc/{rnc}"

    try:
        respuesta = requests.get(
            url,
            timeout=15
        )

        respuesta.raise_for_status()

    except requests.RequestException as error:
        raise RuntimeError(
            "No fue posible comunicarse con DGAPI. "
            "Verifique que DGAPI esté ejecutándose "
            "en el puerto 8001."
        ) from error

    # --------------------------------------------------------
    # Procesar respuesta JSON
    # --------------------------------------------------------

    try:
        datos = respuesta.json()

    except ValueError as error:
        raise RuntimeError(
            "DGAPI devolvió una respuesta inválida."
        ) from error

    # --------------------------------------------------------
    # Verificar si el RNC fue encontrado
    # --------------------------------------------------------

    if not datos.get("encontrado", False):
        return None

    # --------------------------------------------------------
    # Convertir respuesta de DGAPI al formato utilizado
    # por XXX Facturador
    # --------------------------------------------------------

    resultado = {
        "rnc": datos.get("rnc", rnc),
        "nombre_empresa": datos.get("nombre", ""),
        "nombre_comercial": datos.get(
            "nombre_comercial",
            ""
        ),
        "actividad_economica": datos.get(
            "actividad_economica",
            ""
        ),
        "regimen": datos.get(
            "regimen_pago",
            ""
        ),
        "estado": datos.get(
            "estado",
            ""
        ),
        "administracion_local": "",
        "fecha_inicio": datos.get(
            "fecha_inicio",
            ""
        )
    }

    return resultado