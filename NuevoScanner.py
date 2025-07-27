import subprocess
import platform
import ipaddress

# Función para hacer ping a la IP
def hacer_ping(ip):
    try:
        # Determina el parámetro correcto para el comando "ping" según el sistema operativo
        param = "-n" if platform.system().lower() == "windows" else "-c"
        
        # Ejecuta el comando "ping" con 1 intento, redirigiendo salida y errores a /dev/null
        resultado = subprocess.run(["ping", param, "1", str(ip)],
                                   stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL)
        
        # Devuelve True si el código de retorno es 0 (éxito)
        return resultado.returncode == 0
    except Exception as e:
        # En caso de error, imprime el mensaje y devuelve False
        print(f"Error al hacer ping a {ip}: {e}")
        return False

# Función para obtener la dirección MAC de una IP usando ARP
def obtener_mac(ip):
    try:
        # Ejecuta el comando ARP dependiendo del sistema operativo
        if platform.system().lower() == "windows":
            resultado = subprocess.check_output(["arp", "-a", str(ip)], text=True)
        else:
            resultado = subprocess.check_output(["arp", "-n", str(ip)], text=True)

        # Recorre cada línea del resultado del comando ARP
        for linea in resultado.splitlines():
            # Busca si la IP aparece en la línea
            if str(ip) in linea:
                partes = linea.split()
                # Busca el campo que contenga ":" o "-" como separador típico de MAC
                for parte in partes:
                    if "-" in parte or ":" in parte:
                        return parte  # Devuelve la MAC encontrada
        # Si no encontró la MAC en ninguna línea
        return "MAC no encontrada"
    except subprocess.CalledProcessError:
        # Si la IP no está en la tabla ARP, devuelve mensaje
        return "No en tabla ARP"

# Función principal para escanear un rango de 254 direcciones IP
def escanear_rango(ip_base_str):
    try:
        # Convierte la IP ingresada en un objeto ip_address
        ip_base = ipaddress.ip_address(ip_base_str)
    except ValueError:
        # Si la IP no es válida, muestra mensaje y termina
        print(" Dirección IP inválida.")
        return

    # Muestra mensaje de inicio del escaneo
    print(f"\n🔍 Escaneando desde {ip_base} hasta {ip_base + 253}...\n")

    # Recorre 254 IPs consecutivas desde la IP base
    for i in range(254):
        ip_actual = ip_base + i  # Calcula la IP actual

        # Omite IPs que sean especiales (loopback, multicast, etc.)
        if ip_actual.is_multicast or ip_actual.is_reserved or ip_actual.is_loopback:
            continue

        # Si responde al ping
        if hacer_ping(ip_actual):
            # Obtiene la MAC si está en la tabla ARP
            mac = obtener_mac(ip_actual)
            # Imprime IP activa y su MAC
            print(f" IP Activa: {ip_actual} - MAC: {mac}")

# Punto de entrada del script
if __name__ == "__main__":
    # Solicita al usuario la IP inicial desde la que comenzar el escaneo
    ip_inicial = input("Introduce IP inicial (por ejemplo 192.168.1.1): ")

    # Llama a la función de escaneo con la IP proporcionada
    escanear_rango(ip_inicial)
