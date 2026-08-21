# BUILD SEEDGEN v15.3 (BETA) - Procedura di Build Riproducibile

## Ambiente di Build

| Componente | Versione |
|------------|----------|
| Sistema operativo | Linux Mint 22 (Ubuntu 24.04 base) |
| Kernel | 7.0.0-29-generic |
| Architettura | x86_64 |
| Python | 3.12.3 |
| PyInstaller | 6.22.2 |
| glibc | 2.39 |

## Dipendenze

Nessuna dipendenza esterna. Solo librerie standard Python.

## Procedura di Build

### 1. Verifica del sorgente
```bash
sha256sum seedgen_simulazione_sicuro.py
# Atteso: f35e60ac0ce7683c6d68810f44baf9b863876dc3fe7f8b1e6070c54a6d33be59
cd ~/Scaricati/SeedGen && cat > BUILD.md << 'FINE'
# BUILD SEEDGEN v15.3 (BETA) - Procedura di Build

## Ambiente di Build

| Componente | Versione |
|------------|----------|
| Sistema operativo | Linux Mint 22 |
| Kernel | 7.0.0-29-generic |
| Architettura | x86_64 |
| Python | 3.12.3 |
| PyInstaller | 6.22.2 |

## Dipendenze

Nessuna dipendenza esterna. Solo librerie standard Python.

## Procedura

1. Verifica sorgente: sha256sum seedgen_simulazione_sicuro.py
2. Build: pyinstaller --onefile --name seedgen-v15-linux-x86_64 seedgen_simulazione_sicuro.py
3. Verifica binario: sha256sum dist/seedgen-v15-linux-x86_64
4. Firma: gpg --detach-sign --armor dist/seedgen-v15-linux-x86_64

## Nota

PyInstaller NON garantisce build bit-for-bit identiche.
Il sorgente e la fonte di verita per l'audit.
