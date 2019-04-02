import cx_Oracle as oracle
import dataconfig

class OracleQuery(object):

	def __init__(self):
		self.connection = oracle.connect(dataconfig.data['username'], dataconfig.data['password'], dataconfig.data['client'])
		self.options = ('\n\tOptions: \n\n'
			'\t-------\n'
			'\t   sample     >>>  show sample\n'
			'\t   <column>   >>>  show specific column\n'
			'\t   table      >>>  show table again\n'
			'\t   detail     >>>  show detailed table\n'
			'\t   menu       >>>  return to main\n\n'
			'\t  Enter: ') 

	def disconnect(self):
		self.connection.close()

	def get_cursor(self):
		return self.connection.cursor()

	def remove_cursor(self,cursor):
		cursor.close()

	#get data for excel
	def get_excel_data(self, query):
		cursor = self.get_cursor()
		cursor.execute(query)
		table_dict = {}
		for eachrow in cursor.description:
			table_dict.setdefault(eachrow[0],[])
		return cursor, table_dict

	def get_table_dict(self, table):
		cursor = self.get_cursor()
		table_dict = {}
		try:
			cursor.execute(dataconfig.query['get_table_columns'].format(table))
			for eachrow in cursor.description:
				table_dict.setdefault(eachrow[0],[])
				table_dict[eachrow[0]].append(str(eachrow[1]).split('.')[1].split('\'')[0])
				table_dict[eachrow[0]].append('Max:' + str(eachrow[3]))
				table_dict[eachrow[0]].append(''.join(['Nullable' if str(eachrow[4]) == 'None' else 'Must contain value)']))
		except Exception:
			table_dict[table] = "not found"
		self.remove_cursor(cursor)
		return table_dict

	def get_table_columns(self, table):
		cursor = self.get_cursor()
		cursor.execute(dataconfig.query['get_table_columns'].format(table))
		for eachrow in cursor.description:
			print('  ' + eachrow[0])
		while True:
			seecol = input(self.options)
			seecol.lower()
			if seecol == 'menu':
				break
			elif seecol == 'table':
				for eachrow in cursor.description:
					print('  ' + eachrow[0])
			elif seecol == 'detail':
				for eachrow in cursor.description:
					print('  ' + eachrow[0])
					print('    ' + '(type: ' + str(eachrow[1]).split('.')[1].split('\'')[0] + '; ' + 'maxsize: ' + str(eachrow[3]) + ''.join(['; ','nullable: ','True)' if str(eachrow[4]) == 'None' else 'Must contain value)']))
					print()
			else:
				sortcol = cursor.description[0][0]
				#cursor.execute(dataconfig.query['get_table_sample'].format(table, sortcol, sortcol))
				if seecol == 'sample':
					print(cursor.fetchone())
					print()
				else:
					found = False
					count = 0
					for index, col in enumerate(cursor.description):
						if seecol == col[0].lower():
							print()
							found = True
							print('  ' + col[0])
							print('    ' + '(type: ' + str(col[1]).split('.')[1].split('\'')[0] + '; ' + 'maxsize: ' + str(col[3]) + ''.join(['; ','nullable: ','True)' if str(col[4]) == 'None' else 'Must contain value)']))
							print()
							print('\t ' + 'First 5 sample:')
							lines = cursor.fetchmany(numRows=5)
							for line in lines:
								if count < 5 and line[index]:
									count += 1
									print('\t  '+line[index])
								else:
									break
					if not found:
						print('\n\t***Check spelling and try again***\n')

		self.remove_cursor(cursor)