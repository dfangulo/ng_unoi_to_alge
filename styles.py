from openpyxl import Workbook
from openpyxl.styles import NamedStyle, Font, Border, Side, Alignment

# Definir estilo predeterminado
default_style = NamedStyle(name="default")
default_style.font = Font(name='Calibri', size=11)
border = Border(left=Side(border_style='thin'), 
                right=Side(border_style='thin'), 
                top=Side(border_style='thin'), 
                bottom=Side(border_style='thin'))
default_style.border = border
default_style.alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)


# Crear libro de trabajo y establecer estilo predeterminado
wb = Workbook()
wb.add_named_style(default_style)
ws = wb.active