# 🚗 ETL Importaciones SUV · Astara Intelligence

App de procesamiento de datos de importaciones de vehículos SUV del mercado peruano, basada en datos de Veritrade.

## ¿Qué hace?

- Carga datasets consolidados de Veritrade (`.xlsx` o `.csv`)
- Filtra registros de vehículos SUV
- Aplica parsers específicos por marca para extraer **MODELO**, **VERSION** y **AÑO MODELO**
- Genera un dataset limpio listo para análisis
- Permite descargar el resultado como CSV

## Marcas soportadas

KIA · HYUNDAI · VOLKSWAGEN · NISSAN · TOYOTA · HONDA · SUZUKI · MAZDA · SUBARU ·
CHEVROLET · MITSUBISHI · RENAULT · JAC · CHANGAN · GEELY · HAVAL · GREAT WALL ·
JETOUR · BYD · DFSK · SWM · JEEP · AUDI · BMW · PEUGEOT · DONGFENG · JAECOO · OMODA

## Cómo usar

1. Subí el dataset consolidado de Veritrade
2. Seleccioná las marcas a procesar
3. Hacé clic en **Procesar ETL**
4. Explorá y descargá el resultado

## Deploy local

```bash
pip install -r requirements.txt
streamlit run app_importaciones.py
```

## Stack

- [Streamlit](https://streamlit.io)
- [Pandas](https://pandas.pydata.org)
- Python 3.11+
