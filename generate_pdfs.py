import os
from fpdf import FPDF

# Enable HTML writing
class PDF(FPDF):
    def header(self):
        # Top color band
        self.set_fill_color(41, 128, 185) # A nice blue
        self.rect(0, 0, 210, 20, "F")
        self.set_y(8)
        self.set_font("helvetica", "B", 16)
        self.set_text_color(255, 255, 255)
        self.cell(0, 0, "TORTUGA CYBERSECURITY ACADEMY", align="C")
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def generate_html_en():
    return """
    <h1 align="center">Phishing & Common Cyber Attacks</h1>
    <h3 align="center"><i>A Guide to Protecting Yourself Online</i></h3>
    <br>
    
    <h2>What is Phishing?</h2>
    <p><b>Phishing</b> is when attackers send scam emails (or text messages) designed to trick you into revealing sensitive information, like your passwords, bank details, or Social Security number. They often pretend to be a trusted company (like your bank, Amazon, or Netflix) to gain your trust.</p>
    
    <h2>How to Spot a Phishing Attack</h2>
    <ul>
        <li><b>Urgent or Threatening Language:</b> "Your account will be suspended if you do not act immediately."</li>
        <li><b>Generic Greetings:</b> "Dear Customer" instead of your real name.</li>
        <li><b>Mismatched Sender Addresses:</b> The email says it's from PayPal, but the actual email address is "security@paypal-update123.com".</li>
        <li><b>Suspicious Links:</b> Hover over a link (without clicking) to see the actual URL. If it looks strange, do not click.</li>
    </ul>

    <h2>How to Protect Yourself</h2>
    <ul>
        <li><b>Never click links</b> in unexpected emails. Go directly to the website by typing the address in your browser.</li>
        <li><b>Enable Two-Factor Authentication (2FA)</b> on all your accounts.</li>
        <li><b>Never download attachments</b> from people you do not know.</li>
    </ul>

    <h2>Other Common Attacks</h2>
    <p><b>Ransomware:</b> Malware that locks your files until you pay a ransom. Protect yourself by keeping regular backups of your important files on an external hard drive or cloud storage.</p>
    <p><b>Malware/Viruses:</b> Software designed to harm your computer. Protect yourself by only downloading software from official websites and keeping your Operating System updated.</p>
    <br><br>
    <p align="center"><i>Generated securely by TORTUGA. Stay safe!</i></p>
    """

def generate_html_es():
    # Note: Using HTML entities for accents to avoid fpdf latin-1 issues easily
    return """
    <h1 align="center">Phishing y Ataques Cibern&eacute;ticos Comunes</h1>
    <h3 align="center"><i>Una Gu&iacute;a para Protegerte en L&iacute;nea</i></h3>
    <br>
    
    <h2>&iquest;Qu&eacute; es el Phishing?</h2>
    <p>El <b>Phishing</b> es cuando los atacantes env&iacute;an correos electr&oacute;nicos (o mensajes de texto) fraudulentos dise&ntilde;ados para enga&ntilde;arte y que reveles informaci&oacute;n confidencial, como tus contrase&ntilde;as, datos bancarios o n&uacute;mero de seguro social. A menudo se hacen pasar por una empresa de confianza (como tu banco, Amazon o Netflix) para ganarse tu confianza.</p>
    
    <h2>C&oacute;mo Detectar un Ataque de Phishing</h2>
    <ul>
        <li><b>Lenguaje Urgente o Amenazante:</b> "Su cuenta ser&aacute; suspendida si no act&uacute;a de inmediato."</li>
        <li><b>Saludos Gen&eacute;ricos:</b> "Estimado Cliente" en lugar de tu nombre real.</li>
        <li><b>Direcciones de Remitente Sospechosas:</b> El correo dice ser de PayPal, pero la direcci&oacute;n real es "seguridad@paypal-update123.com".</li>
        <li><b>Enlaces Extra&ntilde;os:</b> Pasa el rat&oacute;n sobre un enlace (sin hacer clic) para ver la URL real. Si parece extra&ntilde;a, no hagas clic.</li>
    </ul>

    <h2>C&oacute;mo Protegerte</h2>
    <ul>
        <li><b>Nunca hagas clic en enlaces</b> de correos inesperados. Ve directamente al sitio web escribiendo la direcci&oacute;n en tu navegador.</li>
        <li><b>Activa la Autenticaci&oacute;n de Dos Pasos (2FA)</b> en todas tus cuentas.</li>
        <li><b>Nunca descargues archivos adjuntos</b> de personas que no conoces.</li>
    </ul>

    <h2>Otros Ataques Comunes</h2>
    <p><b>Ransomware:</b> Software malicioso que bloquea tus archivos hasta que pagas un rescate. Prot&eacute;gete manteniendo copias de seguridad regulares de tus archivos importantes en un disco duro externo o almacenamiento en la nube.</p>
    <p><b>Malware/Virus:</b> Software dise&ntilde;ado para da&ntilde;ar tu computadora. Prot&eacute;gete descargando software solo de sitios web oficiales y manteniendo tu Sistema Operativo actualizado.</p>
    <br><br>
    <p align="center"><i>Generado de forma segura por TORTUGA. &iexcl;Mantente a salvo!</i></p>
    """

def create_pdf(filename, html_content):
    pdf = PDF()
    pdf.add_page()
    pdf.set_text_color(40, 40, 40)
    pdf.write_html(html_content)
    os.makedirs("docs", exist_ok=True)
    pdf.output(filename)

if __name__ == "__main__":
    create_pdf("docs/PHISHING_AND_ATTACKS_EN.pdf", generate_html_en())
    create_pdf("docs/PHISHING_Y_ATAQUES_ES.pdf", generate_html_es())
    print("Beautiful PDFs generated successfully.")
