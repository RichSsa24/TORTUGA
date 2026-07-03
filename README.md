<div align="center">
  <img src="docs/logo.png" alt="TORTUGA Logo" width="220" onerror="this.style.display='none'">
  
  <h1>TORTUGA</h1>
  <p><em>Applies reversible, leveled security hardening to Windows, Linux, and macOS through a bilingual CLI.</em></p>

  <p>
    <a href="https://github.com/RichSsa24/TORTUGA/actions/workflows/ci.yml"><img src="https://github.com/RichSsa24/TORTUGA/actions/workflows/ci.yml/badge.svg" alt="CI Status"></a>
    <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python Version">
    <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  </p>
  <p>
    <a href="docs/README.es.md"><strong>Documentación en español →</strong></a>
  </p>
</div>

<br />

## Why TORTUGA

| Feature | TORTUGA | privacy.sexy | HardeningKitty | Debloat Scripts |
| :--- | :--- | :--- | :--- | :--- |
| **Rollback** | Per-run exact prior state JSON | Generic Windows default scripts | Start-of-run backup only | Usually irreversible |
| **Impact Prediction** | Checks live state before applying | None | None | None |
| **Output** | Plain-language WHAT/WHY/UNDO | Script code / jargon | Jargon-heavy audit log | Script code |
| **Default Mode** | Dry-run (requires `--apply`) | Generates active scripts | Varies | Active execution |
| **Cross-Platform** | Windows, Linux, macOS | Windows, macOS | Windows only | Varies by script |

## Safety Model

* **Dry-run by default:** Running the CLI scans and reports current state. It writes zero changes unless explicitly passed `--apply`.
* **Preflight impact prediction:** Before touching a setting, TORTUGA checks if the system actively relies on it (e.g., checking for active SMB sessions before disabling the protocol) and demotes the action if risks are found.
* **Recorded and reversible:** Every modified registry key or policy is logged in a state file. `tortuga rollback` restores every setting it changed to its recorded prior value.
* **What it is NOT:** TORTUGA is not an antivirus. It cannot fix a machine that is already compromised. No tool makes a computer "100% secure".

See [THREAT_MODEL.md](docs/THREAT_MODEL.md) for limits.

## Quick Start

**Prerequisites:** Python 3.10+. Note: Windows requires elevated PowerShell; Linux/macOS requires `sudo` for `--apply`.

```bash
git clone https://github.com/RichSsa24/TORTUGA.git
cd TORTUGA
pip install -r requirements.txt

# 1. Dry-run: scan and predict impact without applying
python -m tortuga harden --module system_hardening --level 3

# 2. Apply: execute the hardening
python -m tortuga harden --module system_hardening --level 3 --apply
# -> Generates a rollback ID, e.g., run_1783053171.json

# 3. Rollback: undo the specific run
python -m tortuga rollback run_1783053171.json
```

## How It Works

### Levels
| Level | Intent | Functionality Risk |
| :--- | :--- | :--- |
| **1** | Basic Hygiene | Zero risk; enables built-in security features. |
| **2** | Standard Protection | Low risk; disables legacy protocols not used by most users. |
| **3** | Hardened Desktop | Moderate risk; restricts background telemetry and tightens permissions. |
| **4** | Enterprise Strict | High risk; breaks some legacy apps and sharing protocols. |
| **5** | Maximum Security | Extreme risk; locks down the system for hostile environments. |

### Modules
| Module | Focus |
| :--- | :--- |
| `system_hardening` | OS internals, process mitigations, and credential guard. |
| `network_security` | Firewall rules, protocol disabling (SMBv1, LLMNR), and port filtering. |
| `privacy` | Telemetry reduction, tracking prevention, and ad-ID blocking. |

## Usage

TORTUGA supports two primary subcommands:

### `harden`
Scan and apply hardening actions.
```bash
# Scan network security up to level 4 (Dry-run)
python -m tortuga harden --module network_security --level 4

# Apply system hardening in Spanish
python -m tortuga harden --module system_hardening --level 3 --apply --lang es
```

### `rollback`
Rollback a specific transaction log.
```bash
# Revert a previous hardening session using its transaction log
python -m tortuga rollback run_1783053171.json
```

## Documentation

| Document | Purpose |
| :--- | :--- |
| [CONFIG_MATRIX.md](docs/CONFIG_MATRIX.md) | The exact registry keys and commands run per level. |
| [LANDSCAPE.md](docs/LANDSCAPE.md) | Detailed comparison with existing tools. |
| [THREAT_MODEL.md](docs/THREAT_MODEL.md) | What TORTUGA defends against and what it does not cover. |

## Roadmap

- [ ] `ROLLBACK.md` limit and recovery documentation.
- [ ] Exportable Educational Guides (PDFs).
- [ ] `browser_hardening` module.
- [ ] `application_security` module.

## Contributing and Security

See [CONTRIBUTING.md](CONTRIBUTING.md) for plugin development and PR guidelines.
Review [SECURITY.md](SECURITY.md) to report vulnerabilities privately.

## License

MIT License.
