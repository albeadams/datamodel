import pandas as pd
import xlwings as xw
import oracle as oc

def RunQuery():
	wb = xw.Book.caller()
	sht = wb.sheets['Query']
	queryStr = sht.range('C2').value
	oclient = oc.OracleQuery()
	cursor, columns = oclient.get_excel_data(queryStr)
	df = pd.DataFrame(cursor, columns=columns)
	sht.range('C9').value = df
	oclient.remove_cursor(cursor)
	oclient.disconnect()