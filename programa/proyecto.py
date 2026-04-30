# Importamos todo lo necesario
import calendar
from datetime import datetime
import json
import os
import time

# Cargamos horarios
with open("/workspaces/Proyecto-Python/programa/clase.json", "r", encoding="utf-8") as f:
    datos_horario = json.load(f)

# Lista para los exámenes pendientes
examenes_pendientes = []

# Obtener fecha y hora actual
ahora = datetime.now()
año = ahora.year
mes = ahora.month
hora = ahora.hour

#Días de la semana y día actual
dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
dia_hoy = dias_semana[ahora.weekday()]


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
input("Pulsa Enter para empezar seleccionando tu clase.")

print("\nELIGE LA CLASE DONDE ESTÁS")
print("1. 1.º de BACH A (letras)")
print("2. 1.º de BACH A (ciencias)")
print("3. 1.º de BACH B (letras)")
print("4. 1.º de BACH B (ciencias)\n")

opcion = input("Introduce el número de tu clase (1-4) ")

curso = {
    "1": "1.º BACH A (letras)",
    "2": "1.º BACH A (ciencias)",
    "3": "1.º BACH B (letras)",
    "4": "1.º BACH B (ciencias)"
}

curso_usuario =curso.get(opcion)


if not curso_usuario:
    print("Opción inválida. Reinicia el programa")
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


print("\n" + "="*30)
print(" CONFIGURAR HORAS DISPONIBLES")
print("="*30)
print("\nIntroduce cuántas horas reales puedes estudiar cada día:\n (Nota: puedes usar 1 número decimal (0.0) pero usa el punto para separar).")

for dia in dias_semana:
    while True: 
        res = input(f"¿Cuántas horas tienes para estudiar el {dia.lower()}?")

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


    accion = input("¿Qué quieres hacer?")

    if accion == "1":  #aquí el usuario introducirá los exámenes.
        meter_examen = True
         #bucle para añadir varios exámenes a la vez sin tener que pasar por el menú.
        while  meter_examen:
            print ("\nAÑADIR NUEVO EXAMEN.")
            asignatura = input("¿De qué asignatura es?: ")
            dificultad = input("Elige la dificultad: \n1. Difícil\n2. Media\n3. Fácil\n")

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
                    "asig": asignatura,
                    "dif": dificultad,
                  "dias": diasrestantes,
                 "horas": horas_necesarias
                 })


            except ValueError:
                print("Formato de fecha incorrecto.") #por si el valor de la fecha es incorrecto.

            
            otra = input("\n¿Quieres añadir otro examen? (s/n): ").lower() # pregunta si volver a añadir a otro examen o ir al menú. .lower() para que dé igual mayúsucla/minúscula.
            if otra != "s":
                meter_examen = False
                print("Volviendo al menú principal...")
        

        #Volver al menú
        input("\nPresiona Enter para regresar al menú...")
            

    elif accion == "2":
        #Consultar horario, cargando el día de la semana
        
        
        horario_clase = datos_horario.get(curso_usuario, {})

        # Vamos a enseñar el horario de hoy o el de mañana, según si ya han terminado las clases o no
        clases_terminadas = False
        if (dia_hoy == "Lunes" and hora >= 18) or (dia_hoy != "Lunes" and hora >= 15):
            clases_terminadas = True

        if clases_terminadas:
            # Calculamos el día de mañana 
            indice_manana = (ahora.weekday() + 1) % 7 #conseguimos el día de mañana pero en número
            dia_manana = dias_semana[indice_manana] #lo pasamos a texto (Lunes, Martes)
            info_dia = horario_clase.get(dia_manana)
        
            
            info_dia = horario_clase.get(dia_manana)
            print(f"Las clases de hoy ya terminaron")
            
            if info_dia:
                print("\n")
                print(f"====INFORMACIÓN PARA MAÑANA {dia_manana.upper()}====")
                print(f"Materias de mañana: {info_dia["materias"]}")
                print(f"Hora de salida: {info_dia["fin"]}")


            else:
                print("No hay clases registradas para mañana. ¡Disfruta del descanso!")

        else:
            print("\n")
            print(f"====INFORMACIÓN PARA HOY {dia_hoy.upper()}====")
            info_dia = horario_clase.get(dia_hoy)

            if info_dia:
                print(f"Materias: {info_dia["materias"]}")
                print(f"Hora de salida: {info_dia["fin"]}")
            else:
                print("No hay clases registradas para hoy. ¡Disfruta del descanso!")
        
        if examenes_pendientes: #para que escriba los exámenes pendientes.
            print("\n ")
            print("\nRECUERDA TUS EXÁMENES:")
            for ex in examenes_pendientes:
                print(f"- {ex["asig"]}: faltan {ex["dias"]} días. Necesitarás {ex["horas"]} horas para estudiar, aproximadamente")
        
        # Para volver al menú-
        input("\nPresiona Enter para regresar al menú...")


    elif accion == "3":
        print("\n" + "="*35)
        print("   TU PLANIFICACIÓN SEMANAL")
        print("="*35)

        if not examenes_pendientes:
            print("No tienes exámenes anotados. ¡Disfruta de tu tiempo libre!")
        else:
            puede = disponibilidad_estudio.get(dia_hoy, 0)

            print(f"Hoy {dia_hoy.lower()} tienes disponibles {puede} horas para estudiar.\n")

            suma_debe = 0 #para abrir esta nueva variablr

            for ex in examenes_pendientes:

                debe = round(ex["horas"] / max(1, ex["dias"]), 1) #horas disponibles ÷ días que quedan, siendo round para que solo ponga un decimal round(..., 1) y max 1 para que no divida entre 0
                suma_debe += debe # (+= sería suma_debe=suma_debe + debe)

                print(f"• {ex["asig"]}:")
                print(f"  Debes dedicarle hoy: {debe}h")
                
                if debe > puede:
                    print(f"¡OJO! Este examen solo ya supera tus horas de hoy.")
                print("-" * 20)

            
            # Resumen final 
            print(f"\nTOTAL QUE DEBERÍAS ESTUDIAR HOY: {round(suma_debe, 1)}h") #round para que quede bonito.
            
            if suma_debe > puede:
                print(f"No te da tiempo. Te faltan {round(suma_debe - puede, 1)}h.")
                print("Consejo: Quita horas de ocio y aprovecha bien el tiempo.")

            elif suma_debe == puede:
                print("Las horas que debes de estudiar hoy son iguales a las que estás disponible.")
                print("¡Qué bien planificado!")
            
            else:
                print(f"¡Plan perfecto! Te sobrarán {round(puede - suma_debe, 1)}h libres.")


        input("\nPresiona Enter para regresar al menú...")   
    
    elif accion == "4":
        print("Saliendo...")
        break
     
    else:
        print("Opción no válida.")
        time.sleep(3)

