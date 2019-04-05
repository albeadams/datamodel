import pandas as pd
import numpy as np
import xlwings as xw
import oracle as oc
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

def RunQuery():
	wb = xw.Book.caller()
	sht1 = wb.sheets['MakeQuery']
	sht2 = wb.sheets['Query']
	queryStr = sht1.range('B1').value
	oclient = oc.OracleQuery()
	cursor, columns = oclient.get_excel_data(queryStr)
	df = pd.DataFrame(cursor, columns=columns)
	df_indexed = df.set_index(list(df)[0])
	sht2.range('A2').value = df_indexed
	oclient.remove_cursor(cursor)
	oclient.disconnect()

def make_pdf():
	wb = xw.Book.caller()
	sht1 = wb.sheets['Query']
	sht2 = wb.sheets['Graph']
		
	getcoord = 2
	while sht2.cells(getcoord, 2).value:
		if sht2.cells(getcoord, 1).value == 'x':
			x = sht2.cells(getcoord, 2).value
		elif sht2.cells(getcoord, 1).value == 'y':
			y = sht2.cells(getcoord, 2).value
		getcoord += 1

	getcol = 1
	xf = sht1.range('A2').options(pd.DataFrame, expand='table', header=1).value
	while sht1.cells(2, getcol).value:
		if sht1.cells(2, getcol).value == x:
			#xf = sht1.range('B2').options(pd.Series, expand='table').value
			#sht2.range('C1').value = xf
			col1 = xf.iloc[:xf.shape[0]] # get all rows
			col1 = col1[col1.columns[getcol-2]] # get column
		elif sht1.cells(2,getcol).value == y:
			col2 = xf.iloc[:xf.shape[0]] # get all rows
			col2 = col2[col2.columns[getcol-2]] # get column
		getcol +=1

	np.random.seed(19680801)

	N = xf.shape[0]
	x = col1
	y = col2
	colors = np.random.rand(N)
	area = (30 * np.random.rand(N))**2  # 0 to 15 point radii
	
	fig = plt.figure()
	plt.scatter(x, y, s=area, c=colors, alpha=0.5)
	sht2.pictures.add(fig, name='MyPlot', update=True)