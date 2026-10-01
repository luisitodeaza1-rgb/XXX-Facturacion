# XXX Facturador

Sistema de facturación e inventario desarrollado en **Python**, diseñado para gestionar clientes, productos, facturas e inventario desde una aplicación de escritorio.

El proyecto está construido con una arquitectura modular, separando la interfaz gráfica, la lógica de negocio y el acceso a la base de datos.

## Características    

* Gestión de clientes
* Consulta de clientes por RNC
* Integración con DGAPI para consulta de RNC
* Gestión de productos
* Control de inventario
* Creación de facturas
* Cálculo automático de subtotal, ITBIS y total
* Generación automática de números de factura
* Historial de facturas
* Búsqueda de facturas
* Visualización del detalle de facturas
* Eliminación de facturas
* Restauración automática del inventario al eliminar una factura
* Gestión de usuarios
* Configuración de datos de la empresa
* Reportes
* Persistencia de datos mediante SQLite

## Arquitectura

```text
┌─────────────────────────────────────┐
│           XXX Facturador            │
│                                     │
│          Python + Tkinter           │
└──────────────────┬──────────────────┘
                   │
          ┌────────┴────────┐
          │                 │
          ▼                 ▼
     Services            SQLite
          │
          │ HTTP / JSON
          ▼
┌─────────────────────────────────────┐
│               DGAPI                 │
│              FastAPI                │
│                                     │
│        Consulta de información      │
│              de RNC                  │
└─────────────────────────────────────┘
```

## Tecnologías

| Tecnología | Uso                                    |
| ---------- | -------------------------------------- |
| Python     | Lenguaje principal                     |
| Tkinter    | Interfaz gráfica                       |
| SQLite     | Base de datos                          |
| SQL        | Consultas y gestión de datos           |
| FastAPI    | API externa del proyecto               |
| Pydantic   | Validación de datos en la API          |
| Requests   | Comunicación HTTP                      |
| JSON       | Intercambio de datos                   |
| Git        | Control de versiones                   |
| GitHub     | Repositorio y seguimiento del proyecto |

## Estructura del proyecto

```text
XXX Facturador/
│
├── database/
│   └── facturacion.db
│
├── Services/
│   ├── auth_service.py
│   ├── Client_services.py
│   ├── Configuracion_services.py
│   ├── Facturas_historial_services.py
│   ├── Facturas_services.py
│   ├── Product_services.py
│   ├── Reportes_services.py
│   └── RNC_services.py
│
├── views/
│   ├── Cliente.py
│   ├── Configuracion.py
│   ├── dashboard.py
│   ├── facturas.py
│   ├── facturas_historial.py
│   ├── login.py
│   ├── Product.py
│   └── Reportes.py
│
├── crear_usuario.py
├── database.py
└── Main.py
```

## Flujo de facturación

```text
Cliente
   │
   ├── Registrado ──────────────┐
   │                            │
   └── No registrado            │
          │                     │
          ▼                     │
        DGAPI                   │
          │                     │
          ▼                     │
      Información               │
      del RNC                   │
          │                     │
          └──────────┬──────────┘
                     ▼
                 Facturación
                     │
                     ▼
              Validación de
                 productos
                     │
                     ▼
               Actualización
               del inventario
                     │
                     ▼
              Registro de factura
```

## Consulta de RNC

El sistema permite introducir un RNC y determinar primero si existe como cliente registrado.

Si no está registrado, el facturador realiza una consulta a **DGAPI**.

Cuando el RNC es encontrado, sus datos pueden utilizarse para emitir la factura sin crear automáticamente un nuevo cliente en la base de datos.

Esto permite diferenciar entre:

```text
Cliente registrado
        ↓
Se utiliza su registro
```

y

```text
Particular
        ↓
Se utiliza para la factura
        ↓
No se registra automáticamente como cliente
```

## Inventario

El sistema valida el stock antes de generar una factura.

Al completar una venta:

```text
Stock disponible
        ↓
Cantidad facturada
        ↓
Stock actualizado
```

Si una factura es eliminada desde el historial, las cantidades correspondientes son restauradas automáticamente.

```text
Factura eliminada
        ↓
Detalle eliminado
        ↓
Stock restaurado
```

Las operaciones se manejan mediante transacciones para reducir el riesgo de inconsistencias en la base de datos.

## Base de datos

El sistema utiliza **SQLite**.

Principales tablas:

```text
usuarios
clientes
productos
facturas
detalle_factura
configuracion
```

La tabla `facturas` almacena tanto la relación con clientes registrados como los datos del cliente utilizados específicamente en la factura.

Esto permite conservar el nombre y RNC utilizados al momento de generar una factura.

## Instalación

Clonar el repositorio:

```text
git clone <URL_DEL_REPOSITORIO>
```

Entrar al proyecto:

```text
cd "XXX Facturador"
```

Instalar las dependencias necesarias:

```text
python -m pip install requests
```

## Ejecución

XXX Facturador utiliza DGAPI para las consultas de RNC, por lo que primero debe iniciarse la API.

### 1. Iniciar DGAPI

```text
cd "C:\Users\PC\OneDrive\Escritorio\py\proyectos\API DGII"
.\venv\Scripts\activate
uvicorn main:app --host 127.0.0.1 --port 8001
```

DGAPI quedará disponible en:

```text
http://127.0.0.1:8001
```

### 2. Iniciar XXX Facturador

En otra terminal:

```text
cd "C:\Users\PC\OneDrive\Escritorio\py\proyectos\XXX Facturador"
python Main.py
```

## Versionado

El proyecto se desarrolla progresivamente mediante versiones.

### V0.1

Primer prototipo del sistema de facturación.

### V0.2

Organización modular del proyecto.

### V0.3

Implementación de gestión de clientes.

### V0.4

Gestión de productos e inventario.

### V0.5

Implementación del sistema de facturación.

### V0.6

Implementación del historial de facturas.

### V0.7

Creación e integración de DGAPI.

### V0.8

Implementación de endpoints para consulta de RNC.

### V0.9

Comunicación entre XXX Facturador y DGAPI mediante HTTP y JSON.

### V1.0

Integración de consulta de RNC desde el módulo de clientes.

### V1.1

Implementación de facturación para particulares mediante DGAPI sin registrarlos automáticamente como clientes.

### V1.2

Modificación de la base de datos para almacenar nombre y RNC directamente en las facturas.

### V1.3

Adaptación del historial para soportar clientes registrados y particulares.

### V1.4

Implementación de eliminación de facturas y restauración automática del inventario.

### V1.5

Implementación de indicadores de facturación: cantidad de facturas, subtotal, ITBIS y total facturado.

### V1.6

Consolidación de la arquitectura y flujo actual del sistema.

## Próximas mejoras

Algunas funcionalidades consideradas para futuras versiones:

* Generación de facturas en PDF
* Exportación de reportes
* Control de costos de productos
* Cálculo de ganancias
* Mejoras en roles y permisos
* Mejoras de seguridad
* Nuevos reportes
* Optimización de la API
* Despliegue del sistema

## Estado del proyecto

**Versión actual: V1.6**

Proyecto en desarrollo continuo.

La finalidad del proyecto es seguir incorporando funcionalidades mientras aplico conocimientos de **Python, bases de datos, APIs REST, arquitectura de software, automatización y control de versiones**.

---

**Desarrollado con Python por Luis Manuel De Aza Salcedo.**
