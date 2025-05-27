import cv2
import numpy as np
import cuia
import math

def iniciar_ar(on_flor_detectada=None, on_close=None):
    cam = 0
    bk = cuia.bestBackend(cam)

    # Dimensiones del frame
    webcam = cv2.VideoCapture(cam, bk)
    if not webcam.isOpened():
        print("No se pudo abrir la cámara.")
        return

    ancho = int(webcam.get(cv2.CAP_PROP_FRAME_WIDTH))
    alto = int(webcam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    webcam.release()

    # Cargar calibración
    try:
        import camara
        cameraMatrix = camara.cameraMatrix
        distCoeffs = camara.distCoeffs
    except ImportError:
        cameraMatrix = np.array([
            [1000, 0, ancho/2],
            [0, 1000, alto/2],
            [0, 0, 1]
        ])
        distCoeffs = np.zeros((5, 1))

    # Modelos
    modelo1 = cuia.modeloGLTF('crisantemo.glb')
    modelo1.rotar((math.pi / 2.0, 0, 0))
    modelo1.escalar(1.2)
    modelo1.flotar()

    modelo2 = cuia.modeloGLTF('girasol.glb')
    modelo2.rotar((math.pi / 2.0, 0, 0))
    modelo2.escalar(0.35)
    modelo2.flotar()

    modelo3 = cuia.modeloGLTF('rosa.glb')
    modelo3.rotar((math.pi / 2.0, 0, 0))
    modelo3.escalar(0.5)
    modelo3.flotar()

    modelo4 = cuia.modeloGLTF('lirio_2.glb')
    modelo4.rotar((math.pi / 2.0, 0, 0))
    modelo4.escalar(0.20)
    modelo4.flotar()

    modelo5 = cuia.modeloGLTF('margarita.glb')
    modelo5.rotar((math.pi / 2.0, 0, 0))
    modelo5.escalar(0.4)
    modelo5.flotar()
        
    modelo6 = cuia.modeloGLTF('tulipan.glb')
    modelo6.rotar((math.pi / 2.0, 0, 0))
    modelo6.escalar(1.0)
    modelo6.flotar()

    def from_opencv_to_pygfx(rvec, tvec):
        pose = np.eye(4)
        pose[0:3, 3] = tvec.T
        pose[0:3, 0:3] = cv2.Rodrigues(rvec)[0]
        pose[1:3] *= -1
        return np.linalg.inv(pose)

    def calcular_fov(camera_matrix, ancho, alto):
        if ancho > alto:
            f = camera_matrix[1, 1]
            fov_rad = 2 * np.arctan(alto / (2 * f))
        else:
            f = camera_matrix[0, 0]
            fov_rad = 2 * np.arctan(ancho / (2 * f))
        return np.rad2deg(fov_rad)

    def detectar_pose(frame, tam_marcador):
        bboxs, ids, _ = detector.detectMarkers(frame)
        if ids is not None:
            obj_points = np.array([
                [-tam_marcador/2.0, tam_marcador/2.0, 0.0],
                [ tam_marcador/2.0, tam_marcador/2.0, 0.0],
                [ tam_marcador/2.0, -tam_marcador/2.0, 0.0],
                [-tam_marcador/2.0, -tam_marcador/2.0, 0.0]
            ])
            resultado = {}
            for i in range(len(ids)):
                ret, rvec, tvec = cv2.solvePnP(obj_points, bboxs[i], cameraMatrix, distCoeffs)
                if ret:
                    resultado[ids[i][0]] = (rvec, tvec)
            return True, resultado
        return False, None

    escena_cris = cuia.escenaPYGFX(calcular_fov(cameraMatrix, ancho, alto), ancho, alto)
    escena_gira = cuia.escenaPYGFX(calcular_fov(cameraMatrix, ancho, alto), ancho, alto)
    escena_rosa = cuia.escenaPYGFX(calcular_fov(cameraMatrix, ancho, alto), ancho, alto)
    escena_lirio = cuia.escenaPYGFX(calcular_fov(cameraMatrix, ancho, alto), ancho, alto)
    escena_marga = cuia.escenaPYGFX(calcular_fov(cameraMatrix, ancho, alto), ancho, alto)
    escena_tuli = cuia.escenaPYGFX(calcular_fov(cameraMatrix, ancho, alto), ancho, alto)

    escena_cris.agregar_modelo(modelo1)
    escena_cris.ilumina_modelo(modelo1)

    escena_gira.agregar_modelo(modelo2)
    escena_gira.ilumina_modelo(modelo2)

    escena_rosa.agregar_modelo(modelo3)
    escena_rosa.ilumina_modelo(modelo3)

    escena_lirio.agregar_modelo(modelo4)
    escena_lirio.ilumina_modelo(modelo4)

    escena_marga.agregar_modelo(modelo5)
    escena_marga.ilumina_modelo(modelo5)

    escena_tuli.agregar_modelo(modelo6)
    escena_tuli.ilumina_modelo(modelo6)

    ar = cuia.myVideo(cam, bk)
    diccionario = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)
    detector = cv2.aruco.ArucoDetector(diccionario)

    def realidadMixta(frame):
        ret, pose = detectar_pose(frame, 0.19)
        if ret and pose:
            for id_marcador, (rvec, tvec) in pose.items():
                M = from_opencv_to_pygfx(rvec, tvec)
                if id_marcador == 0:
                    #print(f"Marcador detectado: {id_marcador}")
                    escena_cris.actualizar_camara(M)
                    imagen_render = escena_cris.render()
                    nombre_flor = "Crisantemo"
                elif id_marcador == 1:
                    #print(f"Marcador detectado: {id_marcador}")
                    escena_gira.actualizar_camara(M)
                    imagen_render = escena_gira.render()
                    nombre_flor = "Girasol"
                elif id_marcador == 2:
                    #print(f"Marcador detectado: {id_marcador}")
                    escena_rosa.actualizar_camara(M)
                    imagen_render = escena_rosa.render()
                    nombre_flor = "Rosa"
                elif id_marcador == 3:
                    #print(f"Marcador detectado: {id_marcador}")
                    escena_lirio.actualizar_camara(M)
                    imagen_render = escena_lirio.render()
                    nombre_flor = "Lirio"
                elif id_marcador == 4:
                    #print(f"Marcador detectado: {id_marcador}")
                    escena_marga.actualizar_camara(M)
                    imagen_render = escena_marga.render()
                    nombre_flor = "Margarita"
                elif id_marcador == 5:
                    #print(f"Marcador detectado: {id_marcador}")
                    escena_tuli.actualizar_camara(M)
                    imagen_render = escena_tuli.render()
                    nombre_flor = "Tulipan"
                if nombre_flor and on_flor_detectada:
                    on_flor_detectada(nombre_flor)

                imagen_render_bgr = cv2.cvtColor(imagen_render, cv2.COLOR_RGBA2BGRA)
                return cuia.alphaBlending(imagen_render_bgr, frame)
        return frame

    ar.process = realidadMixta

    try:
        ar.play("Realidad Aumentada (presiona ESPACIO para salir)", key=ord(' '))
    finally:
        ar.release()
        cv2.destroyAllWindows()
        if on_close:
            on_close()

