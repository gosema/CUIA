# cara.py

import cv2
import numpy as np
from insightface.app import FaceAnalysis
import cuia
import estado_compartido 

def analizar_cara_con_insight(actualizar_ui=None):
    def mostrar(texto):
        if actualizar_ui:
            actualizar_ui(texto)
        else:
            print(texto)

    mostrar("Iniciando análisis facial...")

    cam = 0
    bk = cuia.bestBackend(cam)

    test_cam = cv2.VideoCapture(cam, bk)
    if not test_cam.isOpened():
        mostrar("No se pudo abrir la cámara.")
        return

    ancho = int(test_cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    alto = int(test_cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    test_cam.release()

    app = FaceAnalysis(name='buffalo_l')
    app.prepare(ctx_id=-1)

    cap = cuia.myVideo(cam, bk)

    try:
        recomendaciones_actuales = []
        indice_recomendacion = 0
        while True:
            ret, frame = cap.read()
            if not ret or frame is None:
                continue

            cv2.imshow("Presiona 'a' para analizar | 'q' para salir", frame)
            key = cv2.waitKey(1)

            if key == ord('a') or estado_compartido.capturar_por_voz:
                if estado_compartido.capturar_por_voz:
                    estado_compartido.capturar_por_voz = False
                faces = app.get(frame)
                if not faces:
                    mostrar("No se detectaron caras.")
                    continue

                for i, face in enumerate(faces):
                    age = face.age
                    gender = "Hombre" if face.gender == 1 else "Mujer"
                    recomendaciones_actuales = recomendar_flores(age, gender)
                    indice_recomendacion = 0
                    flor = recomendaciones_actuales[indice_recomendacion]
                    mostrar(f"[Cara {i+1}] Edad: {age:.1f} años, Género: {gender} → Recomendación: {flor}")

            elif key == ord('s') or estado_compartido.siguiente:
                if estado_compartido.siguiente:
                    estado_compartido.siguiente = False
                if recomendaciones_actuales:
                    indice_recomendacion = (indice_recomendacion + 1) % len(recomendaciones_actuales)
                    flor = recomendaciones_actuales[indice_recomendacion]
                    mostrar(f"Siguiente flor recomendada: {flor}")
                else:
                    mostrar("Primero analiza una cara presionando 'a'.")

            elif key == ord('q') or estado_compartido.escape:
                if estado_compartido.escape:
                    estado_compartido.escape = False
                mostrar("Finalizando análisis.")
                break

    except Exception as e:
        mostrar(f"Error durante el análisis facial: {e}")

    finally:
        cap.release()
        try:
            cv2.destroyAllWindows()
        except Exception as e:
            mostrar(f"No se pudo cerrar ventanas OpenCV: {e}")


def recomendar_flores(edad, genero):
    """
    Devuelve una lista ordenada de flores recomendadas según edad y género.
    """
    recomendaciones = []

    if edad < 13:
        recomendaciones = ["Margarita", "Girasol", "Tulipán"]
    elif edad < 20:
        recomendaciones = ["Girasol", "Margarita", "Rosa"]
    elif edad < 35:
        recomendaciones = ["Rosa", "Tulipán", "Girasol"] if genero == "Mujer" else ["Tulipán", "Girasol", "Rosa"]
    elif edad < 50:
        recomendaciones = ["Tulipán", "Lirio", "Rosa"] if genero == "Mujer" else ["Lirio", "Crisantemo", "Tulipán"]
    elif edad < 70:
        recomendaciones = ["Lirio", "Crisantemo", "Tulipán"] if genero == "Mujer" else ["Crisantemo", "Lirio", "Girasol"]
    else:
        recomendaciones = ["Crisantemo", "Lirio", "Tulipán"]

    return recomendaciones
