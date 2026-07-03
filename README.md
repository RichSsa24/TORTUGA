<div align="center">
  <img src="https://raw.githubusercontent.com/RichSsa24/TORTUGA/main/docs/logo.png" alt="TORTUGA Logo" width="150" onerror="this.style.display='none'">
  
  <h1>TORTUGA Cybersecurity Framework</h1>
  <p><em>Advanced OS Hardening, Simplified and Reversible.</em></p>

  <!-- Badges -->
  <p>
    <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python Version">
    <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey" alt="Supported Platforms">
    <img src="https://img.shields.io/badge/build-passing-brightgreen" alt="Build Status">
    <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  </p>

  <p>
    <a href="#english"><strong>English Documentation</strong></a> ·
    <a href="#español"><strong>Documentación en Español</strong></a>
  </p>
</div>

<br />

---

<h2 id="english">English</h2>

TORTUGA is an open-source, cross-platform security orchestrator. It allows non-technical users and system administrators alike to apply layered cybersecurity hardening configurations to their operating systems safely. 

Unlike traditional "debloat" or "hardening" scripts that aggressively delete files and permanently alter systems, TORTUGA is built on a foundation of safety, transparency, and reversibility.

### Core Philosophy

* **100% Reversible Transactions:** Every action TORTUGA performs is logged in a stateful transaction file. If a security policy breaks an application you rely on, you can perfectly roll back the system to its exact previous state.
* **Preflight Dry-Runs:** Before applying any changes, TORTUGA scans your system and generates an execution plan. It evaluates current configurations and predicts the impact of its actions without altering a single byte.
* **Non-Destructive Operations:** TORTUGA strictly modifies system policies and configurations. It never deletes personal data, user files, or essential system binaries.
* **Transparent Execution:** No obscure tech jargon. Every security modification is clearly explained in plain language, detailing exactly *what* is being changed and *why* it matters.

### Included Security Guides
Education is the first line of defense. We have compiled comprehensive, professionally designed guides to help you understand and defend against common cyber threats:
* [Download Phishing & Common Cyber Attacks Guide (PDF)](docs/PHISHING_AND_ATTACKS_EN.pdf)

### Installation

**Prerequisites:** 
* Python 3.10 or higher.
* Administrator/Root privileges (required for applying system policies).

```bash
# Clone the repository
git clone https://github.com/RichSsa24/TORTUGA.git

# Navigate to the directory
cd TORTUGA

# Install dependencies
pip install -r requirements.txt
```

### Usage Guide

TORTUGA operates through a simple Command Line Interface (CLI).

<details>
<summary><strong>1. System Scan (Dry-Run)</strong></summary>
<br>
To see what TORTUGA recommends without making any actual changes, run a scan. This generates a detailed execution plan.

```bash
python -m tortuga harden --module system_hardening --level 3
```
</details>

<details>
<summary><strong>2. Apply Hardening Policies</strong></summary>
<br>
To apply the changes, append the `--apply` flag. Ensure you are running your terminal as Administrator (Windows) or using `sudo` (Linux/macOS).

```bash
python -m tortuga harden --module system_hardening --level 3 --apply
```
Upon completion, TORTUGA will provide a `RUN_ID`. Save this ID in case you need to revert the changes.
</details>

<details>
<summary><strong>3. Rollback a Transaction</strong></summary>
<br>
If a security setting interferes with your workflow, you can undo the entire transaction using the `RUN_ID` generated during the hardening process.

```bash
python -m tortuga rollback <RUN_ID>.json
```
</details>

---

<h2 id="español">Español</h2>

TORTUGA es un orquestador de seguridad multiplataforma de código abierto. Permite tanto a usuarios sin conocimientos técnicos como a administradores de sistemas aplicar configuraciones de seguridad por capas en sus sistemas operativos de manera completamente segura.

A diferencia de los scripts tradicionales que borran archivos de forma agresiva y alteran los sistemas permanentemente, TORTUGA está construido sobre una base de seguridad, transparencia y reversibilidad.

### Filosofía Principal

* **Transacciones 100% Reversibles:** Cada acción que realiza TORTUGA se registra en un archivo de transacción de estado. Si una política de seguridad interfiere con una aplicación que utilizas, puedes revertir el sistema perfectamente a su estado anterior.
* **Simulaciones Previas (Dry-Run):** Antes de aplicar cualquier cambio, TORTUGA escanea tu sistema y genera un plan de ejecución. Evalúa las configuraciones actuales y predice el impacto de sus acciones sin alterar un solo byte.
* **Operaciones No Destructivas:** TORTUGA modifica estrictamente políticas y configuraciones del sistema. Nunca elimina datos personales, archivos de usuario ni binarios esenciales del sistema.
* **Ejecución Transparente:** Sin jerga técnica confusa. Cada modificación de seguridad se explica claramente, detallando exactamente *qué* se está cambiando y *por qué* es importante.

### Guías de Seguridad Incluidas
La educación es la primera línea de defensa. Hemos recopilado guías exhaustivas y diseñadas profesionalmente para ayudarte a comprender y defenderte de las amenazas cibernéticas comunes:
* [Descargar Guía de Phishing y Ataques Cibernéticos (PDF)](docs/PHISHING_Y_ATAQUES_ES.pdf)

### Instalación

**Requisitos:** 
* Python 3.10 o superior.
* Privilegios de Administrador/Root (necesarios para aplicar políticas del sistema).

```bash
# Clonar el repositorio
git clone https://github.com/RichSsa24/TORTUGA.git

# Navegar al directorio
cd TORTUGA

# Instalar dependencias
pip install -r requirements.txt
```

### Guía de Uso

TORTUGA opera a través de una interfaz de línea de comandos (CLI) sencilla y directa.

<details>
<summary><strong>1. Escaneo del Sistema (Modo Simulación)</strong></summary>
<br>
Para ver qué recomienda TORTUGA sin hacer ningún cambio real, ejecuta un escaneo. Esto generará un plan de ejecución detallado.

```bash
python -m tortuga harden --module system_hardening --level 3 --lang es
```
</details>

<details>
<summary><strong>2. Aplicar Políticas de Seguridad</strong></summary>
<br>
Para aplicar los cambios, añade la bandera `--apply`. Asegúrate de estar ejecutando tu terminal como Administrador (Windows) o usando `sudo` (Linux/macOS).

```bash
python -m tortuga harden --module system_hardening --level 3 --lang es --apply
```
Al finalizar, TORTUGA proporcionará un `RUN_ID`. Guarda este ID en caso de que necesites revertir los cambios.
</details>

<details>
<summary><strong>3. Revertir una Transacción (Rollback)</strong></summary>
<br>
Si una configuración de seguridad interfiere con tu flujo de trabajo, puedes deshacer toda la transacción utilizando el `RUN_ID` generado durante el proceso de protección.

```bash
python -m tortuga rollback <RUN_ID>.json --lang es
```
</details>

---

<div align="center">
  <p><small>TORTUGA is released under the MIT License. Contributions are welcome.</small></p>
</div>
