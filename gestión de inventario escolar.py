import flet as ft
from datetime import datetime

class InventarioEscolarApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Gestión de Inventario Escolar"
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        # Estado de la aplicación
        self.material_actual = None
        self.lista_materiales = []
        
        self.inicializar_controles()
        self.cargar_datos_iniciales()

    def inicializar_controles(self):
        self.formulario_material = ft.Form(
            fields=[
                ft.FormField(
                    name="nombre",
                    label="Nombre del Material",
                    content=ft.TextField(hint_text="Ej: Marcadores", width=300)
                ),
                ft.FormField(
                    name="cantidad",
                    label="Cantidad",
                    content=ft.TextField(hint_text="0", width=150, text_align=ft.TextAlign.RIGHT)
                ),
                ft.FormField(
                    name="categoria",
                    label="Categoría",
                    content=ft.Dropdown(
                        hint_text="Seleccione categoría",
                        options=[
                            ft.dropdown.Option("Material de Arte"),
                            ft.dropdown.Option("Útiles Escolares"),
                            ft.dropdown.Option("Equipo Digital"),
                            ft.dropdown.Option("Otros")
                        ]
                    )
                ),
                ft.FormField(
                    name="fecha_registro",
                    label="Fecha de Registro",
                    content=ft.TextField(
                        value=datetime.now().strftime("%Y-%m-%d"),
                        readonly=True,
                        width=200
                    )
                )
            ]
        )

        self.grilla_materiales = ft.DataGrid(
            columns=[
                ft.DataGridColumn(name="nombre", header="Material", width=250),
                ft.DataGridColumn(name="cantidad", header="Cantidad", width=100),
                ft.DataGridColumn(name="categoria", header="Categoría", width=200),
                ft.DataGridColumn(name="fecha_registro", header="Fecha", width=150)
            ],
            rows=[],
            column_spacing=20,
            row_height=60
        )

        self.page.controls.append(
            ft.Column(
                expand=True,
                controls=[
                    ft.Text("Nuevo Material", text_align=ft.TextAlign.CENTER, text_size=20),
                    self.formulario_material,
                    ft.ElevatedButton("Guardar", on_click=self.guardar_material),
                    ft.Separator(height=30),
                    ft.Text("Lista de Materiales", text_align=ft.TextAlign.CENTER, text_size=20),
                    self.grilla_materiales,
                    ft.ElevatedButton("Actualizar Lista", on_click=self.actualizar_lista)
                ]
            )
        )

    def guardar_material(self, e):
        material = {
            "nombre": self.formulario_material.fields["nombre"].content.value,
            "cantidad": int(self.formulario_material.fields["cantidad"].content.value),
            "categoria": self.formulario_material.fields["categoria"].content.selected_value,
            "fecha_registro": self.formulario_material.fields["fecha_registro"].content.value
        }
        
        self.lista_materiales.append(material)
        self.actualizar_lista()
        self.limpiar_formulario()

    def actualizar_lista(self, e=None):
        self.grilla_materiales.rows = [
            ft.DataGridRow(cells=[
                ft.DataGridCell(content=ft.Text(m["nombre"])),
                ft.DataGridCell(content=ft.Text(str(m["cantidad"]))),
                ft.DataGridCell(content=ft.Text(m["categoria"])),
                ft.DataGridCell(content=ft.Text(m["fecha_registro"]))
            ])
            for m in sorted(self.lista_materiales, key=lambda x: x["nombre"])
        ]
        self.page.update()

    def limpiar_formulario(self):
        for field in self.formulario_material.fields.values():
            if isinstance(field.content, ft.TextField):
                field.content.value = ""
            elif isinstance(field.content, ft.Dropdown):
                field.content.selected_value = None
        self.formulario_material.fields["fecha_registro"].content.value = \
            datetime.now().strftime("%Y-%m-%d")

def main(page: ft.Page):
    app = InventarioEscolarApp(page)

ft.app(target=main)
