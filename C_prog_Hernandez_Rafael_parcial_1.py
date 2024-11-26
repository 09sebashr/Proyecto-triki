# Importamos las librerías necesarias
import random  # Para generar movimientos aleatorios para la IA
import hashlib  # Para encriptar contraseñas usando SHA-256

# Lista para almacenar los usuarios y sus estadísticas (victorias, derrotas, empates)
usuarios = []

# Función para imprimir el tablero del juego
def imprimir_tablero(tablero):
    for fila in tablero:  # Recorre cada fila del tablero
        print(' ' + ' | '.join(fila))  # Imprime los valores de la fila con separadores
        print('---|---|---')  # Dibuja las líneas divisorias del tablero

# Función para verificar si un jugador ha ganado
def verificar_ganador(tablero, jugador):
    # Combinaciones ganadoras posibles (filas, columnas y diagonales)
    combinaciones_ganadoras = [
        [(0, 0), (0, 1), (0, 2)],  # Fila superior
        [(1, 0), (1, 1), (1, 2)],  # Fila media
        [(2, 0), (2, 1), (2, 2)],  # Fila inferior 
        [(0, 0), (1, 0), (2, 0)],  # Columna izquierda 
        [(0, 1), (1, 1), (2, 1)],  # Columna central 
        [(0, 2), (1, 2), (2, 2)],  # Columna derecha 
        [(0, 0), (1, 1), (2, 2)],  # Diagonal principal     
        [(0, 2), (1, 1), (2, 0)],  # Diagonal inversa
    ]
    # Verificamos si alguna de las combinaciones ganadoras está completa con el jugador actual
    for combinacion in combinaciones_ganadoras:
        if all(tablero[i][j] == jugador for i, j in combinacion):
            return True
    return False  # Si no hay combinación ganadora, retornamos False

# Función para verificar si el juego terminó en empate
def verificar_empate(tablero):
    # El juego está en empate si no hay espacios vacíos en el tablero
    return all(tablero[i][j] != ' ' for i in range(3) for j in range(3))

# Función para manejar la jugada del usuario
def jugada_usuario(tablero):
    while True:
        try:
            # El usuario elige una posición entre 1 y 9
            mov = int(input("Elige una posición (1-9): ")) - 1
            i, j = divmod(mov, 3)  # Convierte el número en índices (i, j)
            if 0 <= i < 3 and 0 <= j < 3 and tablero[i][j] == ' ':
                tablero[i][j] = 'X'  # Marca la posición elegida con 'X'
                print(f"Has elegido la posición {mov + 1}.")
                break
            else:
                print("Posición no válida o ya ocupada. Inténtalo de nuevo.")
        except ValueError:
            print("Entrada no válida. Debes ingresar un número del 1 al 9.")

# Función para ordenar el array de posiciones libres usando el algoritmo Combsort
def combsort(arr):
    gap = len(arr)
    shrink = 1.3
    sorted = False
    
    while not sorted:
        gap = max(1, int(gap / shrink))  # Calcula el nuevo gap
        sorted = True
        
        # Compara elementos en las posiciones gap y realiza intercambios si es necesario
        for i in range(len(arr) - gap):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                sorted = False
    return arr

# Función para manejar la jugada de la IA
def jugada_ia(tablero):
    opciones = obtener_posiciones_libres(tablero)  # Obtiene las posiciones libres
    sorted_opciones = combsort(opciones)  # Ordena las posiciones libres
    mov = random.choice(sorted_opciones)  # Elige aleatoriamente una de las opciones
    tablero[mov[0]][mov[1]] = 'O'  # Marca la posición elegida con 'O'
    print(f"La IA elige la posición {mov[0] * 3 + mov[1] + 1}.")

# Función para obtener las posiciones libres del tablero
def obtener_posiciones_libres(tablero):
    return [(i, j) for i in range(3) for j in range(3) if tablero[i][j] == ' ']

# Función principal del juego Triki
def triqui(usuario):
    tablero = [[' ' for _ in range(3)] for _ in range(3)]  # Inicializa un tablero vacío 3x3
    jugador = 'X'  # El jugador empieza con 'X'
    
    print("Bienvenido al juego de Triki!")
    
    while True:
        if jugador == 'X':  # Si es turno del jugador
            jugada_usuario(tablero)
            imprimir_tablero(tablero)
            if verificar_ganador(tablero, jugador):  # Verifica si el jugador ha ganado
                print(f"¡Felicidades {usuario['nombre']}! Ganaste.")
                usuario['victorias'] += 1
                break
            if verificar_empate(tablero):  # Verifica si es empate
                print("¡Es un empate!")
                usuario['empates'] += 1
                break
            jugador = 'O'  # Cambia al turno de la IA
        else:  # Si es turno de la IA
            jugada_ia(tablero)
            imprimir_tablero(tablero)
            if verificar_ganador(tablero, 'O'):  # Verifica si la IA ha ganado
                print(f"La IA ha ganado. ¡Mejor suerte la próxima vez {usuario['nombre']}!")
                usuario['derrotas'] += 1
                break
            if verificar_empate(tablero):  # Verifica si es empate
                print("¡Es un empate!")
                usuario['empates'] += 1
                break
            jugador = 'X'  # Cambia al turno del jugador



