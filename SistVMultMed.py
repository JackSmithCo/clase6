import re

class Medicamento:
    def __init__(self):
        self.__nombre = "" 
        self.__dosis = 0 
    
    def verNombre(self):
        return self.__nombre 
    
    def verDosis(self):
        return self.__dosis 
    
    def asignarNombre(self, med):
        self.__nombre = med 
    
    def asignarDosis(self, dosis):
        self.__dosis = dosis 

class Mascota:
    def __init__(self):
        self.__nombre = " "
        self.__historia = 0
        self.__tipo = " "
        self.__peso = " "
        self.__fecha_ingreso = " "
        self.__lista_medicamentos = []
        
    def verNombre(self):
        return self.__nombre
    def verHistoria(self):
        return self.__historia
    def verTipo(self):
        return self.__tipo
    def verPeso(self):
        return self.__peso
    def verFecha(self):
        return self.__fecha_ingreso
    def verLista_Medicamentos(self):
        return self.__lista_medicamentos 
    
    def asignarNombre(self, n):
        self.__nombre = n
    def asignarHistoria(self, nh):
        self.__historia = nh
    def asignarTipo(self, t):
        self.__tipo = t.lower()
    def asignarPeso(self, p):
        self.__peso = p
    def asignarFecha(self, f):
        self.__fecha_ingreso = f
    def asignarLista_Medicamentos(self, lista):
        self.__lista_medicamentos = lista
    
    def eliminarMedicamento(self, nombre_medicamento):
        for m in self.__lista_medicamentos:
            if m.verNombre().lower() == nombre_medicamento.lower():
                self.__lista_medicamentos.remove(m)
                return True
        return False

class sistemaV:
    def __init__(self):
        self.caninos = {}
        self.felinos = {}
    
    def verificarExiste(self, historia):
        return historia in self.caninos or historia in self.felinos
        
    def verNumeroMascotas(self):
        return len(self.caninos) + len(self.felinos)
    
    def ingresarMascota(self, mascota):
        if mascota.verTipo() == "canino":
            self.caninos[mascota.verHistoria()] = mascota
        elif mascota.verTipo() == "felino":
            self.felinos[mascota.verHistoria()] = mascota

    def __buscarMascota(self, historia):
        if historia in self.caninos:
            return self.caninos[historia]
        elif historia in self.felinos:
            return self.felinos[historia]
        return None

    def verFechaIngreso(self, historia):
        mascota = self.__buscarMascota(historia)
        return mascota.verFecha() if mascota else None

    def verMedicamento(self, historia):
        mascota = self.__buscarMascota(historia)
        return mascota.verLista_Medicamentos() if mascota else None

    def eliminarMascota(self, historia):
        if historia in self.caninos:
            del self.caninos[historia]
            return True
        elif historia in self.felinos:
            del self.felinos[historia]
            return True
        return False

    def eliminarMedicamento(self, historia, nombre_medicamento):
        mascota = self.__buscarMascota(historia)
        if mascota:
            return mascota.eliminarMedicamento(nombre_medicamento)
        return False

def validar_fecha(fecha):
    return re.match(r"^\d{2}/\d{2}/\d{4}$", fecha)

def main():
    servicio_hospitalario = sistemaV()
    
    while True:
        try:
            menu = int(input('''\nIngrese una opción: 
1- Ingresar una mascota 
2- Ver fecha de ingreso 
3- Ver número de mascotas en el servicio 
4- Ver medicamentos que se están administrando
5- Eliminar mascota 
6- Eliminar un medicamento de una mascota
7- Salir 
Usted ingresó la opción: '''))
        except ValueError:
            print("Por favor, ingrese un número válido.")
            continue

        if menu == 1:
            if servicio_hospitalario.verNumeroMascotas() >= 10:
                print("No hay espacio ...") 
                continue

            try:
                historia = int(input("Ingrese la historia clínica de la mascota: "))
            except ValueError:
                print("Historia clínica inválida.")
                continue

            if not servicio_hospitalario.verificarExiste(historia):
                nombre = input("Ingrese el nombre de la mascota: ")
                tipo = input("Ingrese el tipo de mascota (felino o canino): ")

                if tipo not in ['canino', 'felino']:
                    print("Tipo inválido. Solo se permiten 'canino' o 'felino'.")
                    continue

                try:
                    peso = float(input("Ingrese el peso de la mascota: "))
                except ValueError:
                    print("Peso inválido.")
                    continue

                fecha = input("Ingrese la fecha de ingreso (dd/mm/aaaa): ")
                if not validar_fecha(fecha):
                    print("Fecha inválida. Use el formato dd/mm/aaaa.")
                    continue

                try:
                    nm = int(input("Ingrese cantidad de medicamentos: "))
                except ValueError:
                    print("Cantidad inválida.")
                    continue

                lista_med = []
                nombres_existentes = set()

                for _ in range(nm):
                    nombre_med = input("Ingrese el nombre del medicamento: ").strip()
                    if nombre_med.lower() in nombres_existentes:
                        print("Este medicamento ya fue ingresado para esta mascota. Intente con otro.")
                        continue
                    try:
                        dosis = int(input("Ingrese la dosis: "))
                    except ValueError:
                        print("Dosis inválida.")
                        continue
                    med = Medicamento()
                    med.asignarNombre(nombre_med)
                    med.asignarDosis(dosis)
                    lista_med.append(med)
                    nombres_existentes.add(nombre_med.lower())

                mas = Mascota()
                mas.asignarNombre(nombre)
                mas.asignarHistoria(historia)
                mas.asignarTipo(tipo)
                mas.asignarPeso(peso)
                mas.asignarFecha(fecha)
                mas.asignarLista_Medicamentos(lista_med)

                servicio_hospitalario.ingresarMascota(mas)

            else:
                print("Ya existe una mascota con ese número de historia clínica.")

        elif menu == 2:
            historia = int(input("Ingrese la historia clínica de la mascota: "))
            fecha = servicio_hospitalario.verFechaIngreso(historia)
            print(f"La fecha de ingreso es: {fecha}" if fecha else "No se encontró la mascota.")

        elif menu == 3:
            print(f"El número de mascotas en el sistema es: {servicio_hospitalario.verNumeroMascotas()}")

        elif menu == 4:
            historia = int(input("Ingrese la historia clínica de la mascota: "))
            medicamentos = servicio_hospitalario.verMedicamento(historia)
            if medicamentos:
                print("Los medicamentos suministrados son:")
                for m in medicamentos:
                    print(f" - {m.verNombre()} (Dosis: {m.verDosis()})")
            else:
                print("No se encontró la mascota.")

        elif menu == 5:
            historia = int(input("Ingrese la historia clínica de la mascota: "))
            if servicio_hospitalario.eliminarMascota(historia):
                print("Mascota eliminada con éxito.")
            else:
                print("No se encontró la mascota.")

        elif menu == 6:
            historia = int(input("Ingrese la historia clínica de la mascota: "))
            nombre_med = input("Ingrese el nombre del medicamento a eliminar: ")
            if servicio_hospitalario.eliminarMedicamento(historia, nombre_med):
                print("Medicamento eliminado con éxito.")
            else:
                print("No se encontró el medicamento o la mascota.")

        elif menu == 7:
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida. Intente nuevamente.")

if __name__ == '__main__':
    main()





            

                

