#!/usr/bin/env python3
# backend/clean_expired_accounts.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from repositories import usuario_repository as repo

def main():
    eliminadas = repo.eliminar_cuentas_expiradas()
    if eliminadas:
        print(f"Se eliminaron {eliminadas} cuentas expiradas")

if __name__ == "__main__":
    main()
