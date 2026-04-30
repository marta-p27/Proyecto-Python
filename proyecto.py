# Importamos todo lo necesario
import calendar
from datetime import datetime
import json
import os

# Cargamos horarios
with open('/workspaces/Proyecto-Python/programa/clase.json', 'r', encoding='utf-8') as f:
    datos_horario = json.load(f)

# Lista para los exámenes pendientes
examenes_pendientes = []

# Obtener fecha y hora actual
ahora = datetime.now()
año = ahora.year
mes = ahora.month
hora = ahora.hour

# Saludos 
print("\n" + "*"*50)
if hora < 12:
    print("¡Buenos días! Empieza bien el día organizándote.")
elif hora < 20:
    print("¡Buenas tardes! Aprovecha el resto del día.")
else:
    print("¡Buenas noches! No te olvides añadir las nuevas tareas")
   
print("*"*50+ "\n")
# Enseñar el calendario
print(calendar.month(año, mes))


# Eligir curso
print('ELIGE LA CLASE DONDE ESTÁS')
print('1. 1.º de BACH A (letras)')
print('2. 1.º de BACH A (ciencias)')
print('3. 1.º de BACH B (letras)')
print('4. 1.º de BACH B (ciencias)')
print()
opcion = input('Introduce el número de tu clase (1-4) ')

curso = {
    "1": "1.º BACH A (letras)",
    "2": "1.º BACH A (ciencias)",
    "3": "1.º BACH B (letras)",
    "4": "1.º BACH B (ciencias)"
}

curso_usuario =curso.get(opcion)

if not curso_usuario:
    print('Opción inválida. Reinicia el programa')
    exit()


# Vamos a elegir las horas libres que dispone el usuario para estudiar

    #Con esto vamos a tener ya los días puestos, en principio con solo 0 horas disponibles, valor que se podrá editar a continuación.
disponibilidad_estudio = {
    "Lunes": 0.0,
    "Martes": 0.0,
    "Miércoles": 0.0,
    "Jueves": 0.0,
    "Viernes": 0.0,
    "Sábado": 0.0,
    "Domingo": 0.0
}

dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

print("\n" + "-"*30)
print(" CONFIGURAR HORAS DISPONIBLES")
print("-"*30)
print("Introduce cuántas horas reales puedes estudiar cada día:")

for dia in dias_semana:
    while True: 
        res = input(f"¿Cuántas horas tienes para estudiar el {dia}? (puedes usar un número decimal, pero usa la coma (,) para separar): ")

        try:
            horas = float(res) #para que lo pase a número
            if 0 <= horas <= 24:
                disponibilidad_estudio[dia] = horas
                break 
            
            else:
                print("Error: Introduce un número entre 0 y 24.")
        
        except ValueError:
            print("Error: Escribe un número válido.")


# Empezamos ya con el menú de opciones que tiene el asistente.
while True:
    os.system('clear')
    
    #Menú del asistente
    print("\n" + "="*30)
    print("      MENÚ DEL ASISTENTE")
    print("="*30)
    print("1. Añadir nuevo examen/tarea")
    print("2. Ver horario y horas libres de hoy")
    print("3. Ver tu plan de estudio recomendado.")
    print("4. Salir")

    #Calendario
    print("\n" + "*"*25)
    print(calendar.month(año, mes))
    print("\n" + "*"*25)


    accion = input('¿Qué quieres hacer?')

    if accion == "1":  #aquí el usuario introducirá los exámenes.
        meter_examen = True
         #bucle para añadir varios exámenes a la vez sin tener que pasar por el menú.
        while  meter_examen:
            print ('\nAÑADIR NUEVO EXAMEN.')
            asignatura = input('¿De qué asignatura es?: ')
            dificultad = input('Elige la dificultad: \n1. Difícil\n2. Media\n3. Fácil\n')

            # Según el nivel de dificultad hay diferente cantidad de horas que se va a necesitar añadir
            if dificultad == "1":
                horas_necesarias = 8
            elif dificultad == "2":
                horas_necesarias = 5
            elif dificultad == "3":
                horas_necesarias = 2
            else:
                print("Valor no válido, asignando 3h por defecto")
                horas_necesarias = 3
            fecha_texto = input('Fecha del examen (DD/MM/AAAA): ')

            try:
                # Fecha en modo de texto a modo de fecha real
                fecha_examen = datetime.strptime(fecha_texto, "%d/%m/%Y")
                diasrestantes = (fecha_examen - ahora).days + 1
                print(f"Examen de {asignatura} guardado.\nNecesitarás dedicarle, aproximadamente, {horas_necesarias} horas. Faltan {diasrestantes} días.")
            
                #Guardamos exámenes pendientes:
                examenes_pendientes.append({
                    'asig': asignatura,
                    'dif': dificultad,
                  'dias': diasrestantes,
                 'horas': horas_necesarias
                 })


            except ValueError:
                print("Formato de fecha incorrecto.") #por si el valor de la fecha es incorrecto.

            
            otra = input('\n¿Quieres añadir otro examen? (s/n): ').lower() # pregunta si volver a añadir a otro examen o ir al menú. .lower() para que dé igual mayúsucla/minúscula.
            if otra != 's':
                meter_examen = False
                print("Volviendo al menú principal...")
        

        #Volver al menú
        input('\nPresiona Enter para regresar al menú...')
            

    elif accion == "2":
        #Consultar horario, cargando el día de la semana
        
        dia_hoy = dias_semana[ahora.weekday()]
        horario_clase = datos_horario.get(curso_usuario, {})

        # Vamos a enseñar el horario de hoy o el de mañana, según si ya han terminado las clases o no
        clases_terminadas = False
        if (dia_hoy == "Lunes" and hora >= 18) or (dia_hoy != "Lunes" and hora >= 15):
            clases_terminadas = True

        if clases_terminadas:
            # Calculamos el día de mañana 
            dia_manana = (ahora.weekday() + 1) % 7
            info_dia = horario_clase.get(dia_manana)
            print(f"\nLas clases de hoy ya terminaron")
            
            if info_dia:
                print("\n")
                print(f"====INFORMACIÓN PARA MAÑANA {dia_manana.upper()}====")
                print(f"Materías de hoy: : {info_dia['materias']}")
                print(f"Hora de salida: {info_dia['fin']}")


            else:
                print("No hay clases registradas para mañana. ¡Disfruta del descanso!")

        else:
            print("\n")
            print(f"====INFORMACIÓN PARA HOY {dia_hoy.upper()}====")
            info_dia = horario_clase.get(dia_hoy)

            if info_dia:
                print(f"Materias: {info_dia['materias']}")
                print(f"Hora de salida: {info_dia['fin']}")
            else:
                print("No hay clases registradas para hoy. ¡Disfruta del descanso!")
        
        if examenes_pendientes: #para que escriba los exámenes pendientes.
            print("\n ")
            print("\nRECUERDA TUS EXÁMENES:")
            for ex in examenes_pendientes:
                print(f"- {ex['asig']}: faltan {ex['dias']} días. Necesitarás {ex['horas']} horas para estudiar, aproximadamente")
        
        # Para volver al menú-
        input('\nPresiona Enter para regresar al menú...')


    elif accion == "3":
        print(n)
    
    elif accion == "4":
        print("Saliendo...")
        break
    
    else:
        print("Opción no válida.")

