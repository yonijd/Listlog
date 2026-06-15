#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import winreg
from pathlib import Path

__version__ = "1.0.0"

TOOL_NAME = "listlog"
SCRIPT_NAME = "listlog.py"
MENU_NUMBER = "1_listlog"
MENU_LABEL = "Listado Simple (listlog)"
MENU_ICON = "imageres.dll,3"

PARENT_NAME = "01_ialogpack"
REG_LOCATIONS = [
    (r"Software\Classes\Directory\shell", "%1"),
    (r"Software\Classes\Directory\Background\shell", "%V")
]

def get_paths():
    profile = Path(os.environ["USERPROFILE"])
    prod_dir = profile / ".ialogpack"
    src = Path(__file__).parent / SCRIPT_NAME
    dst = prod_dir / SCRIPT_NAME
    logs_dir = prod_dir / "logs"
    return src, dst, prod_dir, logs_dir

def copy_script(src, dst, prod_dir, logs_dir):
    prod_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    if not src.exists():
        print(f"ERROR: No se encuentra {SCRIPT_NAME}")
        sys.exit(1)

    if dst.exists() and os.path.getmtime(src) <= os.path.getmtime(dst):
        print(f"= {SCRIPT_NAME} destino mas reciente, se omite")
        return

    shutil.copy2(src, dst)
    print(f"+ {SCRIPT_NAME} copiado a: {dst}")

def ensure_parent_menu(reg_path):
    parent_path = f"{reg_path}\\{PARENT_NAME}"
    created = False
    try:
        parent_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, parent_path, 0, winreg.KEY_WRITE)
    except FileNotFoundError:
        parent_key = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, parent_path, 0, winreg.KEY_WRITE)
        created = True
    winreg.SetValueEx(parent_key, "MUIVerb", 0, winreg.REG_SZ, "IALogPack")
    winreg.SetValueEx(parent_key, "Icon", 0, winreg.REG_SZ, "cmd.exe")
    winreg.SetValueEx(parent_key, "SubCommands", 0, winreg.REG_SZ, "")
    try:
        winreg.DeleteValue(parent_key, "ExtendedSubCommandsKey")
    except FileNotFoundError:
        pass
    winreg.CloseKey(parent_key)

    shell_path = f"{parent_path}\\shell"
    shell_key = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, shell_path, 0, winreg.KEY_WRITE)
    winreg.CloseKey(shell_key)
    status = "creado" if created else "actualizado"
    print(f"+ Menu padre {status}: {parent_path}")

def register_submenu(reg_path, var, dst):
    cmd = f'cmd.exe /k python "{dst}" {var}'

    parent_path = f"{reg_path}\\{PARENT_NAME}"
    submenu_path = f"{parent_path}\\shell\\{MENU_NUMBER}"
    cmd_path = f"{submenu_path}\\command"

    submenu_key = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, submenu_path, 0, winreg.KEY_WRITE)
    winreg.SetValueEx(submenu_key, "", 0, winreg.REG_SZ, MENU_LABEL)
    winreg.SetValueEx(submenu_key, "Icon", 0, winreg.REG_SZ, MENU_ICON)
    winreg.CloseKey(submenu_key)

    cmd_key = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, cmd_path, 0, winreg.KEY_WRITE)
    winreg.SetValueEx(cmd_key, "", 0, winreg.REG_SZ, cmd)
    winreg.CloseKey(cmd_key)

    print(f"+ Submenu registrado: {submenu_path} (var: {var})")

# Agregar entrada recursiva
TOOL_NAME_REC = "listlog_recursive"
MENU_NUMBER_REC = "2_listlog_recursive"
MENU_LABEL_REC = "Listado Recursivo (listlog)"

def register_submenu_recursive(reg_path, var, dst):
    cmd = f'cmd.exe /k python "{dst}" {var} --recursive'

    parent_path = f"{reg_path}\\{PARENT_NAME}"
    submenu_path = f"{parent_path}\\shell\\{MENU_NUMBER_REC}"
    cmd_path = f"{submenu_path}\\command"

    submenu_key = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, submenu_path, 0, winreg.KEY_WRITE)
    winreg.SetValueEx(submenu_key, "", 0, winreg.REG_SZ, MENU_LABEL_REC)
    winreg.SetValueEx(submenu_key, "Icon", 0, winreg.REG_SZ, MENU_ICON)
    winreg.CloseKey(submenu_key)

    cmd_key = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, cmd_path, 0, winreg.KEY_WRITE)
    winreg.SetValueEx(cmd_key, "", 0, winreg.REG_SZ, cmd)
    winreg.CloseKey(cmd_key)

    print(f"+ Submenu registrado: {submenu_path} (var: {var}) [RECURSIVO]")

def main():
    print("=" * 60)
    print(f"   INSTALADOR - {TOOL_NAME.upper()} v{__version__}")
    print("=" * 60)

    src, dst, prod_dir, logs_dir = get_paths()

    print(f"\n[1/4] Copiando script...")
    copy_script(src, dst, prod_dir, logs_dir)

    for reg_path, var in REG_LOCATIONS:
        print(f"\n[2/4] Verificando menu padre en: {reg_path}")
        ensure_parent_menu(reg_path)

        print(f"[3/4] Registrando submenu SIMPLE...")
        register_submenu(reg_path, var, dst)

        print(f"[4/4] Registrando submenu RECURSIVO...")
        register_submenu_recursive(reg_path, var, dst)

    print("\n" + "=" * 60)
    print(f"   INSTALACION COMPLETADA")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        input("\nPresione Enter para salir...")
