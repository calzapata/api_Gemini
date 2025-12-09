import os
import base64
from google import genai

client = genai.Client(api_key="")
MODEL_NAME = "gemini-2.5-flash"

total_general = 0

def procesar_carpeta_pdf(ruta_carpeta, prompt_extraccion):
    global total_general
    total_general = 0
    
    for archivo in os.listdir(ruta_carpeta):
        if archivo.lower().endswith(".pdf"):
            ruta_pdf = os.path.join(ruta_carpeta, archivo)
            print(f"\n📄 Procesando: {archivo}")
            extraer_datos_pdf(ruta_pdf, prompt_extraccion)
    
    print(f"\n💰 TOTAL GENERAL DE TODAS LAS FACTURAS: ${total_general}")


def extraer_datos_pdf(ruta_pdf, prompt_extraccion):
    global total_general
    try:
        with open(ruta_pdf, "rb") as f:
            pdf_bytes = f.read()
            pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                {"text": prompt_extraccion},
                {
                    "inline_data": {
                        "mime_type": "application/pdf",
                        "data": pdf_base64
                    }
                }
            ]
        )

        print("\n--- Resultado IA ---")
        print(response.text)
        print("--------------------\n")

    except Exception as e:
        print(f"⚠ Error procesando {ruta_pdf}: {e}")


prompt = """
Extrae la siguiente información del PDF:
- Empresa que realizo la reparacion
- valor total de la reparacion (solo el número)
- fecha de la factura
- Descripción breve del servicio realizado


"""

carpeta = r"C:\Users\calza\Documents\scripts\Scripts_Gemini\Leer_pdf\documentos"

procesar_carpeta_pdf(carpeta, prompt)
