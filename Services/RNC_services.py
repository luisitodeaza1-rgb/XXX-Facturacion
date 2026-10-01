import requests
from bs4 import BeautifulSoup


URL_DGII = (
    "https://dgii.gob.do/app/WebApps/ConsultasWeb2/"
    "ConsultasWeb/consultas/rnc.aspx"
)


def consultar_rnc(rnc):

    rnc = rnc.replace("-", "").replace(" ", "").strip()

    if not rnc:
        raise ValueError("Debe introducir un RNC.")

    if not rnc.isdigit():
        raise ValueError(
            "El RNC debe contener solamente números."
        )

    session = requests.Session()

    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/136.0.0.0 Safari/537.36"
        )
    })

    try:

        respuesta = session.get(
            URL_DGII,
            timeout=15
        )

        respuesta.raise_for_status()

        soup = BeautifulSoup(
            respuesta.text,
            "html.parser"
        )

        formulario = soup.find("form")

        if not formulario:
            raise RuntimeError(
                "No se pudo encontrar el formulario de consulta de la DGII."
            )

        datos = {}

        for campo in formulario.find_all(
            ["input", "select", "textarea"]
        ):

            nombre = campo.get("name")

            if not nombre:
                continue

            if campo.name == "select":

                opcion = campo.find(
                    "option",
                    selected=True
                )

                datos[nombre] = (
                    opcion.get("value", "")
                    if opcion
                    else ""
                )

            elif campo.get("type") in (
                "submit",
                "button"
            ):

                continue

            else:

                datos[nombre] = campo.get(
                    "value",
                    ""
                )

        # Buscar automáticamente el campo
        # relacionado con RNC/Cédula.
        campo_rnc = None

        for campo in formulario.find_all("input"):

            nombre = (
                campo.get("name", "")
                or ""
            ).lower()

            identificador = (
                campo.get("id", "")
                or ""
            ).lower()

            if (
                "rnc" in nombre
                or "rnc" in identificador
                or "cedula" in nombre
                or "cedula" in identificador
            ):

                campo_rnc = campo.get("name")

                break

        if not campo_rnc:

            raise RuntimeError(
                "La DGII cambió la estructura de su formulario "
                "y no se encontró el campo RNC."
            )

        datos[campo_rnc] = rnc

        # Intentamos localizar el botón de búsqueda.
        boton = None

        for elemento in formulario.find_all(
            ["input", "button"]
        ):

            texto = (
                elemento.get("value", "")
                or elemento.get_text(" ", strip=True)
            ).lower()

            if (
                "buscar" in texto
                or "consultar" in texto
            ):

                boton = elemento

                break

        if boton:

            nombre_boton = boton.get("name")

            if nombre_boton:

                datos[nombre_boton] = (
                    boton.get("value", "Buscar")
                )

        respuesta = session.post(
            URL_DGII,
            data=datos,
            timeout=15
        )

        respuesta.raise_for_status()

        soup = BeautifulSoup(
            respuesta.text,
            "html.parser"
        )

        texto = soup.get_text(
            " ",
            strip=True
        )

        if "no encontrado" in texto.lower():

            return None

        if "no existe" in texto.lower():

            return None

        if "no se encontraron" in texto.lower():

            return None

        resultado = extraer_datos_resultado(
            soup,
            rnc
        )

        return resultado

    except requests.RequestException as error:

        raise RuntimeError(
            "No fue posible comunicarse con la DGII."
        ) from error


def extraer_datos_resultado(
    soup,
    rnc
):

    texto = soup.get_text(
        "\n",
        strip=True
    )

    resultado = {
        "rnc": rnc,
        "nombre_empresa": "",
        "nombre_comercial": "",
        "actividad_economica": "",
        "regimen": "",
        "estado": "",
        "administracion_local": ""
    }

    lineas = [
        linea.strip()
        for linea in texto.splitlines()
        if linea.strip()
    ]

    etiquetas = {
        "Nombre/Razón Social": "nombre_empresa",
        "Nombre / Razón Social": "nombre_empresa",
        "Nombre Comercial": "nombre_comercial",
        "Actividad Económica": "actividad_economica",
        "Régimen de Pago": "regimen",
        "Régimen": "regimen",
        "Estado": "estado",
        "Administración Local": "administracion_local"
    }

    for indice, linea in enumerate(lineas):

        for etiqueta, clave in etiquetas.items():

            if linea.lower() == etiqueta.lower():

                if indice + 1 < len(lineas):

                    resultado[clave] = (
                        lineas[indice + 1]
                    )

    # Si no encontramos ningún dato,
    # consideramos que la respuesta no pudo
    # ser interpretada correctamente.
    datos_encontrados = any(
        resultado[clave]
        for clave in (
            "nombre_empresa",
            "nombre_comercial",
            "actividad_economica",
            "regimen",
            "estado"
        )
    )

    if not datos_encontrados:

        return None

    return resultado