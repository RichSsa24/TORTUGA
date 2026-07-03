<div align="center">
  <img src="https://raw.githubusercontent.com/RichSsa24/TORTUGA/main/docs/logo.png" alt="TORTUGA Logo" width="150" onerror="this.style.display='none'">
  <h1>🐢 TORTUGA</h1>
  <p><em>Slow, steady, and secure. Your personal cybersecurity assistant.</em></p>
  <p>
    <a href="#english">English</a> •
    <a href="#español">Español</a>
  </p>
</div>

---

<h2 id="english">🇬🇧 English</h2>

**TORTUGA** is a free, easy-to-use tool designed to secure your computer against common cyber threats, tracking, and malware. You don't need to be a hacker or an IT expert to use it. 

Many "speed-up" or "debloat" tools online can accidentally break your computer by aggressively deleting files. **TORTUGA is different**. It is built on four core promises:

1. ⏪ **100% Reversible**: Every single change TORTUGA makes is recorded. If an app stops working after you secure your computer, TORTUGA can perfectly undo the exact setting to fix it.
2. 🔮 **Predicts the Future (Dry-Run)**: Before modifying anything, TORTUGA runs a live check and tells you *exactly* what it plans to do and if it suspects it will break something.
3. 🎓 **Plain English (and Spanish)**: We don't use confusing tech jargon. TORTUGA explains every change in simple words so you understand *why* your computer is being modified.
4. 🛡️ **Non-Destructive**: TORTUGA never deletes your personal files or programs. It only adjusts invisible system policies to make your computer act like a fortress.

### 📚 Learn How to Protect Yourself
We have included free guides to help you identify and stop hackers before they trick you:
- 📖 **[Phishing and Common Attacks Guide (PDF)](docs/PHISHING_AND_ATTACKS_EN.pdf)**

### 🚀 Getting Started

**Requirements:** Windows, macOS, or Linux (Ubuntu/Debian) with Python 3.10+ installed.

1. **Download the tool:**
   ```bash
   git clone https://github.com/RichSsa24/TORTUGA.git
   cd TORTUGA
   pip install -r requirements.txt
   ```
2. **Scan your computer (Safe Mode):**
   See what TORTUGA recommends without actually changing anything.
   ```bash
   python -m tortuga harden --module system_hardening --level 3
   ```
3. **Apply the Protection:**
   *(Note: You must run your terminal/command prompt as Administrator/Root for this to work).*
   ```bash
   python -m tortuga harden --module system_hardening --level 3 --apply
   ```
4. **Undo a Change (Rollback):**
   If something went wrong, simply use the "Run ID" that TORTUGA gave you at the end of the previous step.
   ```bash
   python -m tortuga rollback <RUN_ID>.json
   ```

---

<h2 id="español">🇪🇸 Español</h2>

**TORTUGA** es una herramienta gratuita y fácil de usar, diseñada para asegurar tu computadora contra amenazas cibernéticas comunes, rastreo y virus. No necesitas ser un experto en informática para usarla.

Muchas herramientas en internet prometen "acelerar" tu PC, pero terminan rompiendo el sistema operativo. **TORTUGA es diferente**. Se basa en cuatro promesas fundamentales:

1. ⏪ **100% Reversible**: Cada cambio que hace TORTUGA queda registrado. Si una aplicación deja de funcionar después de proteger tu equipo, TORTUGA puede deshacer exactamente ese cambio para arreglarlo.
2. 🔮 **Predice el Futuro (Simulación)**: Antes de tocar nada, TORTUGA revisa tu sistema y te dice *exactamente* qué planea hacer y si sospecha que algo podría fallar.
3. 🎓 **Lenguaje Sencillo**: No usamos jerga técnica confusa. TORTUGA explica cada cambio con palabras simples para que entiendas *por qué* se está modificando tu computadora.
4. 🛡️ **No Destructivo**: TORTUGA nunca borra tus archivos personales ni programas. Solo ajusta configuraciones invisibles del sistema para convertir tu computadora en una fortaleza.

### 📚 Aprende a Protegerte
Hemos incluido guías gratuitas para ayudarte a identificar y detener a los hackers antes de que te engañen:
- 📖 **[Guía de Phishing y Ataques Comunes (PDF)](docs/PHISHING_Y_ATAQUES_ES.pdf)**

### 🚀 Cómo Empezar

**Requisitos:** Windows, macOS o Linux (Ubuntu/Debian) con Python 3.10+ instalado.

1. **Descarga la herramienta:**
   ```bash
   git clone https://github.com/RichSsa24/TORTUGA.git
   cd TORTUGA
   pip install -r requirements.txt
   ```
2. **Escanea tu computadora (Modo Seguro):**
   Mira lo que TORTUGA recomienda sin cambiar absolutamente nada.
   ```bash
   python -m tortuga harden --module system_hardening --level 3 --lang es
   ```
3. **Aplica la Protección:**
   *(Nota: Debes ejecutar tu terminal como Administrador/Root para que esto funcione).*
   ```bash
   python -m tortuga harden --module system_hardening --level 3 --lang es --apply
   ```
4. **Deshacer un Cambio (Rollback):**
   Si algo salió mal, simplemente usa el "Run ID" que TORTUGA te dio al final del paso anterior.
   ```bash
   python -m tortuga rollback <RUN_ID>.json --lang es
   ```

---
*For Developers: See [CONTRIBUTING.md](CONTRIBUTING.md) to add new rules to the engine.*