#################################################################################################



# Función para encriptar la contraseña con SHA-256
def encriptar_contraseña(contraseña):
    return hashlib.sha256(contraseña.encode()).hexdigest()

# Función para verificar si la contraseña proporcionada coincide con la encriptada
def verificar_contraseña(contraseña, contraseña_encriptada):
    return encriptar_contraseña(contraseña) == contraseña_encriptada

# Función para registrar un nuevo usuario
def registrar_usuario():
    nombre = input("Ingresa el nombre del usuario: ")
    while True:
        contraseña = input("Ingresa una contraseña: ")
        confirmacion = input("Confirma la contraseña: ")
        if contraseña == confirmacion:
            break  # Si las contraseñas coinciden, continúa
        else:
            print("Las contraseñas no coinciden. Intenta de nuevo.")
    
    contraseña_encriptada = encriptar_contraseña(contraseña)
    
    # Crea un diccionario para almacenar los datos del usuario
    usuario = {
        'nombre': nombre,
        'contraseña': contraseña_encriptada,
        'victorias': 0,
        'derrotas': 0,
        'empates': 0
    }
    usuarios.append(usuario)  # Agrega el usuario a la lista
    print(f"Usuario {nombre} registrado exitosamente.")

# Función para iniciar sesión
def iniciar_sesion():
    nombre = input("Ingresa tu nombre de usuario: ")
    for usuario in usuarios:
        if usuario['nombre'] == nombre:
            contraseña = input("Ingresa tu contraseña: ")
            if verificar_contraseña(contraseña, usuario['contraseña']):  # Verifica la contraseña
                print(f"Bienvenido, {nombre}!")
                return usuario
            else:
                print("Contraseña incorrecta.")
                return None
    print("Usuario no encontrado.")
    return None

# Función para editar un usuario (renombrar)
def editar_usuario():
    nombre = input("Ingresa el nombre del usuario a editar: ")
    for usuario in usuarios:
        if usuario['nombre'] == nombre:
            print(f"Editando usuario {nombre}.")
            nuevo_nombre = input("Ingresa el nuevo nombre: ")
            usuario['nombre'] = nuevo_nombre  # Cambia el nombre del usuario
            print(f"Usuario {nombre} ha sido renombrado a {nuevo_nombre}.")
            return
    print("Usuario no encontrado.")

# Función para listar todos los usuarios
def listar_usuarios():
    if not usuarios:  # Si no hay usuarios registrados, muestra un mensaje
        print("No hay usuarios registrados.")
        return
    for usuario in usuarios:
        # Muestra el nombre y las estadísticas del usuario
        print(f"Nombre: {usuario['nombre']}, Victorias: {usuario['victorias']}, Derrotas: {usuario['derrotas']}, Empates: {usuario['empates']}")

# Función para eliminar un usuario
def eliminar_usuario():
    nombre = input("Ingresa el nombre del usuario a eliminar: ")
    for i, usuario in enumerate(usuarios):
        if usuario['nombre'] == nombre:
            del usuarios[i]  # Elimina el usuario de la lista
            print(f"Usuario {nombre} eliminado exitosamente.")
            return
    print("Usuario no encontrado.")

# Menú principal que permite al usuario elegir opciones
def menu_principal():
    while True:
        print("\nBienvenido al Menú Principal")
        print("1. Registrar nuevo usuario")
        print("2. Iniciar sesión")
        print("3. Editar usuario")
        print("4. Listar usuarios")
        print("5. Eliminar usuario")
        print("6. Jugar Triki")
        print("7. Salir")
        opcion = input("Elige una opción (1-7): ")
        
        if opcion == '1':
            registrar_usuario()
        elif opcion == '2':
            usuario = iniciar_sesion()  # Inicia sesión con el nombre de usuario
            if usuario:
                triqui(usuario)  # Si el usuario inicia sesión correctamente, empieza el juego
        elif opcion == '3':
            editar_usuario()
        elif opcion == '4':
            listar_usuarios()
        elif opcion == '5':
            eliminar_usuario()
        elif opcion == '6':
            if not usuarios:
                print("No hay usuarios registrados para jugar.")
                continue
            nombre_usuario = input("Ingresa el nombre del usuario que jugará: ")
            for usuario in usuarios:
                if usuario['nombre'] == nombre_usuario:
                    triqui(usuario)  # Empieza el juego con el usuario elegido
                    break
            else:
                print("Usuario no encontrado.")
        elif opcion == '7':
            print("Gracias por jugar. ¡Hasta pronto!")
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")

# Inicio del programa
if __name__ == "__main__":
    menu_principal()
