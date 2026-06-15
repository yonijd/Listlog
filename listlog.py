#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import ctypes
import time
import subprocess
from pathlib import Path
from datetime import datetime

__version__ = "1.0.0"

def resize_and_dock_window():
    try:
        kernel32 = ctypes.windll.kernel32
        user32 = ctypes.windll.user32
        os.system("mode con cols=88 lines=40")
        kernel32.SetConsoleTitleW("LISTADO DE DIRECTORIO - LISTLOG")
        time.sleep(0.05)
        hwnd = kernel32.GetConsoleWindow()
        if hwnd:
            class RECT(ctypes.Structure):
                _fields_ = [("left", ctypes.c_int),
                            ("top", ctypes.c_int),
                            ("right", ctypes.c_int),
                            ("bottom", ctypes.c_int)]
            rect = RECT()
            user32.GetWindowRect(hwnd, ctypes.byref(rect))
            window_width = rect.right - rect.left
            window_height = rect.bottom - rect.top
            screen_width = user32.GetSystemMetrics(0)
            x = screen_width - window_width - 20
            y = 20
            user32.MoveWindow(hwnd, x, y, window_width, window_height, True)
    except Exception:
        pass

def format_size(bytes_size):
    if bytes_size < 1024:
        return f"{bytes_size} B"
    elif bytes_size < 1024 * 1024:
        return f"{bytes_size / 1024:.2f} KB"
    elif bytes_size < 1024 * 1024 * 1024:
        return f"{bytes_size / (1024 * 1024):.2f} MB"
    else:
        return f"{bytes_size / (1024 * 1024 * 1024):.2f} GB"

def get_directory_info(target_path, recursive):
    elements = []
    total_size = 0
    file_count = 0
    dir_count = 0
    pdf_count = 0
    
    start_time = time.time()
    
    try:
        for entry in os.scandir(target_path):
            try:
                stat_info = entry.stat()
                mtime = datetime.fromtimestamp(stat_info.st_mtime).strftime("%Y-%m-%d %H:%M")
                
                if entry.is_file():
                    size = stat_info.st_size
                    ext = Path(entry.name).suffix.lower()
                    elements.append({
                        "name": entry.name,
                        "type": ext if ext else "FILE",
                        "size": size,
                        "mtime": mtime,
                        "is_dir": False
                    })
                    total_size += size
                    file_count += 1
                    if ext == ".pdf":
                        pdf_count += 1
                elif entry.is_dir():
                    elements.append({
                        "name": entry.name,
                        "type": "DIR",
                        "size": 0,
                        "mtime": mtime,
                        "is_dir": True
                    })
                    dir_count += 1
            except Exception:
                continue
    except Exception as e:
        print(f"Error: {e}")
        return [], 0, 0, 0, 0, 0
        
    if recursive:
        for root, dirs, files in os.walk(target_path):
            if root != str(target_path):
                dir_count += len(dirs)
            for file in files:
                file_path = Path(root) / file
                try:
                    if Path(root) == target_path:
                        continue
                    stat_info = file_path.stat()
                    size = stat_info.st_size
                    total_size += size
                    file_count += 1
                    if file_path.suffix.lower() == ".pdf":
                        pdf_count += 1
                except Exception:
                    continue
                    
    elapsed_time = time.time() - start_time
    elements.sort(key=lambda x: (not x["is_dir"], x["name"].lower()))
    
    return elements, total_size, file_count, dir_count, pdf_count, elapsed_time

def draw_clean_table(elements):
    w_name = 44
    w_type = 6
    w_size = 10
    w_mod = 16
    
    lines = []
    header = f"{'NOMBRE':<{w_name}}  {'TIPO':^{w_type}}  {'TAMANO':>{w_size}}  {'MODIFICADO':^{w_mod}}"
    lines.append(header)
    lines.append("-" * len(header))
    
    for el in elements:
        name = el["name"]
        if len(name) > (w_name - 3):
            name = name[:(w_name - 6)] + "..."
            
        el_type = el["type"]
        if len(el_type) > w_type:
            el_type = el_type[:w_type]
            
        size_str = format_size(el["size"]) if not el["is_dir"] else "<DIR>"
        mtime = el["mtime"]
        
        lines.append(f"{name:<{w_name}}  {el_type:^{w_type}}  {size_str:>{w_size}}  {mtime:^{w_mod}}")
        
    lines.append("-" * len(header))
    return "\n".join(lines)

