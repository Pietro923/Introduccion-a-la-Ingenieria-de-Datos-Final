# 🎬 Proyecto de Finalización de curso Introduccion a la Ingenieria de Datos

Este proyecto implementa un pipeline completo de MLOps para construir un sistema de recomendación de películas. El flujo de trabajo integra múltiples tecnologías:
- **Airbyte** para ingestión de datos
- **DBT** para transformación
- **Dagster** para orquestación
- **MLflow** para experimentación y seguimiento de modelos

## 📋 Tabla de Contenidos
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Arquitectura](#-arquitectura)
  - [1. Instalar Conda](#1-instalar-conda)
  - [2. Instalar Docker Desktop](#2-instalar-docker-desktop)
  - [3. Instalar y Configurar Airbyte](#3-instalar-y-configurar-airbyte)
  - [4. Configurar Conexiones en Airbyte](#4-configurar-conexiones-en-airbyte)
  - [5. Levantar Docker Compose](#5-levantar-docker-compose)
  - [6. Instalar y Configurar DBT](#6-instalar-y-configurar-dbt)
  - [7. Integrar con Dagster](#7-integrar-con-dagster)
  - [8. Configurar MLflow](#8-configurar-mlflow)
- [Ejecución del Pipeline](#-ejecución-del-pipeline)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Problemas](#-Problemas-que-tuve)

## 🛠 Tecnologías Utilizadas

| Tecnología | Función |
|------------|---------|
| **Python + Conda** | Gestión de entorno y dependencias |
| **Docker + Docker Compose** | Containerización y orquestación de servicios |
| **Airbyte** | Extracción y carga de datos (EL) |
| **DBT** | Transformación de datos (T) |
| **Dagster** | Orquestación del pipeline |
| **MLflow** | Seguimiento de experimentos ML |
| **PostgreSQL** | Base de datos |

## 🏗 Arquitectura

```
Fuente de Datos           Pipeline MLOps                Resultados
┌───────────────┐         ┌────────────────────────┐    ┌───────────────┐
│  movies.csv   │         │                        │    │               │
│  critic_      │─ ─ ─ ─ ▶│      ┌─────────┐      │    │   Sistema de  │
│  reviews.csv  │         │      │ Airbyte │      │    │ Recomendación │
│  user_        │         │      └────┬────┘      │    │  de Películas │
│  reviews.csv  │         │           │           │    │               │
└───────────────┘         │      ┌────▼────┐      │    └───────┬───────┘
                          │      │   DBT   │      │            │
                          │      └────┬────┘      │            │
                          │           │           │    ┌───────▼───────┐
                          │      ┌────▼────┐      │    │               │
                          │      │ Dagster │      │    │    MLflow     │
                          │      └────┬────┘      │    │  Dashboard    │
                          │           │           │    │               │
                          │      ┌────▼────┐      │    └───────────────┘
                          │      │ MLflow  │      │
                          │      └─────────┘      │
                          │                        │
                          └────────────────────────┘
```

## 🛠️ Instalación Paso a Paso

### 1. Instalar Conda

<img src="anaconda.png" alt="Anaconda Web" width="600">

Conda se utiliza para gestionar el entorno de Python y las dependencias:

#### Windows:
```
# 1. Descargar el instalador
   - https://www.anaconda.com/download
   - Se coloca el correo para recibir el link al instalador.

# 2. Ejecutar el instalador (GUI)
# - Seleccionar "Install for all users"
# - Mantener la ruta de instalación predeterminada
# - Marcar la opción "Add Miniconda to my PATH environment variable"
# - Clic en "Install"

# 3. Verificar la instalación (en Windows PowerShell)
      conda --version
```

### 2. Instalar Docker Desktop

Docker y Docker Compose son necesarios para ejecutar los contenedores:

#### Windows:
1. Descargar Docker Desktop desde [docker.com](https://www.docker.com/products/docker-desktop)
2. Ejecutar el instalador y seguir las instrucciones
3. Asegurarse de que WSL 2 esté habilitado (se solicitará durante la instalación) 
4. Reiniciar el sistema después de la instalación
5. Verificar la instalación:
```bash
docker --version
docker-compose --version
```

### 3. Instalar y Configurar Airbyte

Airbyte se utiliza para la extracción y carga de datos:

```bash
# 1. Descargar la última versión de abctl. desde: https://github.com/airbytehq/abctl/releases/tag/v0.24.0
# 2. Extraer el archivo zip a la ubicación que prefiera. Esto creará una carpeta con el ejecutable abctl y otros archivos necesarios.
# 3. Copie la ruta del archivo, y agregarla en las variables de entorno.
# 4. Verifique que abctl esté instalado correctamente.
      abctl version
# 5. Ejecutar Docker
# 6. Instalar Airbyte.
      abctl local install
# 7. Obtener la contraseña predeterminada.
      abctl local credentials
# 8. Ir a localhost:8000 y colocar dicha contraseña para ingresar.
```

### 4. Configurar Conexiones en Airbyte

Configurar las fuentes de datos y destinos en Airbyte:

#### Añadir origen de datos (Source):
1. En la interfaz de Airbyte, seleccionar "Sources" > "New source"
2. Seleccionar "File" como tipo de origen
3. Configurar:
   - Nombre: "Movies Dataset"
   - URL: Añadir la URL de los archivos desde el repositorio:
     - `https://github.com/dodobeatle/dataeng-datos/raw/main/movies.csv`
     - `https://github.com/dodobeatle/dataeng-datos/raw/main/critic_reviews.csv`
     - `https://www.dropbox.com/scl/fi/9vtdm3nvim0kepi00qlw6/user_reviews.csv?rlkey=97v0g535pjgdjxez72ea2hcvy&st=soqqnor8&dl=0`
   - Formato: CSV
   - Configuración del parser: Dejar los valores predeterminados
4. Hacer clic en "Set up source"

#### Añadir destino (Destination):
1. Seleccionar "Destinations" > "New destination"
2. Seleccionar "PostgreSQL" como tipo de destino
3. Configurar:
   - Nombre: "PostgreSQL"
   - Host: `192.168.1.3`
   - Puerto: 5432
   - Usuario: beelbonacossa@gmail.com
   - Base de datos: mlops
   - Schema: target
4. Hacer clic en "Test and Save"

#### Crear conexión:
1. Ir a "Connections" > "New connection"
2. Seleccionar:
   - Source: "movies.csv", "critic_reviews.csv", "user_reviews.csv"
   - Destination: "PostgreSQL"
3. Configurar:
   - Frecuencia de sincronización: 24hs
   - Modo de destino: Raw data (no deduplication)
4. Hacer clic en "Set up connection"
5. Ejecutar la sincronización manualmente haciendo clic en "Sync now"

### 5. Levantar Docker Compose

Para iniciar los servicios adicionales del proyecto:

```bash
# 1. Navegar al directorio example_compose_2
cd example_compose_2

# 2. Levantar los servicios con Docker Compose
docker-compose up -d

# 3. Verificar que todos los contenedores estén funcionando
docker ps

# Esto iniciará:
# - nginx
# - postgres_db
# - pg_admin
# - mysql_db
```

### 6. Instalar y Configurar DBT

DBT (Data Build Tool) se utiliza para transformar los datos:

```bash
# 1. Crear y activar un entorno Conda específico para DBT
conda create --name airbyte_env python=3.9 numpy scikit-learn pandas seaborn matplotlib
conda activate airbyte_env

# 2. Instalar DBT y luego con el adaptador PostgreSQL
pip install dbt-core
pip install dbt-postgres

# 3. Inicializar un proyecto DBT (si no existe)
dbt init dbt_testing

# 4. Configurar el perfil de conexión
# Editar ~/.dbt/profiles.yml
# 5. Probar la conexión
dbt debug

# 6. Crear modelos para transformar los datos
# crear los archivos dbt_testing/models/
  - movies.sql
  - movies_users.sql
  - critic_reviews.sql
  - review_stats.sql
  - user_critic_reviews.sql
  - user_reviews.sql

# 7. Configurar correctamente el schema.yml
    version: 2
    sources:
    - name: raw_data
      description: "Raw data from the mlops project"
      database: mlops
      schema: target
      tables:
        - name: movies
        - name: user_reviews
        - name: critic_reviews
```

### 7. Integrar con Dagster

Dagster orquesta el flujo de trabajo entre Airbyte, DBT y MLflow:

```bash
# 0. Haber instalado conda install -c conda-forge dagster=1.9.1 en el airbyte_env.

# 1. Crear el proyecto.
dagster project scaffold --name dg_testing

# 2. Instalar dependencias
poetry add dagster_airbyte
pip install dagster-dbt

# 3. Configurar "__init__", "definitions", Assets y Resources.

# 4. Iniciar el servicio de Dagster (si no está en el Docker Compose)
dagster dev
```

### 8. Configurar MLflow

MLflow se utiliza para registrar y visualizar experimentos:

```bash
# 1. Acceder a la interfaz web de MLflow
# Navegar a: http://localhost:5000

# 2. Verificar que los experimentos se registren correctamente
# Después de ejecutar el pipeline de Dagster, deberías ver experimentos en la interfaz de MLflow
```

## 🚀 Ejecución del Pipeline

Para ejecutar el pipeline completo:

1. Asegurarse de que todos los servicios estén en funcionamiento:
   - Airbyte (http://localhost:8000)
   - Dagster (http://localhost:3000)
   - MLflow (http://localhost:5000)
   - PostgreSQL (puerto 5432)

2. Ejecutar la sincronización de datos en Airbyte:
   - Acceder a la interfaz de Airbyte
   - Ir a "Connections"
   - Seleccionar la conexión creada
   - Hacer clic en "Sync now"

3. Ejecutar el pipeline de Dagster:
   - Acceder a la interfaz de Dagster (http://localhost:3000)
   - Ir a "Assets"
   - Hacer clic en "Materialize all"

5. Visualizar los resultados en MLflow:
   - Acceder a la interfaz de MLflow (http://localhost:5000)
   - Explorar los experimentos y modelos registrados
   - Revisar las métricas, parámetros y artefactos

## 📂 Estructura del Proyecto

```
dg_testing/
├── example_compose_2/            # Configuración Docker Compose.
│   ├── docker-compose.yml        # Servicios para MLOps (Nginx, Postgres_db, Pg_admi, Mysql_db, MLflow)
│   └── .env                      # Credenciales de uso
├── dbt-testing/                  # Proyecto DBT
│   ├── models/                   # Modelos SQL de transformación
│   ├── dbt_project.yml           # Configuración del proyecto DBT
│
├── definitions.py                # Definición del pipeline
├── dbt.integration.yml           # Conexion con dbt
│
├── resources/
│   └── __init__.py               # Conexiones con la base de datos.
│
├── Assets/                       # Los Assets necesarios para el proyecto.
│   ├── airbyte.py      
│   ├── dbt.py      
│   ├── model_helper.py
│   └── train_model.py
```

## 🔧 Problemas que tuve:

1. **Error con Docker**
   - Docker si bien se instalo de forma correcta, fallaba mostrando cualquier cantidad de errores, leyendos foros y viendo videos me di cuenta que necesitaba tener instalado un sub-sistema Linux en Windows para hacerlo andar: 'wsl --install'
   - Instalación de Airbyte: Esta instalación en teoria deberia demorarse 15/30 minutos, se demoro más de 3 horas por algun motivo, fui comprobando los logs de la instalación por lo que podia ver que efectivamente se estaba instalando pero de forma muy lenta. Verifique       que no era mi conexion, y mis componentes estaban dentro de los recomendados.

2. **Errores con Dagster**
   - Almacenamiento: Comence el curso con 200 GB libres, pero Airbyte, y los demas programas empezaron llenar mi disco (SSD de 480 GB), ahora mismo tengo 30 GB disponibles unicamente.
   - Errores de codificacion y tipeo, en varias ocasiones no funcionaba la conexion con Airbyte o postgress por errores mios por malos tipeos, faltaba una "S" o sobraban letras.
   - Ahora mismo no puedo correr el proyecto debido a la falta de espacio, tambien de potencia, en un testeo me fallo Dagster con un error que indicaba que los componentes no eran suficientemente potentes para la ejecucion.

2. **Errores Generales**
   - Debi haber elegido un Source con información mas ligero.

---

## 🔧 Conclusiones:

Aprendi mucho durante este curso, no tengo dudas que cuando se presente en un futuro la necesidad reveré estas clases y repasare los apuntes que hice de las mismas. 
El profesor Pedro fue Impecable durante cada clase, espero tenerlo en alguna materia mas adelante. 

---
Proyecto Final del Taller de Introduccion a la Ingenieria de Datos.
