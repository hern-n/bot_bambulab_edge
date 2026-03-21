import os
import re
import sys

def renombrar_carpeta(carpeta):
    # Recoger archivos cuyo nombre sea solo un número + extensión
    patron = re.compile(r'^(\d+)(\..+)$')
    archivos = []

    for nombre in os.listdir(carpeta):
        m = patron.match(nombre)
        if m:
            numero = int(m.group(1))
            extension = m.group(2)
            archivos.append((numero, extension, nombre))

    if not archivos:
        print("No se encontraron archivos con nombre numérico en la carpeta.")
        return

    # Ordenar por número
    archivos.sort(key=lambda x: x[0])

    print(f"Se encontraron {len(archivos)} archivos. Vista previa del renombrado:\n")
    plan = []
    for nuevo_num, (viejo_num, ext, nombre_original) in enumerate(archivos, start=1):
        nuevo_nombre = f"{nuevo_num}{ext}"
        print(f"  {nombre_original:>10}  →  {nuevo_nombre}")
        plan.append((nombre_original, nuevo_nombre))

    print()
    confirmacion = input("¿Proceder con el renombrado? (s/n): ").strip().lower()
    if confirmacion != 's':
        print("Operación cancelada.")
        return

    # Renombrar en dos pasadas para evitar colisiones (ej: 1.png ya existe)
    temporal = {}
    for original, nuevo in plan:
        tmp = original + ".tmp_rename"
        os.rename(os.path.join(carpeta, original), os.path.join(carpeta, tmp))
        temporal[tmp] = nuevo

    for tmp, nuevo in temporal.items():
        os.rename(os.path.join(carpeta, tmp), os.path.join(carpeta, nuevo))

    print(f"\n✓ {len(plan)} archivos renombrados correctamente.")

if __name__ == "__main__":

    carpeta = "elements"

    if not os.path.isdir(carpeta):
        print(f"Error: '{carpeta}' no es una carpeta válida.")
        sys.exit(1)

    renombrar_carpeta(carpeta)