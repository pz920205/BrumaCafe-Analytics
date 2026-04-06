import pandas as pd
import json
import os
import sys

def cargar_y_limpiar():
    # 1. ENCONTRAR EL ARCHIVO (No importa dónde estés parado)
    nombre_archivo = "mongodb eventos.json"
    posibles_rutas = [
        nombre_archivo,                                      # Misma carpeta
        os.path.join("..", nombre_archivo),                  # Una carpeta arriba
        os.path.join("data", nombre_archivo),                # Carpeta data
        os.path.join(os.path.dirname(__file__), nombre_archivo) # Ruta del script
    ]
    
    ruta_final = None
    for ruta in posibles_rutas:
        if os.path.exists(ruta):
            ruta_final = ruta
            break
    
    if not ruta_final:
        print(f"❌ ERROR: No encontré '{nombre_archivo}'.")
        print(f"Asegúrate de que el archivo JSON esté en la carpeta: {os.getcwd()}")
        return

    # 2. LEER LOS DATOS
    try:
        with open(ruta_final, 'r', encoding='utf-8') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
    except Exception as e:
        print(f"❌ Error al leer el JSON: {e}")
        return

    # 3. LIMPIEZA EXPRESO (Para Bruma Café)
    # Convertir fechas
   errors='coerce')
    
    # Convertir números y llenar vacíos con 0
    for col in ['revenue', 'costos']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Calcular Utilidad si las columnas existen
    if 'revenue' in df.columns and 'costos' in df.columns:
        df['utilidad'] = df['revenue'] - df['costos']
        df['margen_%'] = (df['utilidad'] / df['revenue']).fillna(0) * 100

    # 4. GUARDAR RESULTADO
    archivo_salida = "eventos_limpios.csv"
    df.to_csv(archivo_salida, index=False, encoding='utf-8-sig')
    
    print("✅ ¡LOGRADO!")
    print(f"📂 Archivo cargado desde: {os.path.abspath(ruta_final)}")
    print(f"💾 Archivo guardado como: {archivo_salida}")
    print("\n--- RESUMEN DE VENTAS ---")
    print(df[['fecha', 'tipo_evento', 'revenue']].head())

if __name__ == "__main__":
    cargar_y_limpiar()


