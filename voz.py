import time
import speech_recognition as sr
import estado_compartido

class Voz:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.stop_listening = None
        self.exit_flag = False
        self.on_text_recognized = None  # Callback externo para avisar a la UI
        self.on_analizar_cara = None  # Nuevo callback

    def iniciar(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("Calibración completada.")

        self.exit_flag = False
        self.stop_listening = self.recognizer.listen_in_background(
            self.microphone, self.callback
        )

    def detener(self):
        self.exit_flag = True
        if self.stop_listening:
            self.stop_listening()
            self.stop_listening = None
        print("Escucha detenida.")

    def callback(self, recognizer, audio):
        idiomas = ["es-ES", "en-US", "fr-FR"]
        mejores_resultados = []
        comandos_salir = {
            "es-ES": "salir",
            "en-US": "exit",
            "fr-FR": "quitter",
        }
        comandos_cara = {
            "es-ES": "analizar cara",
            "en-US": "analyze face",
            "fr-FR": "analyser visage",
        }
        comandos_marcador = {
            "es-ES": "analizar marcador",
            "en-US": "analyze marker",
            "fr-FR": "analyser marqueur",
        }
        comandos_capturar = {
            "es-ES": "capturar",
            "en-US": "capture",
            "fr-FR": "capturer",
        }
        comandos_next = {
            "es-ES": "siguiente",
            "en-US": "next",
            "fr-FR": "next",
        }
        comandos_escape = {
            "es-ES": "escape",
            "en-US": "escape",
            "fr-FR": "escape",
        }

        for idioma in idiomas:
            try:
                texto = recognizer.recognize_google(audio, language=idioma)
                print(f"Intentando con {idioma}: {texto}")
                if texto:
                    mejores_resultados.append((texto, idioma))
                    if any(comando in texto.lower() for comando in comandos_salir.values()):
                        print(f"Comando de salida detectado: '{texto}'")
                        self.exit_flag = True
                        break
                    if any(comando in texto.lower() for comando in comandos_cara.values()):
                        print("Comando 'analizar cara' detectado")
                        if self.on_analizar_cara:
                            self.on_analizar_cara()  # Llamar al callback
                    if any(comando in texto.lower() for comando in comandos_marcador.values()):
                        print("Comando 'analizar marcador' detectado")
                        if self.on_analizar_marcador:
                            self.on_analizar_marcador()  # Llamar al callback
                    if any(comando in texto.lower() for comando in comandos_capturar.values()):
                        print("Comando 'capturar' detectado")
                        estado_compartido.capturar_por_voz = True
                    if any(comando in texto.lower() for comando in comandos_next.values()):
                        print("Comando 'siguiente' detectado")
                        estado_compartido.siguiente = True
                    if any(comando in texto.lower() for comando in comandos_escape.values()):
                        print("Comando 'siguiente' detectado")
                        estado_compartido.escape = True


            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                print("Error con el servicio:", e)
                break

        if mejores_resultados and self.on_text_recognized:
            mejor_texto, mejor_idioma = max(mejores_resultados, key=lambda x: len(x[0]))
            self.on_text_recognized(mejor_texto, mejor_idioma)
