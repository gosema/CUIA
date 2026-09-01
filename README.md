# Interfaz Conversacional y Realidad Aumentada para Recomendación de Flores

Resumen
-------
Prototipo académico que integra reconocimiento de voz multilingüe, análisis facial y realidad aumentada basada en marcadores para ofrecer recomendaciones de flores personalizadas. El proyecto demuestra la capacidad de diseñar e integrar pipelines en tiempo real que combinan visión por computador, render 3D y interacción multimodal para la asignatura de CUIA (Computación Ubicua e Inteligencia Ambiental).

Estado del proyecto
-------------------
- Lenguaje: Python 3.x
- Estado: Prototipo funcional (requiere configuración de dependencias y drivers gráficos para render 3D)
- Archivos principales: `main.py`, `voz.py`, `cara.py`, `marcador.py`, `cuia.py`, `camara.py`

Objetivos cumplidos
-------------------
- Integrar reconocimiento de voz en background con callbacks hacia la UI.
- Detectar edad y género mediante `insightface` y generar recomendaciones de flores.
- Renderizar modelos glTF y componer las rendiciones con la entrada de cámara (AR basada en ArUco).
- Diseñar una UI mínima (Kivy) que coordina modos de interacción (voz, análisis facial y AR).
- Arquitectura modular con separación clara de responsabilidades y uso de hilos para mantener la interfaz responsiva.

Funcionalidades clave
---------------------
- Comandos por voz (es/en/fr): activar captura, analizar cara, analizar marcador, navegar recomendaciones.
- Análisis facial interactivo (captura por tecla o por voz) con recomendaciones basadas en edad/género.
- Modo AR: detección de marcadores ArUco y superposición de modelos 3D (`*.glb`) en la escena real.
- Calibración de cámara configurable en `camara.py`.

Tecnologías y herramientas
-------------------------
- Python 3.x
- Kivy (interfaz)
- OpenCV (captura, ArUco, procesamiento de imágenes)
- insightface (FaceAnalysis)
- speech_recognition (API Google, para POC)
- pygfx + wgpu (render 3D y canvas offscreen)
- numpy, matplotlib, pylinalg
- glTF (.glb) para modelos 3D

Estructura del repositorio
--------------------------
- `main.py` — entrada y UI principal (Kivy)
- `voz.py` — gestión de reconocimiento de voz y callbacks
- `cara.py` — análisis facial y recomendaciones
- `marcador.py` — pipeline AR con ArUco y render 3D
- `cuia.py` — utilidades 3D, render y clases auxiliares
- `camara.py` — parámetros de calibración de cámara
- `Documentación_CUIA_JoseMaría.pdf` — memoria del proyecto

Instalación y ejecución 
--------------------------------
1. Crear y activar un entorno virtual:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
2. Instalar dependencias:
```powershell
pip install -r CUIA/requirements.txt
```
3. Revisar que los modelos `.glb` estén en `CUIA/` (ej.: `crisantemo.glb`, `girasol.glb`, `margarita.glb`, `lirio_2.glb`, `tulipan.glb`).
4. Ejecutar la aplicación:
```powershell
python CUIA/main.py
```

Notas importantes sobre entorno
-------------------------------
- El render con `pygfx`/`wgpu` puede requerir controladores gráficos modernos y pasos adicionales según la plataforma (especialmente en Windows). Consulte la documentación oficial de `pygfx` y `wgpu` si aparecen errores relacionados con el backend gráfico.
- El reconocimiento de voz usa el servicio de Google a través de `speech_recognition`. Para producción, considere usar una solución on-premise o API con credenciales.

Cómo evaluar técnicamente
-------------------------
- Ejecutar y verificar que la UI carga y que la cámara se abre.
- Probar comandos por voz: activar captura, decir "analizar cara" o "analizar marcador".
- Validar que `insightface` detecta caras y devuelve edad/género razonables.
- Colocar un marcador ArUco (o el patrón por defecto) y comprobar la superposición 3D.
- Revisar latencia y estabilidad con distintas condiciones lumínicas.

