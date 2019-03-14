import oracle

class MainMenu(object):

	def __init__(self):
		self.oclient = oracle.OracleQuery()
		self.table_list = 'lookup/table_lookup.txt' 

	def options(self):
		options = ('\nOptions: \n'
			'   choices                >>>  shows table name choices\n'
			'   table <table_name>     >>>  lists columns for specific table\n'
			'   all                    >>>  list all tables\n'
			'   keys <table_name>      >>>  list keys for specific table\n'
			'   relat <table_name>     >>>  lists all relationships for specific table\n'
			'   mod <module_name>      >>>  all tables involved in a module, i.e. sales\n'
			'   exit/quit/cls          >>>  exit program\n\n'
			'  Enter: ')
		return options

	def get_table_columns(self, arg):
		with open(self.table_list, "r") as fp:
			for line in iter(fp.readline, ''):
				if line.split(',')[0] == arg[1]:
					table = line.split(',')[1]
		if table:
			self.oclient.get_table_columns(table)

	def view_table_choices(self, arg):
		#open file, print off first before comma
		with open(self.table_list, "r") as fp:
			for line in iter(fp.readline, ''):
				print('    '+line.split(',')[0])
				

	def query_columns(self):
		return 'columns selected'

	def query_keys(self):
		return 'keys selected'

	def query_relationships(self):
		return 'relationships selected'

	def query_module(self):
		return 'module selected'

	def route(self, args):
		switch = {
			'choices': self.view_table_choices,
			'table': self.get_table_columns,
			'columns': self.query_columns,
			'keys': self.query_keys,
			'relationships': self.query_relationships,
			'module': self.query_module
		}

		if args[0] in switch:
			func = switch.get(args[0], lambda: 'invalid choice')
			func(args)
			if args[0] == 'choices': 
				return True
			else: 
				return False
		else:
			print('\t***Check spelling and try again***')

	def run(self):
		choices = False
		while True:
			if not choices:
				pick = input(self.options())
			else:
				pick = input('\n  Enter: ')
			pick.lower()
			if pick == 'exit' or pick == 'quit' or pick == 'cls':
				self.oclient.disconnect()
				break
			else:
				print()
				args = pick.split(' ')
				choices = self.route(args)