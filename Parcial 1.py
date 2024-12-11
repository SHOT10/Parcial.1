from sqlalchemy import Column, Integer, String, Float, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# Configuración de la base de datos (ajusta según tu configuración)
engine = create_engine('postgresql://usuario:contraseña@localhost/presupuesto')
Session = sessionmaker(bind=engine)

# Función para crear todas las tablas si no existen
def create_tables():
    Base.metadata.create_all(engine)

# Modelo de Gasto
Base = declarative_base()

class Gasto(Base):
    __tablename__ = 'gastos'
    id = Column(Integer, primary_key=True)
    concepto = Column(String(100), nullable=False)
    cantidad = Column(Float, nullable=False)
    fecha = Column(Date, default=datetime.date.today)

# Función para agregar un nuevo gasto
def agregar_gasto():
    concepto = input("Concepto del gasto: ")
    cantidad = float(input("Cantidad: "))
    nuevo_gasto = Gasto(concepto=concepto, cantidad=cantidad)
    session = Session()
    session.add(nuevo_gasto)
    session.commit()
    session.close()
    print("Gasto agregado correctamente.")

# Función para buscar gastos
def buscar_gastos():
    busqueda = input("Buscar por concepto (parte del texto): ")
    session = Session()
    resultados = session.query(Gasto).filter(Gasto.concepto.like(f"%{busqueda}%")).all()
    if resultados:
        for gasto in resultados:
            print(f"ID: {gasto.id}, Concepto: {gasto.concepto}, Cantidad: {gasto.cantidad}, Fecha: {gasto.fecha}")
    else:
        print("No se encontraron gastos.")
    session.close()

# Función para editar un gasto
def editar_gasto():
    id_gasto = int(input("Ingrese el ID del gasto a editar: "))
    session = Session()
    gasto = session.query(Gasto).get(id_gasto)
    if gasto:
        nuevo_concepto = input("Nuevo concepto (deje en blanco para no cambiar): ")
        nueva_cantidad = input("Nueva cantidad (deje en blanco para no cambiar): ")
        if nuevo_concepto:
            gasto.concepto = nuevo_concepto
        if nueva_cantidad:
            gasto.cantidad = float(nueva_cantidad)
        session.commit()
        print("Gasto editado correctamente.")
    else:
        print("Gasto no encontrado.")
    session.close()

# Función para eliminar un gasto
def eliminar_gasto():
    id_gasto = int(input("Ingrese el ID del gasto a eliminar: "))
    session = Session()
    gasto = session.query(Gasto).get(id_gasto)
    if gasto:
        session.delete(gasto)
        session.commit()
        print("Gasto eliminado correctamente.")
    else:
        print("Gasto no encontrado.")
    session.close()

# Menú principal
def menu():
    create_tables()
    while True:
        print("\nMenú de gestión de presupuesto")
        print("1. Agregar gasto")
        print("2. Buscar gastos")
        print("3. Editar gasto")
        print("4. Eliminar gasto")
        print("0. Salir")
        opcion = input("Selecciona una opción: ")
        if opcion == '1':
            agregar_gasto()
        elif opcion == '2':
            buscar_gastos()
        elif opcion == '3':
            editar_gasto()
        elif opcion == '4':
            eliminar_gasto()
        elif opcion == '0':
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()