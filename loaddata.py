from openpyxl import load_workbook

def loadData(filename="data/cover_day_delnull.xlsx"):
    xlsx_file_reader = load_workbook(filename=filename)
    sht=xlsx_file_reader.worksheets[0]
    datalist=[]
    for row in sht.rows:
        row_container = []
        for cell in row:
            row_container.append(cell.value)
        datalist.append(row_container)
    return datalist[0],datalist[1:]
if __name__ == "__main__":
    res=loadData()
    print(res[0])