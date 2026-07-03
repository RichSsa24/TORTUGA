<div align="center">
  <img src="logo.png" alt="TORTUGA Logo" width="220" onerror="this.style.display='none'">
  
  <h1>TORTUGA</h1>
  <p><em>Aplica configuraciones de seguridad reversibles y por niveles en Windows, Linux y macOS mediante una CLI bilingüe.</em></p>

  <p>
    <a href="https://github.com/RichSsa24/TORTUGA/actions/workflows/ci.yml"><img src="https://github.com/RichSsa24/TORTUGA/actions/workflows/ci.yml/badge.svg" alt="CI Status"></a>
    <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python Version">
    <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  </p>
  <p>
    <a href="../README.md"><strong>Read in English →</strong></a>
  </p>
</div>

<br />

## Por qué TORTUGA

| Característica | TORTUGA | privacy.sexy | HardeningKitty | Scripts de Debloat |
| :--- | :--- | :--- | :--- | :--- |
| **Reversión (Rollback)** | JSON exacto del estado previo por ejecución | Scripts genéricos por defecto de Windows | Copia de seguridad solo al inicio | Usualmente irreversible |
| **Predicción de Impacto** | Verifica el estado en vivo antes de aplicar | Ninguna | Ninguna | Ninguna |
| **Salida de Consola** | QUÉ/POR QUÉ/DESHACER en lenguaje claro | Código del script / jerga | Registro de auditoría denso | Código del script |
| **Modo por Defecto** | Modo simulación (requiere `--apply`) | Genera scripts activos | Varía | Ejecución activa |
| **Multiplataforma** | Windows, Linux, macOS | Windows, macOS | Solo Windows | Varía por script |

## Modelo de Seguridad

* **Modo simulación por defecto (dry-run):** Ejecutar la CLI escanea y reporta el estado actual. No escribe ningún cambio a menos que se pase explícitamente `--apply`.
* **Predicción de impacto preliminar (preflight):** Antes de tocar una configuración, TORTUGA verifica si el sistema depende activamente de ella (ej. revisando sesiones activas de SMB antes de desactivar el protocolo) y degrada la acción si encuentra riesgos.
* **Registrado y reversible:** Cada clave de registro o política modificada se guarda en un archivo de estado. `tortuga rollback` restaura cada ajuste modificado a su valor previo registrado.
* **Lo que NO es:** TORTUGA no es un antivirus. No puede arreglar una máquina que ya ha sido comprometida. Ninguna herramienta hace que una computadora sea "100% segura".

Consulta [THREAT_MODEL.md](THREAT_MODEL.md) para ver los límites.

## Guía Rápida

**Requisitos:** Python 3.10+. Nota: Windows requiere PowerShell elevado; Linux/macOS requieren `sudo` para `--apply`.

```bash
git clone https://github.com/RichSsa24/TORTUGA.git
cd TORTUGA
pip install -r requirements.txt

# 1. Simulación (dry-run): escanea y predice el impacto sin aplicar
python -m tortuga harden --module system_hardening --level 3

# 2. Aplicar: ejecuta la configuración de seguridad
python -m tortuga harden --module system_hardening --level 3 --apply
# -> Genera un ID de reversión, ej., run_1783053171.json

# 3. Reversión (rollback): deshace la ejecución específica
python -m tortuga rollback run_1783053171.json
```

## Cómo Funciona

### Niveles
| Nivel | Propósito | Riesgo de Funcionalidad |
| :--- | :--- | :--- |
| **1** | Higiene Básica | Riesgo nulo; habilita funciones de seguridad integradas. |
| **2** | Protección Estándar | Riesgo bajo; desactiva protocolos antiguos que la mayoría no usa. |
| **3** | Escritorio Protegido | Riesgo moderado; restringe la telemetría en segundo plano y ajusta permisos. |
| **4** | Estricto Corporativo | Riesgo alto; rompe algunas aplicaciones antiguas y protocolos de red. |
| **5** | Seguridad Máxima | Riesgo extremo; bloquea el sistema para entornos hostiles. |

### Módulos
| Módulo | Enfoque |
| :--- | :--- |
| `system_hardening` | Internos del SO, mitigaciones de procesos y protección de credenciales. |
| `network_security` | Reglas de firewall, desactivación de protocolos (SMBv1, LLMNR) y filtrado de puertos. |
| `privacy` | Reducción de telemetría, prevención de rastreo y bloqueo de ID de anuncios. |

## Uso

TORTUGA soporta dos subcomandos principales:

### `harden`
Escanea y aplica acciones de seguridad.
```bash
# Escanea la seguridad de red hasta el nivel 4 (Modo simulación)
python -m tortuga harden --module network_security --level 4

# Aplica la seguridad del sistema
python -m tortuga harden --module system_hardening --level 3 --apply
```

### `rollback`
Revierte un registro de transacción específico.
```bash
# Revierte una sesión previa usando su registro de transacción
python -m tortuga rollback run_1783053171.json
```

## Documentación

| Documento | Propósito |
| :--- | :--- |
| [CONFIG_MATRIX.md](CONFIG_MATRIX.md) | Las claves de registro exactas y comandos ejecutados por nivel. |
| [LANDSCAPE.md](LANDSCAPE.md) | Comparativa detallada con herramientas existentes. |
| [THREAT_MODEL.md](THREAT_MODEL.md) | De qué te defiende TORTUGA y qué es lo que no cubre. |

## Hoja de Ruta (Roadmap)

- [ ] Documentación de límites y recuperación `ROLLBACK.md`.
- [ ] Guías educativas exportables (PDFs).
- [ ] Módulo `browser_hardening`.
- [ ] Módulo `application_security`.

## Contribución y Seguridad

Consulta [CONTRIBUTING.md](../CONTRIBUTING.md) para desarrollo de plugins y guías de PR.
Revisa [SECURITY.md](../SECURITY.md) para reportar vulnerabilidades de forma privada.

## Licencia

Licencia MIT.
