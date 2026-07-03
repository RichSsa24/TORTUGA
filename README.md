# TORTUGA 🐢
*Slow, steady, and secure. A layered security and privacy hardening tool.*

TORTUGA is an open-source, cross-platform CLI tool designed to help users secure their machines against common threats and tracking, without requiring deep technical knowledge. 

Unlike many "debloat" or "hardening" scripts that break operating systems by aggressively deleting files or disabling core services, TORTUGA is built on four core principles:
1. **Reversibility**: Every single action taken by TORTUGA is recorded in a local JSON transaction log. If something breaks, TORTUGA can perfectly revert the exact setting back to what it was before.
2. **Impact Prediction (Dry-Run)**: TORTUGA runs a live pre-flight check *before* modifying anything, telling you exactly what will happen and warning you if it detects active services that might break.
3. **Education**: TORTUGA explains every change in plain language (English and Spanish) so you understand *why* a setting is being changed.
4. **Non-Destruction**: TORTUGA modifies policies and registry/configuration files. It does not delete system files.

## Features
- **Cross-Platform**: Supports Windows (PowerShell), Debian/Ubuntu Linux (Bash), and macOS (Bash).
- **Security Levels**: Choose a hardening level from 1 (Basic) to 5 (Maximum Paranoia).
- **Bilingual**: Fully supports English and Spanish (`--lang es`).
- **Granular Modules**: Selectively run modules like `system_hardening`, `network_security`, or `privacy`.

## Installation
Requires Python 3.10+.
```bash
git clone https://github.com/RichSsa24/TORTUGA.git
cd TORTUGA
pip install -r requirements.txt
```

## Usage

### 1. Scan (Dry-Run)
See what TORTUGA will do without making any changes.
```bash
python -m tortuga scan --level 3
```

### 2. Harden
Apply the hardening settings.
```bash
python -m tortuga harden --level 3
```
*Note: Depending on the OS and the actions, you must run this command in an elevated prompt (Administrator / root).*

### 3. Rollback
If a change breaks your workflow, you can easily revert it using the Run ID provided at the end of the hardening process.
```bash
python -m tortuga rollback <RUN_ID>
```

## Documentation
- [Security Matrix](docs/CONFIG_MATRIX.md)
- [Threat Model](docs/THREAT_MODEL.md)

## Contributing
Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to add new actions to the modules.

## License
MIT License
