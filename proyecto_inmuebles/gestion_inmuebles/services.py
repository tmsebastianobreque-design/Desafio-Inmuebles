import os
import sys
import django


directorio_actual = os.path.dirname(os.path.abspath(__file__))
carpeta_app = directorio_actual
carpeta_proyecto_root = os.path.dirname(carpeta_app)
carpeta_workspace = os.path.dirname(carpeta_proyecto_root)

for ruta in [carpeta_workspace, carpeta_proyecto_root, carpeta_app]:
    if ruta not in sys.path:
        sys.path.insert(0, ruta)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proyecto_inmuebles.settings")

try:
    django.setup()
except ModuleNotFoundError:
    os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
    django.setup()

from django.db import connection

# =====================================================================
# REQUERIMIENTO 2: Listado por Comunas usando Django y SQL
# =====================================================================
def listar_inmuebles_por_comuna_sql():
    consulta = """
        SELECT 
            com.nombre AS nombre_comuna,
            inm.nombre AS nombre_inmueble,
            inm.descripcion AS descripcion_inmueble
        FROM gestion_inmuebles_inmueble AS inm
        INNER JOIN gestion_inmuebles_comuna AS com ON inm.comuna_id = com.id
        ORDER BY com.nombre, inm.nombre ASC;
    """
    
    with connection.cursor() as cursor:
        cursor.execute(consulta)
        resultados = cursor.fetchall()
        
    ruta_salida = 'resultado_comunas_sql.txt'
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        comuna_actual = None
        for comuna, inmueble, descripcion in resultados:
            if comuna != comuna_actual:
                if comuna_actual is not None:
                    f.write("\n")
                f.write(f"COMUNA: {comuna}\n")
                f.write("="*40 + "\n")
                comuna_actual = comuna
            
            f.write(f"{inmueble} - {descripcion}\n")
            
    print(f"¡Archivo '{ruta_salida}' generado con éxito!")

# =====================================================================
# REQUERIMIENTO 3: Listado por Regiones usando Django y SQL
# =====================================================================
def listar_inmuebles_por_region_sql():
    consulta = """
        SELECT 
            reg.nombre AS nombre_region,
            com.nombre AS nombre_comuna,
            inm.nombre AS nombre_inmueble,
            inm.precio_mensual AS precio
        FROM gestion_inmuebles_inmueble AS inm
        INNER JOIN gestion_inmuebles_comuna AS com ON inm.comuna_id = com.id
        INNER JOIN gestion_inmuebles_region AS reg ON com.region_id = reg.id
        ORDER BY reg.nombre, com.nombre, inm.nombre ASC;
    """
    
    with connection.cursor() as cursor:
        cursor.execute(consulta)
        resultados = cursor.fetchall()
        
    ruta_salida = 'resultado_regiones_sql.txt'
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        region_actual = None
        for region, comuna, inmueble, precio in resultados:
            if region != region_actual:
                if region_actual is not None:
                    f.write("\n")
                f.write(f"REGIÓN: {region}\n")
                f.write("="*50 + "\n")
                region_actual = region
                
            f.write(f"Región: {region} | Comuna: {comuna} | Inmueble: {inmueble} | Precio: ${precio}\n")
            
    print(f"¡Archivo '{ruta_salida}' generado con éxito!")

# =====================================================================
# BLOQUE DE EJECUCIÓN DIRECTA
# =====================================================================
if __name__ == "__main__":
    print("--- INICIANDO EXTRACCIÓN DE REQUERIMIENTOS SEGÚN RÚBRICA ---")
    listar_inmuebles_por_comuna_sql()
    listar_inmuebles_por_region_sql()
    print("--- PROCESO TERMINADO EXITOSAMENTE ---")
