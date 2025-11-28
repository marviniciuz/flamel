from time import sleep
from celery import shared_task
from transmutacao.models import DocumentoProcessado
from django.utils import timezone
from django.core.files.base import ContentFile
from flamel_project.celery_config import app
from PIL import Image
from io import BytesIO
import cv2
import numpy as np
import pytesseract
from pdf2image import convert_from_path
from gtts import gTTS              
import fitz                     


def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    full_text = ""
    for i, image in enumerate(images):
        text = pytesseract.image_to_string(image, lang='por')
        full_text += f"\n\n--- PAGINA {i+1} ---\n\n{text}"
    return full_text


@app.task
def processar_documento_task(documento_id):
    documento = None
    try:
        documento = DocumentoProcessado.objects.get(pk=documento_id)
        
        documento.status = 'PROCESSANDO'
        documento.log_processamento = f"Iniciando processamento para: {documento.tipo_transfomacao}"
        documento.save()

        print(f"[{documento.id}] Processamento iniciado: {documento.tipo_transfomacao}")

        original_name = documento.arquivo_original.name.split('/')[-1].replace('.pdf', '')
        
        if documento.tipo_transfomacao == 'EXTRAIR_TEXTO':
            
            full_text = extract_text_from_pdf(documento.arquivo_original.path)
            output_filename = f"{original_name}_transcrito.txt"
            
            documento.arquivo_resultado.save(output_filename, ContentFile(full_text.encode('utf-8')))
            documento.log_processamento = "Processamento OCR concluído e arquivo TXT gerado." 
        
        elif documento.tipo_transfomacao == 'MELHORAR_PDF':
            
            pdf_buffer = BytesIO() 
            doc_output = fitz.open(documento.arquivo_original.path)

            images = convert_from_path(documento.arquivo_original.path)
            
            new_doc = fitz.open()

            for i, pil_image in enumerate(images):
                img_cv = np.array(pil_image)
                gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
                _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
                
                img_pil_clean = Image.fromarray(binary)
                text = pytesseract.image_to_string(img_pil_clean, lang='por')
                
                page_width, page_height = img_pil_clean.size
                page = new_doc.new_page(width=page_width, height=page_height)
                
                img_bytes = BytesIO()
                img_pil_clean.save(img_bytes, format='PNG')
                img_bytes.seek(0) 
                
                page.insert_image(page.rect, stream=img_bytes.read())

                page.insert_text((50, 50), text, fontsize=1) 
                
            new_doc.save(pdf_buffer)
            new_doc.close()
            pdf_buffer.seek(0)

            output_filename = f"{original_name}_otimizado.pdf"
            documento.arquivo_resultado.save(output_filename, ContentFile(pdf_buffer.read()))
            documento.log_processamento = "Melhoria e PDF pesquisável (OCR avançado) gerado."

        elif documento.tipo_transfomacao == 'TRANSFORMAR_AUDIO':
            
            full_text = extract_text_from_pdf(documento.arquivo_original.path)
            
            tts = gTTS(text=full_text, lang='pt', tld='com.br', slow=False) 
            mp3_fp = BytesIO()
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            
            output_filename = f"{original_name}_audio.mp3"
            documento.arquivo_resultado.save(output_filename, ContentFile(mp3_fp.read()))
            documento.log_processamento = "Transmutação em Áudio concluída e arquivo MP3 gerado."
            
        else:
            raise ValueError(f"Tipo de transmutação desconhecido: {documento.tipo_transfomacao}")

        documento.status = 'SUCESSO'
        documento.data_conclusao = timezone.now()
        documento.save()
        
        print(f"[{documento.id}] Processamento CONCLUÍDO.")
        
        return True

    except DocumentoProcessado.DoesNotExist:
        print(f"Erro: Documento com ID {documento_id} não encontrado.")
        return False
    except Exception as e:
        if documento:
            documento.status = 'FALHA'
            log_msg = str(e)
            if "tesseract is not installed" in log_msg or "pdfinfo" in log_msg or "No such file or directory" in log_msg:
                 documento.log_processamento = "FALHA: Motores Tesseract/Poppler não encontrados ou problema de PATH. Verifique as instalações."
            else:
                 documento.log_processamento = f"Falha no processamento: {log_msg}"
            documento.save()
        print(f"Erro: Processamento FALHOU: {e}")
        return False