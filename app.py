from flask import Flask, request, jsonify
import os
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ OCR server attivo."

@app.route('/ocr', methods=['POST'])
def ocr_from_blob():
    try:
        # ✅ Ricevi il file correttamente da multipart/form-data
        file = request.files['pdf']
        file.save("temp.pdf")

        # 1. Ricevi il blob e salva come temp.pdf
        # with open("temp.pdf", "wb") as f:
        #    f.write(request.data)

        # 2. Converte il PDF in immagini
        images = convert_from_path("temp.pdf")

        # 3. Applica OCR
        extracted_text = ""
        for i, image in enumerate(images):
            text = pytesseract.image_to_string(image, lang='ita')
            extracted_text += f"\n--- Pagina {i+1} ---\n{text}"

        # 4. Salva output
        with open("output.txt", "w", encoding="utf-8") as out_file:
            out_file.write(extracted_text)

        with open("status.txt", "w") as status_file:
            status_file.write("OCR completato con successo.\n")
            status_file.write(f"Pagine processate: {len(images)}\n")

        extracted_text = extracted_text 
        # jsonify({"status": "success", "pages": len(images)})

        return extracted_text 
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
