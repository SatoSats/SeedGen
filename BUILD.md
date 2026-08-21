# BUILD SEEDGEN v15.4 (BETA) - Procedura di Build Riproducibile

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
# Atteso: a5d904e2e9300e5288fab66ac94a1fb0fe7803a534582f2883a4c90c0d4a99da

### 2. Build

```bash
rm -rf build dist
pyinstaller --onefile --name seedgen-v15.4-linux-x86_64 seedgen_simulazione_sicuro.py
```

### 3. Verifica del binario

```bash
sha256sum dist/seedgen-v15.4-linux-x86_64
```

### 4. Firma GPG del binario

```bash
gpg --detach-sign --armor dist/seedgen-v15.4-linux-x86_64
```

### 5. Verifica della firma

```bash
gpg --verify dist/seedgen-v15.4-linux-x86_64.asc dist/seedgen-v15.4-linux-x86_64
```

## Nota

PyInstaller non garantisce build bit-for-bit identiche tra ambienti diversi.

Il sorgente `seedgen_simulazione_sicuro.py` è la fonte di verità per l'audit.

L'hash SHA-256 del sorgente deve corrispondere a quello documentato sopra.
