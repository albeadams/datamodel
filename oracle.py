import cx_Oracle as oracle
import dataconfig as datafig

class OracleQuery(object):

	def __init__(self):
		self.connection = oracle.connect(datafig.data['username'], datafig.data['password'], datafig.data['client'])

	def disconnect(self):
		self.connection.close()

	def get_cursor(self):
		return self.connection.cursor()

	def remove_cursor(self,cursor):
		cursor.close()

	def get_table_columns(self, table):
		cursor = self.get_cursor()
		cursor.execute(datafig.query['get_table_columns'].format(table))
		for eachrow in cursor.description:
			print('  ' + eachrow[0])
		while True:
			seecol = input('\nOptions:\n\tsample    >>> show sample\n\t<column>  >>> show specific column\n\ttable     >>> show table again\n\tdetail    >>> show detailed table\n\tmenu      >>> return to main\n\nEnter: ')
			seecol.lower()
			if seecol == 'menu':
				break
			elif seecol == 'table':
				for eachrow in cursor.description:
					print('  ' + eachrow[0])
			elif seecol == 'detailed':
				for eachrow in cursor.description:
					print('  ' + eachrow[0])
					print('    ' + '(type: ' + str(eachrow[1]).split('.')[1].split('\'')[0] + '; ' + 'maxsize: ' + str(eachrow[3]) + ''.join(['; ','nullable: ','True)' if str(eachrow[4]) == 'None' else 'Must contain value)']))
					print()
			else:
				sortcol = cursor.description[0][0]
				#cursor.execute(datafig.query['get_table_sample'].format(table, sortcol, sortcol))
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
							lines = cursor.fetchmany(numRows=5)
							for line in lines:
								if count < 5 and line[index]:
									count += 1
									print(line[index])
								else:
									break
					if not found:
						print('\n\t***Check spelling and try again***\n')

		self.remove_cursor(cursor)