def write_log(target_path, table_output, summary_line):
    now = datetime.now()
    folder_name = target_path.name if target_path.name else "raiz"
    folder_clean = "".join([c if c.isalnum() else "_" for c in folder_name])
    
    log_dir = Path(os.environ["USERPROFILE"]) / ".ialogpack" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_filename = f"listlog_{folder_clean}_{now.strftime('%Y-%m-%d_%H-%M-%S')}.log"
    log_filepath = log_dir / log_filename
    
    header = f"REPORTE DE DIRECTORIO - LISTLOG v{__version__}\n"
    header += f"Carpeta: {target_path.absolute()}\n"
    header += f"Fecha/Hora: {now.strftime('%Y-%m-%d %H:%M:%S')}\n"
    header += "=" * 82 + "\n\n"
    
    try:
        with open(log_filepath, "w", encoding="utf-8") as f:
            f.write(header)
            f.write(table_output)
            f.write("\n\n" + summary_line + "\n")
        print(f"\n[+] Log guardado en:")
        print(f"    {log_filepath}")
        return log_filepath
    except Exception as e:
        print(f"Advertencia: No se pudo guardar el log: {e}")
        return None

def copy_to_clipboard(text):
    try:
        subprocess.run("clip", input=text.encode("utf-8"), check=True, shell=True)
        return True
    except Exception:
        return False

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    
    resize_and_dock_window()
    
    if len(sys.argv) < 2:
        print("Error: Falta la ruta")
        print(f"Uso: {Path(__file__).name} <ruta>")
        input("\nPresione Enter para salir...")
        sys.exit(1)
    
    target_str = sys.argv[1].strip().strip('"').strip("'")
    target_path = Path(target_str)
    
    if not target_path.is_dir():
        print(f"Error: '{target_str}' no es una carpeta valida.")
        input("\nPresione Enter para salir...")
        sys.exit(1)
    
    recursive = False
    if len(sys.argv) >= 3:
        recursive = sys.argv[2] == "--recursive"
    
    print("=" * 82)
    print(f"   LISTADOR DE DIRECTORIO - LISTLOG v{__version__} ({'RECURSIVO' if recursive else 'SIMPLE'})")
    print("=" * 82)
    print(f" Directorio: {target_path.absolute()}\n")
    
    elements, total_size, file_count, dir_count, pdf_count, elapsed = get_directory_info(target_path, recursive)
    
    if not elements:
        print("La carpeta esta vacia.")
        print("=" * 82)
        input("\nPresione Enter para salir...")
        sys.exit(0)
    
    table_output = draw_clean_table(elements)
    print(table_output)
    
    summary_line = (
        f" RESUMEN: {file_count:,} Arch. ({pdf_count:,} PDFs) | "
        f"{dir_count:,} Carp. | "
        f"Total: {format_size(total_size)} ({total_size:,} B) | "
        f"Tiempo: {elapsed:.3f} seg"
    )
    
    print(summary_line)
    print("=" * 82)
    
    now = datetime.now()
    header = f"REPORTE DE DIRECTORIO - LISTLOG v{__version__}\n"
    header += f"Carpeta: {target_path.absolute()}\n"
    header += f"Fecha/Hora: {now.strftime('%Y-%m-%d %H:%M:%S')}\n"
    header += "=" * 82 + "\n\n"
    
    full_report = header + table_output + "\n\n" + summary_line + "\n"
    
    write_log(target_path, table_output, summary_line)
    
    if copy_to_clipboard(full_report):
        print("\n[+] Reporte copiado al portapapeles.")
    else:
        print("\n[!] No se pudo copiar al portapapeles.")
    
    print("")
    input("Presione Enter para salir...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        input("\nPresione Enter para salir...")