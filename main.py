import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import random

from conexion_conocimientos import (
    obtener_todas_las_motos,
    buscar_por_marca,
    buscar_por_estilo,
    buscar_por_precio,
    buscar_por_cilindrada,
    buscar_por_modelo,
    buscar_por_anio,
    agregar_moto,
    eliminar_moto,
    actualizar_moto,
    recomendar_moto_datos
)


class ConcesionariaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Experto - Concesionaria de Motocicletas")
        self.root.geometry("1200x800")
        self.root.configure(bg="#111827")
        self.imagen_actual = None

        self.crear_interfaz()
        self.mostrar_motos(obtener_todas_las_motos())

    def crear_interfaz(self):
        titulo = tk.Label(
            self.root,
            text="Catalogo de Motocicletas",
            font=("Segoe UI", 24, "bold"),
            bg="#111827",
            fg="white"
        )
        titulo.pack(pady=15)

        contenedor = tk.Frame(self.root, bg="#111827")
        contenedor.pack(fill="both", expand=True, padx=20, pady=10)

        panel_izquierdo = tk.Frame(contenedor, bg="#1f2937", width=300)
        panel_izquierdo.pack(side="left", fill="y", padx=(0, 15))
        panel_izquierdo.pack_propagate(False)

        panel_derecho = tk.Frame(contenedor, bg="#111827")
        panel_derecho.pack(side="right", fill="both", expand=True)

        tk.Label(
            panel_izquierdo,
            text="Tipo de búsqueda",
            font=("Segoe UI", 10, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(padx=20, pady=(10, 2), anchor="w")

        self.tipo_busqueda = ttk.Combobox(
            panel_izquierdo,
            values=[
                "Todas las motos",
                "Buscar por marca",
                "Buscar por estilo",
                "Buscar por precio",
                "Buscar por cilindrada",
                "Buscar por modelo",
                "Buscar por año"
            ],
            state="readonly",
            font=("Segoe UI", 11)
        )
        self.tipo_busqueda.current(0)
        self.tipo_busqueda.pack(padx=20, pady=10, fill="x")
        self.tipo_busqueda.bind("<<ComboboxSelected>>", self.actualizar_campos_busqueda)

        self.entrada_1 = tk.Entry(panel_izquierdo, font=("Segoe UI", 11))
        self.entrada_2 = tk.Entry(panel_izquierdo, font=("Segoe UI", 11))

        self.btn_buscar = tk.Button(
            panel_izquierdo,
            text="Buscar",
            font=("Segoe UI", 12, "bold"),
            bg="#2563eb",
            fg="white",
            relief="flat",
            command=self.buscar
        )
        self.btn_buscar.pack(padx=20, pady=15, fill="x")

        tk.Button(
            panel_izquierdo,
            text="Mostrar todas",
            font=("Segoe UI", 12, "bold"),
            bg="#10b981",
            fg="white",
            relief="flat",
            command=lambda: self.mostrar_motos(obtener_todas_las_motos())
        ).pack(padx=20, pady=5, fill="x")

        tk.Label(
            panel_izquierdo,
            text="Gestión de motos",
            font=("Segoe UI", 15, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(pady=20)

        tk.Button(
            panel_izquierdo,
            text="Agregar moto",
            bg="#16a34a",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            command=self.ventana_agregar
        ).pack(padx=20, pady=8, fill="x")

        tk.Button(
            panel_izquierdo,
            text="Recomendacion inteligente",
            bg="#7c3aed",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            command=self.ventana_recomendacion
        ).pack(padx=20, pady=8, fill="x")

        columnas = ("Marca", "Modelo", "Estilo", "Cilindrada", "Precio", "Año")

        self.tabla = ttk.Treeview(
            panel_derecho,
            columns=columnas,
            show="headings",
            height=15
        )

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=120)

        self.tabla.pack(fill="both", expand=True)

        panel_botones_tabla = tk.Frame(panel_derecho, bg="#111827")
        panel_botones_tabla.pack(fill="x", pady=10)

        tk.Button(
            panel_botones_tabla,
            text="Editar seleccionado",
            bg="#f59e0b",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            command=self.editar_seleccionado
        ).pack(side="left", padx=5, ipadx=20, ipady=5)

        tk.Button(
            panel_botones_tabla,
            text="Eliminar seleccionado",
            bg="#dc2626",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            command=self.eliminar_seleccionado
        ).pack(side="left", padx=5, ipadx=20, ipady=5)

        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_moto)

        self.panel_imagen = tk.Label(
            panel_derecho,
            text="Imagen de la motocicleta",
            bg="#1f2937",
            fg="white",
            font=("Segoe UI", 14)
        )
        self.panel_imagen.pack(fill="x", pady=15, ipady=40)

        self.actualizar_campos_busqueda()

    def actualizar_campos_busqueda(self, event=None):
        tipo = self.tipo_busqueda.get()

        self.entrada_1.pack_forget()
        self.entrada_2.pack_forget()

        self.entrada_1.delete(0, tk.END)
        self.entrada_2.delete(0, tk.END)

        if tipo in ["Buscar por marca", "Buscar por estilo", "Buscar por modelo", "Buscar por año"]:
            self.entrada_1.pack(padx=20, pady=8, fill="x", before=self.btn_buscar)

            ejemplos = {
                "Buscar por marca": "Ejemplo: honda",
                "Buscar por estilo": "Ejemplo: naked",
                "Buscar por modelo": "Ejemplo: cb150",
                "Buscar por año": "Ejemplo: 2023"
            }

            self.entrada_1.insert(0, ejemplos[tipo])

        elif tipo in ["Buscar por precio", "Buscar por cilindrada"]:
            self.entrada_1.pack(padx=20, pady=8, fill="x", before=self.btn_buscar)
            self.entrada_2.pack(padx=20, pady=8, fill="x", before=self.btn_buscar)

            self.entrada_1.insert(0, "Mínimo")
            self.entrada_2.insert(0, "Máximo")

    def buscar(self):
        tipo = self.tipo_busqueda.get()
        valor1 = self.entrada_1.get().strip().lower()
        valor2 = self.entrada_2.get().strip().lower()

        try:
            if tipo == "Todas las motos":
                resultados = obtener_todas_las_motos()

            elif tipo == "Buscar por marca":
                resultados = buscar_por_marca(valor1)

            elif tipo == "Buscar por estilo":
                resultados = buscar_por_estilo(valor1)

            elif tipo == "Buscar por modelo":
                resultados = buscar_por_modelo(valor1)

            elif tipo == "Buscar por año":
                resultados = buscar_por_anio(int(valor1))

            elif tipo == "Buscar por precio":
                resultados = buscar_por_precio(int(valor1), int(valor2))

            elif tipo == "Buscar por cilindrada":
                resultados = buscar_por_cilindrada(int(valor1), int(valor2))

            else:
                resultados = []

            self.mostrar_motos(resultados)

        except Exception as e:
            messagebox.showerror("Error en búsqueda", f"Verifica los datos ingresados.\n\nError: {e}")

    def mostrar_motos(self, resultados):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        if not resultados:
            messagebox.showinfo("Sin resultados", "No se encontraron motocicletas.")
            return

        for moto in resultados:
            marca = str(moto.get("Marca", ""))
            modelo = str(moto.get("Modelo", ""))
            estilo = str(moto.get("Estilo", ""))
            cilindrada = str(moto.get("Cilindrada", ""))
            precio = str(moto.get("Precio", ""))
            anio = str(moto.get("Anio", ""))

            self.tabla.insert(
                "",
                "end",
                values=(
                    marca.upper(),
                    modelo.upper(),
                    estilo,
                    cilindrada,
                    f"${precio}",
                    anio
                )
            )


    def seleccionar_moto(self, event):
        seleccionado = self.tabla.focus()

        if not seleccionado:
            return

        datos = self.tabla.item(seleccionado, "values")

        if not datos:
            return

        marca = datos[0].lower()
        modelo = datos[1].lower()

        self.mostrar_imagen(marca, modelo)

    def mostrar_imagen(self, marca, modelo):
        ruta = f"imagenes/{marca}_{modelo}.jpg"

        if not os.path.exists(ruta):
            self.panel_imagen.config(
                image="",
                text=f"No hay imagen para {marca.upper()} {modelo.upper()}"
            )
            return

        imagen = Image.open(ruta)
        imagen = imagen.resize((420, 240))
        self.imagen_actual = ImageTk.PhotoImage(imagen)

        self.panel_imagen.config(image=self.imagen_actual, text="")

    def crear_formulario_moto(self, ventana, datos=None):
        campos = {}

        for campo in ["Marca", "Modelo", "Estilo", "Cilindrada", "Precio", "Año"]:
            tk.Label(
                ventana,
                text=campo,
                bg="#1f2937",
                fg="white",
                font=("Segoe UI", 10, "bold")
            ).pack(padx=20, pady=(8, 2), anchor="w")

            entrada = tk.Entry(ventana, font=("Segoe UI", 11))
            entrada.pack(padx=20, pady=2, fill="x")

            if datos:
                valores = {
                    "Marca": datos[0],
                    "Modelo": datos[1],
                    "Estilo": datos[2],
                    "Cilindrada": datos[3],
                    "Precio": str(datos[4]).replace("$", ""),
                    "Año": datos[5]
                }

                entrada.insert(0, valores[campo])

            campos[campo] = entrada

        return campos

    def ventana_agregar(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Agregar motocicleta")
        ventana.geometry("380x500")
        ventana.configure(bg="#1f2937")
        ventana.resizable(False, False)

        tk.Label(
            ventana,
            text="Agregar motocicleta",
            bg="#1f2937",
            fg="white",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=15)

        campos = self.crear_formulario_moto(ventana)

        def guardar():
            try:
                agregar_moto(
                    campos["Marca"].get().strip().lower(),
                    campos["Modelo"].get().strip().lower(),
                    campos["Estilo"].get().strip().lower(),
                    int(campos["Cilindrada"].get().strip()),
                    int(campos["Precio"].get().strip()),
                    int(campos["Año"].get().strip())
                )

                self.mostrar_motos(obtener_todas_las_motos())
                ventana.destroy()
                messagebox.showinfo("Éxito", "Motocicleta agregada correctamente.")

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar la moto:\n{e}")

        tk.Button(
            ventana,
            text="Guardar",
            bg="#16a34a",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            command=guardar
        ).pack(padx=20, pady=20, fill="x")

    def ventana_actualizar(self, datos):
        ventana = tk.Toplevel(self.root)
        ventana.title("Actualizar motocicleta")
        ventana.geometry("380x500")
        ventana.configure(bg="#1f2937")
        ventana.resizable(False, False)

        tk.Label(
            ventana,
            text="Actualizar motocicleta",
            bg="#1f2937",
            fg="white",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=15)

        campos = self.crear_formulario_moto(ventana, datos)

        campos["Marca"].config(state="disabled")
        campos["Modelo"].config(state="disabled")

        def guardar():
            try:
                actualizar_moto(
                    datos[0].lower(),
                    datos[1].lower(),
                    campos["Estilo"].get().strip().lower(),
                    int(campos["Cilindrada"].get().strip()),
                    int(campos["Precio"].get().strip()),
                    int(campos["Año"].get().strip())
                )

                self.mostrar_motos(obtener_todas_las_motos())
                ventana.destroy()
                messagebox.showinfo("Éxito", "Motocicleta actualizada correctamente.")

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar la moto:\n{e}")

        tk.Button(
            ventana,
            text="Guardar cambios",
            bg="#f59e0b",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            command=guardar
        ).pack(padx=20, pady=20, fill="x")
        
    def obtener_moto_seleccionada(self):
            seleccionado = self.tabla.focus()

            if not seleccionado:
                messagebox.showwarning("Sin selección", "Selecciona una motocicleta de la tabla.")
                return None

            datos = self.tabla.item(seleccionado, "values")

            if not datos:
                messagebox.showwarning("Sin selección", "Selecciona una motocicleta válida.")
                return None

            return datos

    def editar_seleccionado(self):
            datos = self.obtener_moto_seleccionada()

            if datos:
                self.ventana_actualizar(datos)

    def eliminar_seleccionado(self):
            datos = self.obtener_moto_seleccionada()

            if not datos:
                return

            confirmar = messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Seguro que deseas eliminar {datos[0]} {datos[1]}?"
            )

            if confirmar:
                eliminar_moto(datos[0].lower(), datos[1].lower())
                self.mostrar_motos(obtener_todas_las_motos())
                messagebox.showinfo("Éxito", "Motocicleta eliminada correctamente.")
    
    
    def ventana_recomendacion(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Recomendación inteligente")
        ventana.geometry("900x650")
        ventana.configure(bg="#1f2937")
        ventana.resizable(False, False)

        imagen_recomendada = {"img": None}

        tk.Label(
            ventana,
            text="Recomendación inteligente",
            bg="#1f2937",
            fg="white",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=15)

        tk.Label(
            ventana,
            text="Uso principal",
            bg="#1f2937",
            fg="white",
            font=("Segoe UI", 10, "bold")
        ).pack(padx=20, pady=(8, 2), anchor="w")

        uso = ttk.Combobox(
            ventana,
            values=["ciudad", "trabajo", "carretera", "terraceria", "deportivo"],
            state="readonly",
            font=("Segoe UI", 11)
        )
        uso.current(0)
        uso.pack(padx=20, pady=5, fill="x")

        tk.Label(
            ventana,
            text="Presupuesto máximo",
            bg="#1f2937",
            fg="white",
            font=("Segoe UI", 10, "bold")
        ).pack(padx=20, pady=(8, 2), anchor="w")

        presupuesto = tk.Entry(ventana, font=("Segoe UI", 11))
        presupuesto.pack(padx=20, pady=5, fill="x")
        presupuesto.insert(0, "50000")

        tk.Label(
            ventana,
            text="Experiencia",
            bg="#1f2937",
            fg="white",
            font=("Segoe UI", 10, "bold")
        ).pack(padx=20, pady=(8, 2), anchor="w")

        experiencia = ttk.Combobox(
            ventana,
            values=["principiante", "intermedio", "avanzado"],
            state="readonly",
            font=("Segoe UI", 11)
        )
        experiencia.current(0)
        experiencia.pack(padx=20, pady=5, fill="x")

        def recomendar():
            try:
                uso_valor = uso.get().strip().lower()
                presupuesto_valor = int(presupuesto.get().strip())
                experiencia_valor = experiencia.get().strip().lower()

                recomendaciones = recomendar_moto_datos(
                    uso_valor,
                    presupuesto_valor,
                    experiencia_valor
                )

                if not recomendaciones:
                    resultado.config(
                        text="No se encontró una motocicleta que coincida con tus respuestas."
                    )
                    panel_img.config(image="", text="Sin imagen")
                    return

                moto = random.choice(recomendaciones)

                marca = str(moto["Marca"])
                modelo = str(moto["Modelo"])
                estilo = str(moto["Estilo"])
                cilindrada = str(moto["Cilindrada"])
                precio = str(moto["Precio"])
                anio = str(moto["Anio"])

                texto = (
                    f"Moto recomendada:\n\n"
                    f"Marca: {marca.upper()}\n"
                    f"Modelo: {modelo.upper()}\n"
                    f"Estilo: {estilo}\n"
                    f"Cilindrada: {cilindrada} cc\n"
                    f"Precio: ${precio}\n"
                    f"Año: {anio}\n\n"
                    f"Motivo: Esta moto se recomienda para uso {uso_valor}, "
                    f"es adecuada para un conductor {experiencia_valor} "
                    f"y se encuentra dentro del presupuesto indicado."
                )

                resultado.config(text=texto)

                ruta = f"imagenes/{marca.lower()}_{modelo.lower()}.jpg"

                if os.path.exists(ruta):
                    img = Image.open(ruta)
                    img = img.resize((360, 260))
                    imagen_recomendada["img"] = ImageTk.PhotoImage(img)
                    panel_img.config(image=imagen_recomendada["img"], text="")
                else:
                    panel_img.config(
                        image="",
                        text=f"No hay imagen para {marca.upper()} {modelo.upper()}"
                    )

            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"No se pudo generar la recomendación:\n{e}"
                )

        tk.Button(
            ventana,
            text="Recomendar",
            bg="#7c3aed",
            fg="white",
            font=("Segoe UI", 12, "bold"),
            relief="flat",
            command=recomendar
        ).pack(padx=20, pady=15, fill="x")

        contenedor_resultado = tk.Frame(ventana, bg="#1f2937")
        contenedor_resultado.pack(padx=20, pady=20, fill="both", expand=True)

        resultado = tk.Label(
            contenedor_resultado,
            text="Completa el formulario y presiona Recomendar.",
            bg="#111827",
            fg="white",
            font=("Segoe UI", 11),
            justify="left",
            wraplength=380
        )
        resultado.pack(side="left", fill="both", expand=True, padx=(0, 10))

        panel_img = tk.Label(
            contenedor_resultado,
            text="Imagen de la recomendación",
            bg="#111827",
            fg="white",
            font=("Segoe UI", 11)
        )
        panel_img.pack(side="right", fill="both", expand=True, padx=(10, 0))

        

        

if __name__ == "__main__":
    root = tk.Tk()
    app = ConcesionariaApp(root)
    root.mainloop()