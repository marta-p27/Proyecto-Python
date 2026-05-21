# Importamos todo lo necesario
import calendar
from datetime import datetime, timedelta
import json
import os
import time

#Formateo de horas para que sea 1:30 y no 1.5h
def formatear_horas(decimal):
    horas = int(decimal)
    minutos = int((decimal % 1) * 60)
    return f"{horas}:{minutos:02d}"

# :02d significa: 
    #    - ':' inicia la regla de formato.
    #    - '0' rellena con ceros a la izquierda si falta espacio.
    #    - '2' obliga a que el número tenga mínimo 2 dígitos de ancho.
    #    - 'd' le dice que es un número entero (dígito).

# Pruebas:
print(formatear_horas(1.5))   # 1:30
print(formatear_horas(2.75))  # 2:45
print(formatear_horas(0.08))  # 0:04

# Cargamos horarios y el json de datos(si existe)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_HORARIO = os.path.join(BASE_DIR, "clase.json")
RUTA_DATOS_USUARIO = os.path.join(BASE_DIR, "datos_usuario.json")

with open(RUTA_HORARIO, "r", encoding="utf-8") as f:
    datos_horario = json.load(f)


def cargar_datos():
    #   Buscamos si el archivo de "datos_usuario.json" ya existe
    if os.path.exists(RUTA_DATOS_USUARIO):
        with open(RUTA_DATOS_USUARIO, "r", encoding="utf-8") as f:
            return json.load(f)
    
    # Para cuando no existe (la primera vez que se abre el programa), de modo que se crea solo-
    return {
        "clase": None,
        "disponibilidad": {
            "Lunes": 0.0, 
            "Martes": 0.0, 
            "Miércoles": 0.0, 
            "Jueves": 0.0, 
            "Viernes": 0.0, 
            "Sábado": 0.0, 
            "Domingo": 0.0
        },
        "examenes": []
    }


# Cargamos los datos
datos_usuario = cargar_datos()
clase_usuario = datos_usuario.get("clase")

# Separamos en variables 
examenes_pendientes = datos_usuario["examenes"]
disponibilidad_estudio = datos_usuario["disponibilidad"]

# Guardar cambios después de editar o borrar
def guardar_todo():
    datos = {
        "clase": clase_usuario,
        "disponibilidad": disponibilidad_estudio,
        "examenes": examenes_pendientes
    }
    with open(RUTA_DATOS_USUARIO, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)



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
input("Pulsa Enter para empezar. ")

#Si no está seleccionado el cursi
if not clase_usuario:
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

    clase_usuario =curso.get(opcion)


    if not clase_usuario:
        print("Opción inválida. Reinicia el programa.")
        exit()

    guardar_todo()
    print(f"Clase configurada: {clase_usuario}")

else:
    print(f"Bienvenido de nuevo. Clase actual: {clase_usuario}")
    time.sleep(3)



# Introducir las horas disponibles
todas_a_cero = all(v == 0.0 for v in disponibilidad_estudio.values())

if todas_a_cero:
    print("\n" + "="*30)
    print(" CONFIGURAR HORAS DISPONIBLES")
    print("="*30)
    print("\nIntroduce cuántas horas reales puedes estudiar cada día:\n (Nota: puedes usar 1 número decimal (0.0) pero usa el punto para separar).")

    for dia in dias_semana:
        while True: 
            res = input(f"¿Cuántas horas tienes para estudiar el {dia.lower()}? ")

            try:
                horas = float(res) #para que lo pase a número
                if 0 <= horas <= 24:
                    disponibilidad_estudio[dia] = horas
                    break 
            
                else:
                    print("Error: Introduce un número entre 0 y 24.")
        
            except ValueError:
                print("Error: Escribe un número válido.")

    guardar_todo() 
    print("\nDisponibilidad guardada correctamente.")
    time.sleep(1)


