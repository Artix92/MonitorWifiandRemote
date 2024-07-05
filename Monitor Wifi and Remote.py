import subprocess
import time
import keyboard

def is_connected_to_wifi(network_name):
    try:
        result = subprocess.check_output(["netsh", "wlan", "show", "interfaces"], encoding='latin-1')
        return network_name in result
    except subprocess.CalledProcessError:
        return False

def connect_to_wifi(network_name):
    try:
        subprocess.check_output(["netsh", "wlan", "connect", "name={}".format(network_name)], encoding='latin-1')
        print(f"Conectado a {network_name}")
    except subprocess.CalledProcessError:
        print(f"No se pudo conectar a {network_name}")

def disconnect_from_wifi():
    try:
        subprocess.check_output(["netsh", "wlan", "disconnect"], encoding='latin-1')
        print("Desconectado de la red Wi-Fi")
        time.sleep(10)  # Esperar 10 segundos
    except subprocess.CalledProcessError:
        print("No se pudo desconectar de la red Wi-Fi")

def is_remote_connection_stable(target_ip="8.8.8.8"): #Tu ip a la que harás ping
    try:
        result = subprocess.check_output(["ping", "-n", "1", target_ip], encoding='latin-1')
        return "TTL=" in result
    except subprocess.CalledProcessError:
        return False


#--------------------------------------------------------------------------------#


def monitor_wifi_and_remote():
    network_name = "Tu_wifi" #Cambiar esta parte
    paused = False

    print("Monitoreo iniciado. Presiona Ctrl+Q para salir, Ctrl+P para pausar/reanudar.")
    #parte opcional no funciona muy bien y con Ctrl + C es lo mismo.
    while True:
        if keyboard.is_pressed('ctrl+q'):
            print("Proceso terminado.")
            break
        elif keyboard.is_pressed('ctrl+p'):
            paused = not paused
            if paused:
                print("Monitoreo pausado.")
            else:
                print("Monitoreo reanudado.")
            time.sleep(1)  # Evitar múltiples detecciones de la tecla

        if not paused:
            print("Monitoreando conexión Wi-Fi...")
            if not is_connected_to_wifi(network_name):
                print(f"No conectado a {network_name}. Intentando reconectar...")
                connect_to_wifi(network_name)
            else:
                print(f"Conectado a {network_name}")
            
            print("Monitoreando estabilidad de conexión remota...")
            if not is_remote_connection_stable():
                print("Conexión remota inestable. Intentando reconectar...")

                disconnect_from_wifi()

                connect_to_wifi(network_name)
                # Aquí puedes intentar reconectar tu sesión remota si es posible
            else:
                print("Conexión remota estable.")

        time.sleep(15)  # Esperar 15 segundos

if __name__ == "__main__":
    monitor_wifi_and_remote()
