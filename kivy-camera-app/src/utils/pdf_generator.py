from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import os
from datetime import datetime

def generate_pdf_report(accident_data, output_dir=None):
    if output_dir is None:
        output_dir = os.path.join(os.path.expanduser('~'), 'ConstatAuto', 'reports')
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f'report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    filepath = os.path.join(output_dir, filename)
    
    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4
    
    # En-tête
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, "Constat Automobile")
    
    # Informations de base
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Date: {datetime.fromtimestamp(accident_data['timestamp'])}")
    c.drawString(50, height - 120, f"ID: {accident_data['id']}")
    c.drawString(50, height - 140, f"Location: {accident_data.get('location', 'Non spécifié')}")
    
    # Description
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 180, "Description:")
    c.setFont("Helvetica", 12)
    description = accident_data.get('description', 'Aucune description')
    c.drawString(50, height - 200, description)
    
    # Images
    if 'photos' in accident_data and accident_data['photos']:
        c.showPage()
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 50, "Photos:")
        y_position = height - 100
        for photo in accident_data['photos']:
            try:
                c.drawImage(photo, 50, y_position, width=200, height=150)
                y_position -= 200
                if y_position < 100:
                    c.showPage()
                    y_position = height - 100
            except:
                print(f"Erreur lors de l'ajout de l'image: {photo}")
    
    # Croquis
    if 'sketch' in accident_data and accident_data['sketch']:
        c.showPage()
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 50, "Croquis de l'accident:")
        try:
            c.drawImage(accident_data['sketch'], 50, height - 400, width=500, height=300)
        except:
            print("Erreur lors de l'ajout du croquis")
    
    c.save()
    return filepath
