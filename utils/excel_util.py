from openpyxl import load_workbook


def read_excel(path, sheet=0):
    wb = load_workbook(path)
    ws = wb.worksheets[sheet]
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        raise ValueError(f"Excel 文件 {path} 无数据")
    header = rows[0]
    return [dict(zip(header, r)) for r in rows[1:] if any(v is not None for v in r)]
