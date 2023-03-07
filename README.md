# cnowind

<img src='./Protocolos/Uniandes-CNO2.png' width='500' />

## Introducción

### Acuerdo Específico 6: Convenio Marco CNO-Uniandes

#### Objetivo General

Implementar el modelo que relaciona el recurso y la potencia de plantas eólicas, así como el protocolo para el reporte de los parámetros necesarios para su ejecución, de acuerdo con las necesidades derivadas de la Resolución CREG 060 de 2019 y la Resolución CREG 148 de 2021, los Acuerdos CNO correspondientes y la demás reglamentación aplicable.

Adicionalmente, especificar los ajustes que es necesario realizar en el modelo de parque onshore, que calcula la energía mensual neta a partir de la cual se estima la Energía Firme para el Cargo por Confiabilidad (ENFICC), para que dicho modelo pueda ser usado en parques eólicos marítimos (offshore), incluyendo la componente de análisis y tratamiento de datos desarrollada en el marco del Acuerdo CNO 1319.

Por otra parte, analizar el estándar IEC 61400-12-2 y otras normas internacionales para establecer el detalle del procedimiento que se debe seguir para la medición y corrección de la velocidad del viento en góndola.

#### Alcances

1. Modelo que relaciona el recurso y la potencia en plantas eólicas. El modelo permitirá obtener la producción de la planta a partir de los parámetros técnicos de la misma, la velocidad y dirección del viento, presión, humedad y temperatura ambiente.
2. Componente de análisis y tratamiento de datos. Esta componente permitirá realizar la extrapolación por altura de la velocidad del viento, el pre-procesamiento y evaluación de los datos, y la aplicación del modelo MCP.
3. Procedimiento de ajuste del modelo de parque eólico terrestre (onshore) para que pueda usarse para parques eólicos marítimos (offshore).
4. Establecer el detalle del procedimiento para la medición y corrección de la velocidad del viento en góndola.

## Documentación

#### Protocolos
Los protocolos se encuentran en la carpeta [`Protocolos`](https://git.cno.org.co/cno/cno_wind/-/tree/main/Protocolos).

#### Memoria de Cálculos
En la carpeta [`memoria_calculos`](https://git.cno.org.co/cno/cno_wind/-/tree/main/memoria_calculos) se encuentra la documentación correspondiente a las pruebas de concepto de las metodologías recomendadas, validación con datos del caso de estudio Parque Coquito y estimación de los errores e incertidumbres.

#### Ejemplos
En la carpeta [`ejemplos`](https://git.cno.org.co/cno/cno_wind/-/tree/main/ejemplos) se encuentra el documento `CNO_Ejemplo.pdf`. Allí se presenta el ejemplo del caso de estudio Parque Coquito con la ejecución de los cuadernos `CNO_Configuracion_Sistema.ipynb` y `CNO_Protocolos.ipynb`. El ejemplo dispone de los archivos necesarios para la ejecución, así como los resultados del mismo.

#### Descargas
La descarga de todos los archivos de los cuadernos `CNO_Configuracion_Sistema.ipynb` y `CNO_Protocolos.ipynb` se alojan en la carpeta `descargas`.

## Instalación

#### Repositorio

Primero es necesario descargar los archivos de los protocolos y los aplicativos para la creación de los archivos de configuración y para correr los modelos. Los archivos se encuentran alojados en el repositorio del Consejo Nacional de Operación en [cno/cno_wind](https://git.cno.org.co/cno/cno_wind). Para [clonar](https://docs.github.com/es/repositories/creating-and-managing-repositories/cloning-a-repository) el repositorio `cno-wind` se recomienda usar el software [GitHub Desktop](https://desktop.github.com/).

Una vez haya descargado e instalado `Github Desktop`, seleccione `File` y `Clone Repository...`. En la pestaña `URL`, en el campo `URL or username/repository` escriba la dirección `https://git.cno.org.co/cno/cno_wind.git`. Seleccione la ubicación donde quiere descargar los archivos y seleccione `Clone`.

#### Distribución y Ambiente

Se recomienda instalar [Miniforge](https://github.com/conda-forge/miniforge) como ambiente para instalar Python y las librerías necesarias para la ejecución de los protocolos. Miniforge es una distribución de Python y el administrador de paquetes `conda`, permite fácilmente la configuración de ambientes y la instalación de paquetes desde el repositorio `conda-forge`.

Durante la instalación utilice las opciones recomendadas en las `Advanced Installation Options` como se muestra a continuación.

![conda-forge/miniforge](img/conda-forge.png)

Luego de descargar e instalar `Miniforge`, inicie el terminal mediante la aplicación `Miniforge Prompt`. Si la instalación se realizó de manera correcta, debe estar en el ambiente `(base)` como se muestra a continuación.

![base-env](img/base-env.png)

Se creará un ambiente específico para correr los protocolos, el cual llamaremos `cno-wind`, y se instalarán los paquetes necesarios. Con este fin abra un terminal con la aplicación `Miniforge Prompt` y desde el ambiente `(base)` **muévase al directorio donde tiene descargado los archivos del protocolo**, por ejemplo, si los tiene descargados en el escritorio:

```terminal
cd C:\usuario\Desktop\cno_wind
```

Luego cree el ambiente con el comando:

```terminal
conda env create --file environment.yml
```
Ahora, se activa dicho ambiente:

```terminal
conda activate cno-wind
```

Después de ejecutar el comando anterior, se debe estar en el ambiente correspondiente, en este caso denotado por `(cno-wind)` como se muestra en la siguiente figura.

![cno-wind-env](img/cno-wind-env.png)

Ahora se instala el kernel correspondiente al ambiente recien creado.

```terminal
python -m ipykernel install --user --name cno-wind --display-name "cno-wind"
```

Finalmente, ejecute el siguiente comando para iniciar los cuadernos.

```terminal
jupyter notebook
```

Si desea eliminar el ambiente creado, ejecute el siguiente comando:

```terminal
conda env remove -n cno-wind
```

Luego, para eliminar el kernel `cno-wind` creado, ejecute el siguiente comando:

```terminal
jupyter kernelspec remove cno-wind
```

## Licencia

GNU AFFERO GENERAL PUBLIC LICENSE v3.0, dispuesta en el archivo `LICENSE`.