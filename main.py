from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.clock import Clock
import threading
import time
from voz import Voz 
from cara import analizar_cara_con_insight
from marcador import iniciar_ar

class VoiceApp(App):
    def build(self):
        self.voz = Voz()
        self.voz.on_text_recognized = self.mostrar_texto
        self.voz.on_analizar_cara = self.analizar_cara_detectado  
        self.voz.on_analizar_marcador = self.analizar_marcador_detectado

        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        self.status_label = Label(text='Estado: Inactivo', size_hint=(1, 0.2))
        self.layout.add_widget(self.status_label)

        self.recomendacion_label = Label(text='Recomendación: ---', size_hint=(1, 0.2))
        self.layout.add_widget(self.recomendacion_label)

        self.flor_detectada_label = Label(text='Flor detectada: ---', size_hint=(1, 0.2))
        self.layout.add_widget(self.flor_detectada_label)

        self.btn_marker = Button(text='Analizar marcador')
        self.btn_marker.bind(on_press=self.analizar_marcador)

        self.btn_face = Button(text='Analizar cara')
        self.btn_face.bind(on_press=self.analizar_cara)

        self.btn_audio = ToggleButton(text='Capturar audio (OFF)')

        self.btn_audio.bind(on_press=self.toggle_audio)

        self.layout.add_widget(self.btn_marker)
        self.layout.add_widget(self.btn_face)
        self.layout.add_widget(self.btn_audio)

        return self.layout

    def toggle_audio(self, instance):
        if instance.state == 'down':
            instance.text = 'Capturando audio... (ON)'
            self.status_label.text = 'Estado: Escuchando...'
            threading.Thread(target=self.iniciar_voz_seguro, daemon=True).start()
        else:
            instance.text = 'Capturar audio (OFF)'
            self.status_label.text = 'Estado: Inactivo'
            self.voz.detener()

    def iniciar_voz_seguro(self):
        self.voz.iniciar()
        while not self.voz.exit_flag:
            time.sleep(0.1)
        self.voz.detener()
        Clock.schedule_once(lambda dt: self.toggle_audio_to_off(), 0)

    def toggle_audio_to_off(self):
        self.btn_audio.state = 'normal'  # Cambiado de 'toggle_audio' a 'btn_audio'
        self.btn_audio.text = 'Capturar audio (OFF)'
        self.status_label.text = 'Estado: Inactivo'

    def mostrar_texto(self, texto, idioma):
        Clock.schedule_once(lambda dt: self.status_label_update(texto, idioma), 0)

    def status_label_update(self, texto, idioma):
        self.status_label.text = f"Reconocido: {texto} ({idioma})"
    
    def analizar_cara_detectado(self):
        print("Acción por voz: Analizar cara")
        Clock.schedule_once(lambda dt: self.analizar_cara(self.btn_face), 0)

    def analizar_cara(self, instance):
        print("Botón presionado: Analizar cara")
        self.status_label.text = "Análisis de cara iniciado (botón)"
        self.btn_marker.disabled = True 
        threading.Thread(target=self.ejecutar_analisis_cara, daemon=True).start()

    def ejecutar_analisis_cara(self):
        def actualizar_desde_hilo(texto):
            Clock.schedule_once(lambda dt: self.recomendacion_label_update(texto), 0)

        try:
            analizar_cara_con_insight(actualizar_desde_hilo)
            Clock.schedule_once(lambda dt: self.status_label_update("Análisis completo", "sistema"), 0)
        except Exception as e:
            print("Error durante el análisis facial:", e)
            Clock.schedule_once(lambda dt: self.status_label_update("Error en análisis", "sistema"), 0)
        finally:
            Clock.schedule_once(lambda dt: self.habilitar_boton_marcador(), 0)
    
    def habilitar_boton_marcador(self):
        self.btn_marker.disabled = False

    def analizar_marcador_detectado(self):
        print("Acción por voz: Analizar marcador")
        Clock.schedule_once(lambda dt: self.analizar_marcador(self.btn_marker), 0)

    def analizar_marcador(self, instance):
        print("Botón presionado: Analizar marcador")
        self.status_label.text = "Análisis de marcador iniciado (botón)"
        self.btn_face.disabled = True  # Desactiva botón de cara

        def actualizar_flor_detectada(nombre_flor):
            Clock.schedule_once(lambda dt: self.flor_detectada_label_update(nombre_flor), 0)

        def al_finalizar_ar():
            Clock.schedule_once(lambda dt: self.habilitar_boton_cara(), 0)  # Reactiva

        # Lanzar el hilo
        threading.Thread(
            target=lambda: iniciar_ar(on_flor_detectada=actualizar_flor_detectada, on_close=al_finalizar_ar),
            daemon=True
        ).start()
    
    def habilitar_boton_cara(self):
        self.btn_face.disabled = False

    def flor_detectada_label_update(self, nombre_flor):
        self.flor_detectada_label.text = f"Flor detectada: {nombre_flor}"

    def recomendacion_label_update(self, texto):
     self.recomendacion_label.text = f"Recomendación: {texto}"

if __name__ == '__main__':
    VoiceApp().run()
