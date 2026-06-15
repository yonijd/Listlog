#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import winreg
from pathlib import Path

TOOL_NAME = "listlog"
SCRIPT_NAME = "listlog.py"
MENU_NUMBER_SIMPLE = "1_listlog"
MENU_NUMBER_RECURSIVE = "2_listlog_recursive"
PARENT_NAME = "01_ialogpack"

REG_LOCATIONS = [
    r"Software\Classes\Directory\shell",
    r"Software\Classes\Directory\Background\shell"
]

def get_dst():
    return Path(os.environ["USERPROFILE"]) / ".ialogpack" / SCRIPT_NAME

def remove_script(dst):
    if dst.exists():
        dst.unlink()
        print(f"+ Eliminado: {dst}")
    else:
        print(f"= {SCRIPT_NAME} no encontrado")

def remove_submenu(reg_path, menu_number):
    parent_path = f"{reg_path}\\{PARENT_NAME}"
    submenu_path = f"{parent_path}\\shell\\{menu_number}"
    cmd_path = f"{submenu_path}\\command"

    try:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, cmd_path)
        print(f"+ Eliminado command: {cmd_path}")
    except:
        pass

    try:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, submenu_path)
        print(f"+ Eliminado submenu: {submenu_path}")
    except:
        pass

def main():
    print("=" * 60)
    print(f"   DESINSTALADOR - {TOOL_NAME.upper()}")
    print("=" * 60)

    print(f"\n[1/2] Eliminando script...")
    remove_script(get_dst())

    print(f"\n[2/2] Eliminando submenus (simple y recursivo)...")
    for reg_path in REG_LOCATIONS:
        remove_submenu(reg_path, MENU_NUMBER_SIMPLE)
        remove_submenu(reg_path, MENU_NUMBER_RECURSIVE)

    print("\n" + "=" * 60)
    print(f"   DESINSTALACION COMPLETADA")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        input("\nPresione Enter para salir...")
