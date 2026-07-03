import os
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 15)
        self.cell(0, 10, self.title, border=False, align="C")
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def generate_en():
    pdf = PDF()
    pdf.title = "Phishing & Common Cyber Attacks: A Guide"
    pdf.add_page()
    pdf.set_font("helvetica", size=11)
    
    content = [
        ("What is Phishing?", "B"),
        ("Phishing is when attackers send scam emails (or text messages) designed to trick you into revealing sensitive information, like your passwords, bank details, or Social Security number. They often pretend to be a trusted company (like your bank, Amazon, or Netflix) to gain your trust.", ""),
        ("", ""),
        ("How to Spot a Phishing Attack:", "B"),
        ("1. Urgent or Threatening Language: 'Your account will be suspended if you do not act immediately.'", ""),
        ("2. Generic Greetings: 'Dear Customer' instead of your real name.", ""),
        ("3. Mismatched Sender Addresses: The email says it's from PayPal, but the actual email address is 'security@paypal-update123.com'.", ""),
        ("4. Suspicious Links: Hover over a link (without clicking) to see the actual URL. If it looks strange, do not click.", ""),
        ("", ""),
        ("How to Protect Yourself:", "B"),
        ("- Never click links in unexpected emails. Go directly to the website by typing the address in your browser.", ""),
        ("- Enable Two-Factor Authentication (2FA) on all your accounts.", ""),
        ("- Never download attachments from people you do not know.", ""),
        ("", ""),
        ("Other Common Attacks:", "B"),
        ("Ransomware: Malware that locks your files until you pay a ransom. Protect yourself by keeping regular backups of your important files on an external hard drive.", ""),
        ("Malware/Viruses: Software designed to harm your computer. Protect yourself by only downloading software from official websites and keeping your Operating System updated.", "")
    ]
    
    for text, style in content:
        pdf.set_font("helvetica", style=style, size=11 if style == "" else 13)
        pdf.multi_cell(190, 10 if style == "B" else 6, text)
        
    os.makedirs("docs", exist_ok=True)
    pdf.output("docs/PHISHING_AND_ATTACKS_EN.pdf")

def generate_es():
    pdf = PDF()
    pdf.title = "Phishing y Ataques Ciberneticos Comunes: Una Guia"
    pdf.add_page()
    pdf.set_font("helvetica", size=11)
    
    content = [
        ("¿Que es el Phishing?", "B"),
        ("El Phishing es cuando los atacantes envian correos electronicos (o mensajes de texto) fraudulentos disenados para enganarte y que reveles informacion confidencial, como tus contrasenas, datos bancarios o numero de seguro social. A menudo se hacen pasar por una empresa de confianza (como tu banco, Amazon o Netflix) para ganarse tu confianza.", ""),
        ("", ""),
        ("Como Detectar un Ataque de Phishing:", "B"),
        ("1. Lenguaje Urgente o Amenazante: 'Su cuenta sera suspendida si no actua de inmediato.'", ""),
        ("2. Saludos Genericos: 'Estimado Cliente' en lugar de tu nombre real.", ""),
        ("3. Direcciones de Remitente Sospechosas: El correo dice ser de PayPal, pero la direccion real es 'seguridad@paypal-update123.com'.", ""),
        ("4. Enlaces Extranos: Pasa el raton sobre un enlace (sin hacer clic) para ver la URL real. Si parece extrana, no hagas clic.", ""),
        ("", ""),
        ("Como Protegerte:", "B"),
        ("- Nunca hagas clic en enlaces de correos inesperados. Ve directamente al sitio web escribiendo la direccion en tu navegador.", ""),
        ("- Activa la Autenticacion de Dos Pasos (2FA) en todas tus cuentas.", ""),
        ("- Nunca descargues archivos adjuntos de personas que no conoces.", ""),
        ("", ""),
        ("Otros Ataques Comunes:", "B"),
        ("Ransomware: Software malicioso que bloquea tus archivos hasta que pagas un rescate. Protegete manteniendo copias de seguridad regulares de tus archivos importantes en un disco duro externo.", ""),
        ("Malware/Virus: Software disenado para danar tu computadora. Protegete descargando software solo de sitios web oficiales y manteniendo tu Sistema Operativo actualizado.", "")
    ]
    
    for text, style in content:
        pdf.set_font("helvetica", style=style, size=11 if style == "" else 13)
        pdf.multi_cell(190, 10 if style == "B" else 6, text.encode('latin-1', 'replace').decode('latin-1'))
        
    os.makedirs("docs", exist_ok=True)
    pdf.output("docs/PHISHING_Y_ATAQUES_ES.pdf")

if __name__ == "__main__":
    generate_en()
    generate_es()
    print("PDFs generated successfully.")
