from django.shortcuts import render
import cv2
import pytesseract
import json
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\molma\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def reconocimiento_placa(request):
    file_path = os.path.join(os.path.dirname(__file__), 'placas.json')
    with open(file_path) as f:
        data = json.load(f)

    placa = ""
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(gray, 150, 200)
        canny = cv2.dilate(canny, None, iterations=1)

        contornos, _ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        placaFound = False

        for c in contornos:
            if placaFound == True:
                break
            area = cv2.contourArea(c)

            x, y, w, h = cv2.boundingRect(c)
            epsilon = 0.09 * cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, epsilon, True)

            if len(approx) == 4 and area > 9000:
                # print('Area = ', area)
                aspect_ratio = float(w) / h
                if aspect_ratio > 1.8:
                    # cv2.drawContours(frame, [c], 0, (255, 255, 0), 2)
                    placa = gray[y:y + h, x:x + w]
                    text = pytesseract.image_to_string(placa, config='--psm 11')
                    text = text.replace("\n", "")
                    # cv2.imshow('Placa', placa) #Mostrar la imagen de la placa
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    # cv2.putText(frame, text, (x-20, y-10), 1, 2.2, (0, 255, 0), 3)

                    # Si encuentra un texto de exactamente 9 caracteres termina el programa
                    if len(text) == 9 and text[2] == '-' and text[7]:
                        print('Placa: ', text)
                        placaFound = True
                        placa = text
                        break

        cv2.imshow('Camara', frame)
        # cv2.imshow('Canny', canny)

        # Leemos una tecla
        t = cv2.waitKey(1)
        if t == 27 or placaFound == True:
            break

    cap.release()
    cv2.destroyAllWindows()

    placa_valida = len(placa) > 0

    print(placa)

    res = ""

    codigo_buscado = placa
    objeto_buscado = None

    for objeto in data:
        if objeto['codigo'] == codigo_buscado:
            objeto_buscado = objeto
            break

    if objeto_buscado is not None:
        print(objeto_buscado)
        ...
    else:
        ...
        res = "No se encontró la placa {} en el sistema".format(placa)
        print(res)



    return render(request, 'templates/reconocimiento_placa.html', {'placa': placa, 'placa_valida': placa_valida, 'objeto_buscado': objeto_buscado, 'res': res})
