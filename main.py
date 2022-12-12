from classes.CoordsGrab import CoordsGrab
import tabula as tb
import easygui


def pdf2excel(file, filepages, coord, colunas):
    df = tb.read_pdf(file, pages=filepages, area=coord, columns=colunas, relative_area=True, relative_columns=True, pandas_options={
        'header': None}, output_format="dataframe", stream=True)
    headers = df[0].iloc[0]
    df = df[0][1:]
    df.columns = headers
    print(df)
    df.to_excel('output.xlsx')


filename = easygui.fileopenbox()
pdfpages = [1 + i for i in range(5)]

CoordsObj = CoordsGrab(filename)
dataPoints = CoordsObj.coords
cols = CoordsObj.cols
pageSize = CoordsObj.size

topbound = dataPoints[0][1]/pageSize[1]*100
botbound = dataPoints[1][1]/pageSize[1]*100
leftbound = dataPoints[0][0]/pageSize[0]*100
rightbound = dataPoints[1][0]/pageSize[0]*100

coords = [topbound, leftbound, botbound, rightbound]
cols[:] = [x/pageSize[0]*100 for x in cols]

pdf2excel(filename, pdfpages, coords, cols)
