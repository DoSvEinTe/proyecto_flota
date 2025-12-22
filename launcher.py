#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LAUNCHER VISUAL - Sistema FlotaGest
Permite ejecutar el sistema sin conocimientos técnicos
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
from pathlib import Path
import threading
import time

class FlotaLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("🚌 Sistema FlotaGest - Gestor de Flota")
        self.root.geometry("700x700")
        self.root.resizable(False, False)
        
        # Configurar estilo
        self.root.configure(bg="#f0f0f0")
        style = ttk.Style()
        style.theme_use('clam')
        
        # Variables
        self.proceso = None
        self.ejecutando = False
        
        self.crear_interfaz()
        
    def crear_interfaz(self):
        """Crear la interfaz gráfica"""
        
        # Marco superior con título
        marco_titulo = tk.Frame(self.root, bg="#2c3e50", height=100)
        marco_titulo.pack(fill=tk.X)
        
        titulo = tk.Label(
            marco_titulo, 
            text="🚌 SISTEMA DE GESTIÓN DE FLOTA",
            font=("Arial", 18, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        titulo.pack(pady=20)
        
        # Marco principal
        marco_principal = ttk.Frame(self.root, padding="20")
        marco_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Sección de estado
        ttk.Label(marco_principal, text="Estado del Sistema:", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        self.label_estado = ttk.Label(
            marco_principal,
            text="⏸ Detenido",
            font=("Arial", 11),
            foreground="red"
        )
        self.label_estado.pack(anchor=tk.W, pady=(0, 20))
        
        # Sección de información
        ttk.Label(marco_principal, text="Información:", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(10, 5))
        
        info_text = tk.Text(marco_principal, height=8, width=60, relief=tk.SUNKEN, borderwidth=1)
        info_text.pack(pady=(0, 15))
        
        info_contenido = """✓ Python: Detectado
✓ Django: Instalado
✓ Base de datos: MySQL (localhost:3306)
✓ Puerto: 127.0.0.1:8000

Instrucciones:
1. Click en 'Iniciar Sistema'
2. Espera a que aparezca el mensaje de inicio
3. Abre tu navegador en: http://127.0.0.1:8000/
4. Usuario/Contraseña: (según tu configuración)
"""
        info_text.insert(tk.END, info_contenido)
        info_text.config(state=tk.DISABLED)
        
        # Marco de botones principales (Iniciar y Detener)
        marco_botones_principal = tk.Frame(marco_principal, bg="#f0f0f0")
        marco_botones_principal.pack(fill=tk.X, pady=20, padx=5)
        
        # Botón Iniciar con estilo mejorado
        self.btn_iniciar = tk.Button(
            marco_botones_principal,
            text="▶ INICIAR SISTEMA",
            command=self.iniciar_sistema,
            height=3,
            bg="#27ae60",
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            activebackground="#229954",
            activeforeground="white",
            bd=0
        )
        self.btn_iniciar.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        
        # Botón Detener con estilo mejorado
        self.btn_detener = tk.Button(
            marco_botones_principal,
            text="⏹ DETENER",
            command=self.detener_sistema,
            height=3,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            activebackground="#c0392b",
            activeforeground="white",
            state=tk.DISABLED,
            bd=0
        )
        self.btn_detener.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        
        # Separador visual
        separador = tk.Frame(marco_principal, bg="#d0d0d0", height=2)
        separador.pack(fill=tk.X, pady=15)
        
        # Marco inferior con botones secundarios (debe ser más grande)
        marco_inferior = tk.Frame(marco_principal, bg="#f0f0f0")
        marco_inferior.pack(fill=tk.BOTH, pady=15, padx=5, expand=False)
        
        # Botón navegador
        btn_navegador = tk.Button(
            marco_inferior,
            text="🌐 ABRIR NAVEGADOR",
            command=self.abrir_navegador,
            height=2,
            bg="#3498db",
            fg="white",
            font=("Arial", 11, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            activebackground="#2980b9",
            activeforeground="white",
            bd=0
        )
        btn_navegador.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        
        # Botón salir
        btn_salir = tk.Button(
            marco_inferior,
            text="❌ SALIR",
            command=self.salir,
            height=2,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 11, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            activebackground="#7f8c8d",
            activeforeground="white",
            bd=0
        )
        btn_salir.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        
    def iniciar_sistema(self):
        """Iniciar el servidor Django"""
        try:
            self.btn_iniciar.config(state=tk.DISABLED)
            self.btn_detener.config(state=tk.NORMAL)
            self.label_estado.config(text="⏳ Iniciando...", foreground="orange")
            self.root.update()
            
            # Obtener ruta del proyecto
            proyecto_dir = Path(__file__).parent
            
            # Thread para ejecutar el servidor
            thread = threading.Thread(target=self._ejecutar_servidor, args=(str(proyecto_dir),), daemon=True)
            thread.start()
            
            # Esperar a que se inicie
            self.root.after(3000, self._verificar_inicio)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo iniciar el sistema:\n{str(e)}")
            self.btn_iniciar.config(state=tk.NORMAL)
            self.btn_detener.config(state=tk.DISABLED)
            
    def _ejecutar_servidor(self, proyecto_dir):
        """Ejecutar el servidor en un thread"""
        try:
            os.chdir(proyecto_dir)
            
            # Crear archivo de logs
            log_file = Path(proyecto_dir) / "servidor.log"
            
            with open(log_file, "w") as log:
                self.proceso = subprocess.Popen(
                    [sys.executable, "manage.py", "runserver", "0.0.0.0:8000"],
                    stdout=log,
                    stderr=subprocess.STDOUT,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
                )
                self.ejecutando = True
            
            # Esperar a que termine
            self.proceso.wait()
            
        except Exception as e:
            print(f"Error: {e}")
            self.ejecutando = False
            
    def _verificar_inicio(self):
        """Verificar si el servidor inició correctamente"""
        if self.ejecutando:
            self.label_estado.config(text="✅ Sistema en ejecución", foreground="green")
            messagebox.showinfo(
                "Sistema Iniciado",
                "El sistema está listo!\n\n"
                "Abre tu navegador en:\nhttp://127.0.0.1:8000/"
            )
        else:
            self.label_estado.config(text="❌ Error al iniciar", foreground="red")
            messagebox.showerror(
                "Error",
                "No se pudo iniciar el sistema.\n"
                "Verifica que MySQL esté corriendo."
            )
            self.btn_iniciar.config(state=tk.NORMAL)
            self.btn_detener.config(state=tk.DISABLED)
            
    def abrir_navegador(self):
        """Abrir el navegador en la URL del sistema"""
        import webbrowser
        try:
            webbrowser.open("http://127.0.0.1:8000/")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el navegador:\n{str(e)}")
            
    def detener_sistema(self):
        """Detener el servidor"""
        try:
            self.label_estado.config(text="⏳ Deteniendo...", foreground="orange")
            self.root.update()
            
            # Intentar matar el proceso de forma agresiva
            if sys.platform == "win32":
                # En Windows, matar todos los procesos python que corran manage.py
                os.system("taskkill /F /IM python.exe /FI \"WINDOWTITLE eq*manage*\" /T 2>nul || taskkill /F /IM python.exe /T 2>nul")
                time.sleep(1)
            else:
                # En Linux/Mac, matar el proceso en el puerto 8000
                os.system("fuser -k 8000/tcp 2>/dev/null || true")
                time.sleep(1)
            
            self.proceso = None
            self.ejecutando = False
            self.label_estado.config(text="⏸ Detenido", foreground="red")
            self.btn_iniciar.config(state=tk.NORMAL)
            self.btn_detener.config(state=tk.DISABLED)
            messagebox.showinfo("Sistema Detenido", "El sistema se ha detenido correctamente.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al detener:\n{str(e)}")
            self.label_estado.config(text="⏸ Detenido", foreground="red")
            
    def salir(self):
        """Salir de la aplicación"""
        if self.ejecutando:
            if messagebox.askyesno("Confirmar", "¿Detener el sistema y salir?"):
                self.detener_sistema()
                self.root.quit()
        else:
            self.root.quit()


def main():
    """Función principal"""
    root = tk.Tk()
    app = FlotaLauncher(root)
    root.mainloop()


if __name__ == "__main__":
    main()