# Empezamos ya con el menú de opciones que tiene el asistente.
while True:
    os.system('clear') #limpiar
    ahora = datetime.now() #por si pasa mucho tiempo abierto, para que no quede con la hora obsoleta
    hora = ahora.hour
    
    #Menú del asistente
    print("\n" + "="*30)
    print("      MENÚ DEL ASISTENTE")
    print("="*30)
    print("1. Añadir nuevo examen")
    print("2. Eliminar o editar exámenes guardados")
    print("3. Ver horario, horas libres de hoy y calendario")
    print("4. Ver tu plan de estudio recomendado.")
    print("5. Editar disponibilidad")
    print("6. Salir")


    accion = input("¿Qué quieres hacer? Introduce el número correspondiente (1-4): ")

    if accion == "1":  #aquí el usuario introducirá los exámenes.
        meter_examen = True
         #bucle para añadir varios exámenes a la vez sin tener que pasar por el menú.
        while  True:

            print ("\nAÑADIR NUEVO EXAMEN.")
            asignatura = input("¿De qué asignatura es?: ")
            dificultad = input("Elige la dificultad: \n1. Difícil\n2. Media\n3. Fácil\n")

            # Según el nivel de dificultad hay diferente cantidad de horas que se va a necesitar añadir
            if dificultad == "1":
                horas_necesarias = 15
            elif dificultad == "2":
                horas_necesarias = 10
            elif dificultad == "3":
                horas_necesarias = 4
            else:
                print("Valor no válido, asignando 3h por defecto")
                horas_necesarias = 3
            

            while True:
                fecha_texto = input('Fecha del examen (DD/MM/AAAA): ')
                try:
                # Fecha en modo de texto a modo de fecha real
                    fecha_examen = datetime.strptime(fecha_texto, "%d/%m/%Y")
                    diasrestantes = (fecha_examen - ahora).days + 1
                    

                    if diasrestantes < 0:
                        print("Error: La fecha introducida ya ha pasado. Introduce una fecha futura.")
                        continue
                    
                    print(f"Examen de {asignatura} guardado.\nNecesitarás dedicarle, aproximadamente, {horas_necesarias} horas. Faltan {diasrestantes} días.")

                    #Guardamos exámenes pendientes:
                    examenes_pendientes.append({
                        "asig": asignatura,
                        "dif": dificultad,
                        "fecha": fecha_texto,
                        "horas": horas_necesarias
                        })
                
                    guardar_todo()
                    break #salimos del bucle de la fecha al estar todo bien
                
                except ValueError:
                    print("Formato de fecha incorrecto.") #por si el valor de la fecha es incorrecto.

            
            respuesta = input("\n¿Quieres añadir otro examen? (s/n): ").lower() # pregunta si volver a añadir a otro examen o ir al menú. .lower() para que dé igual mayúsucla/minúscula.
            if respuesta != "s":
                meter_examen = False
                print("Volviendo al menú principal...")
                time.sleep(2)
                break
        

            

    elif accion == "2":
        ahora = datetime.now()
        
        print("\nEDITAR/ELIMINAR EXÁMENES GUARDADOS")

        if not examenes_pendientes:
            print("No hay exámenes pendientes guardados.¡Disfruta!")
            input("\nPulsa Enter para volver ")

        else:
            
            for i, ex in enumerate(examenes_pendientes): #enumera los examenes
                print(f"{i+1}. {ex['asig']}: (horas necesarias {ex['horas']} - {ex['fecha']})") 

            print("\n¿Qué quieres hacer?")
            print("1. Eliminar un examen")
            print("2. Editar un examen")
            print("3. Volver")

            opcion = input("")

            if opcion == "1":

                editar_examen = True

                while True:
                    # Mostramos la lista actualizada cada vez
                    print("\nLISTA PARA ELIMINAR:")
                    for i, ex in enumerate(examenes_pendientes):
                        print(f"{i+1}. {ex['asig']}")
                
                    entrada = input("\nN.º del examen a borrar (o 's' para salir): ").lower()
                
                    if entrada == 's':
                        break # Salimos del bucle de borrar
                
                    try:
                        indice = int(entrada) - 1 #int convierte a número y ponemos como -1 porque empezamos con 1. para que sea más estético
                        if 0 <= indice < len(examenes_pendientes):
                            borrado = examenes_pendientes.pop(indice) 
                            guardar_todo() 
                            print(f"¡Examen de {borrado['asig']} eliminado!")

                            if not examenes_pendientes:
                                print("No quedan más exámenes.")
                                break
                        
                        else:
                            print("Número fuera de rango.")
                            continue
                        
                    except ValueError:
                        print("Por favor, introduce un número o 's'.")

                # Editar
            elif opcion == "2":
                try:

                    indice = int(input("Número del examen a editar: ")) - 1 
                    if 0 <= indice < len(examenes_pendientes): 
                        ex = examenes_pendientes[indice]
                        print(f"\nEditando {ex['asig']}. (Pulsa Enter para mantener actual)")
            
                        nueva_asig = input(f"Nueva asignatura [{ex['asig']}]: ")
                        if nueva_asig: 
                            ex['asig'] = nueva_asig
            
                        nueva_dif = input(f"Nueva dificultad (1 (díficil), 2 (medio), 3 (fácil)) [{ex['dif']}]: ")
                        if nueva_dif:
                            ex['dif'] = nueva_dif
                            horas_map = {"1": 8, "2": 5, "3": 2}
                            ex['horas'] = horas_map.get(nueva_dif, 3)
            
                        guardar_todo()
                        print("Examen actualizado con éxito.")
                    else:
                        print("Ese examen no existe.")

                except ValueError:
                    print("Entrada inválida.")


            # Volver a menú principal
            elif opcion == "3":
                print("Volviendo al menú principal...")
                time.sleep(2)
                break

                
        


    elif accion == "3":


        #Consultar horario, cargando el día de la semana 
        horario_clase = datos_horario.get(clase_usuario, {})

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
                print(f"Materias de mañana: {info_dia['materias']}")
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
                print(f"· {ex['asig']}: faltan {ex['dias']} días. Necesitarás {ex['horas']} horas para estudiar, aproximadamente")
        
        respuesta = input("¿Quieres ver el calendario de este mes y el mes que viene? (s/n)")
        if respuesta == "s":
            
             # Cálculo del mes que viene y el año que viene
            mes_sig = mes + 1
            año_sig = año
            if mes_sig > 12:
                mes_sig = 1
                año_sig = año + 1
             
             #Calendario
            print("\n" + "*"*25)
            print(calendar.month(año, mes))
            print("*"*25)
            print(calendar.month(año_sig, mes_sig))
            print("*"*25)

            


        # Para volver al menú.
        input("\nPresiona Enter para regresar al menú...").lower()

        

    elif accion == "4":
        print("\n" + "="*35)
        print("   TU PLANIFICACIÓN SEMANAL")


        print("="*35)

        if not examenes_pendientes:
            print("No tienes exámenes anotados. ¡Disfruta de tu tiempo libre!")
        else:
            puede = disponibilidad_estudio.get(dia_hoy, 0) #obtener la disponibilidad uardada para este día de la semana. si no hay, devuelve 0.
           
            
            #Filtro inteligente
            MAX_DIAS_ANTICIPACION = 14  # Si el examen está a más de 2 semanas, no mandará estudiar aún
            MIN_HORAS_SESION = 0.5      # Si toca estudiar menos de 30 minutos (0.5h), se ignora para evitar que ponga que estudies 0.1 h

            horas_futuras = []
            #Lista de disponibilidad futura
            for i in range(100):
                fecha = ahora + timedelta(days=i)

                nombre_dia = dias_semana[fecha.weekday()]


                horas = disponibilidad_estudio.get(nombre_dia,0)
                

                horas_futuras.append({
                    'fecha': fecha,
                    'horas': horas,
                    'dias_hasta_hoy': i
                })

                horas_totales_examenes = 0

                # Aquí guardaremos lo que se recomienda estudiar HOY
            planificacion_hoy = []
            
            # Recorremos cada examen para calcular su proporción individual
            for ex in examenes_pendientes:
                fecha_ex = datetime.strptime(ex['fecha'], "%d/%m/%Y")

                # Calculamos días limpios restando solo las fechas
                dias_restantes = (fecha_ex.date() - ahora.date()).days
                
                # Por si el examen está pasado o muy lejos
                if 0 <= dias_restantes <= MAX_DIAS_ANTICIPACION:
                    
                    # Total de horas de estudio disponibles hasta el examen
                    disponibilidad_estudio_total = 0
                    for dia_futuro in horas_futuras:
                        if dia_futuro['dias_hasta_hoy'] < dias_restantes:
                            disponibilidad_estudio_total += dia_futuro["horas"]
                    
                    # Proporcion de estudio
                    if disponibilidad_estudio_total > 0 and puede > 0:

                        # horas de hoy / horas totales de estudio disponibles
                        proporcion = puede / disponibilidad_estudio_total
                        
                        # Horas asignadas para este examen hoy
                        horas_asignadas_hoy = ex['horas'] * proporcion
                        
                        # Evitar el estudia 0.01h. 
                        if horas_asignadas_hoy >= MIN_HORAS_SESION:
                            planificacion_hoy.append({
                                'asig': ex['asig'],
                                'horas': round(horas_asignadas_hoy, 1), #para redondear
                                'faltan': dias_restantes,
                                'fecha': ex['fecha']
                            })


            # Escribir la planificación
            if puede == 0:
                print("\nHoy tienes 0 horas para estudiar.")

            elif not planificacion_hoy:
                print("\nAún falta un tiempo considerable para tus exámenes o el tiempo que el deberías de dedicar es insignificante.")
                print("¡Disfruta!")
                print("\nLos examenes futuros son:")
                for ex in examenes_pendientes:    
                    print(f"-{ex['asig']}: {ex['fecha']} (horas recomendadas por dificultad: {ex['horas']}.")

            else:
                print("Te recomendamos estudiar hoy:")
                debe = 0
                for plan in planificacion_hoy:
                    print(f"\n· {plan['asig'].upper()} ({plan['fecha']}): {formatear_horas(plan['horas'])}h (faltan {plan['faltan']} días)") #.upper() para que esté el nombre en mayúsculas.
                    if plan['horas'] > puede:
                        print("  —> Cuidado, el tiempo que deberías dedicarle a este examen hoy ya sobre pasa todo tu tiempo disponible de hoy.")
                    debe += plan['horas']
                
                # Alerta extra por si acumulas demasiados exámenes y se te exige más de lo que puedes dar hoy
                if debe > puede:
                    print(f"\nNota: La suma recomendada ({formatear_horas(round(debe, 1))}h) supera tus {puede}h reales de hoy.")
                    print("Te sugerimos priorizar las asignaturas que te resulten más difíciles y quitar tiempo de ocio (¡lo agradecerás después!).")


                elif debe == puede:
                    print("\n¡Qué bien planificado! Justo tienes disponible las horas que te recomendamos estudiar.")

                else:
                    print(f"\n¡Plan perfecto! Te sobran {formatear_horas(puede - debe)} horas. ¡Disfruta del tiempo libre extra!")

        input("\nPresiona Enter para regresar al menú...")   
    
    elif accion == "5":

        print("\nEDITAR DISPONIBILIDAD")
        print("Actualmente, tienes registrado como disponibilidad:")
        
        for dia, horas in disponibilidad_estudio.items(): # enseñamos lo guardado
            print(f"- {dia}: {horas} h")

        
        print("1. Editar un día en específico")
        print("2. Editar todos los días")
        print("3. Salir.")

        dis_opcion = input("¿Qué quieres hacer? ")

        if dis_opcion == "1":
            dia_cambio = input("\n¿Qué día quieres editar? (p.e: Lunes, Martes, Miércoles)").strip().capitalize()
            cambiar_hora = True 
            while True:
                if dia_cambio in disponibilidad_estudio:
                    while True:
                        horas = int(input(f"¿Cuántas horas tienes para estudiar el {dia_cambio.lower()}"))

                        try: 
                            if 0 <= horas <= 24:
                                disponibilidad_estudio[dia_cambio] = horas
                                break 
            
                            else:
                                print("Error: Introduce un número entre 0 y 24.")
                                

                        except ValueError:
                            print("Error: Escribe un número válido.")
            
                    guardar_todo() 
                    print("\nDisponibilidad guardada correctamente.")

                else:
                    print("Día no válido. Asegúrate de escribirlo bien (ej: Miércoles).")
                    time.sleep(1.5)
                    cambiar_hora = False

                        

            

        if dis_opcion == "2":
            for dia in dias_semana:
                while True: 
                    horas = int(input(f"¿Cuántas horas tienes para estudiar el {dia.lower()}? "))

                    try:
                        if 0 <= horas <= 24:
                            disponibilidad_estudio[dia] = horas
                            break 
            
                        else:
                            print("Error: Introduce un número entre 0 y 24.")
        
                    except ValueError:
                        print("Error: Escribe un número válido.")

            guardar_todo() 
            print("\nDisponibilidad guardada correctamente.")


    elif accion == "6":
        print("Saliendo...")
        break
     
    else:
        print("Opción no válida.")
        time.sleep(1.5)

