import oracle

class MainMenu(object):

	def __init__(self):
		self.oclient = oracle.OracleQuery()
		self.table_list = 'lookup/table_lookup.txt'
		self.options = ('\nOptions: \n\n'
			'   choices                >>>  shows table name choices\n'
			'   <table_name>           >>>  lists columns for specific table\n'
			'   table <table_name>     >>>  alternate way to list table columns\n'
			'   all                    >>>  list all tables\n'
			'   keys <table_name>      >>>  list keys for specific table\n'
			'   relat <table_name>     >>>  lists all relationships for specific table\n'
			'   mod <module_name>      >>>  all tables involved in a module, i.e. sales\n'
			'   exit/quit/cls          >>>  exit program\n\n'
			'  Enter: ') 

	def get_table_columns(self, arg):
		#using table <table_name>
		table = ''
		with open(self.table_list, "r") as fp:
			for line in iter(fp.readline, ''):
				# refactor with contains...
				if line[:2] == '++':
					if line.split(',')[0][2:] == arg[1]:
						table = line.split(',')[1]
				if line[:1] == '+':
					if line.split(',')[0][1:] == arg[1]:
						table = line.split(',')[1]
		if table:
			self.oclient.get_table_columns(table)
			return True
		else:
			return False

	def get_table_single(self, arg):
		#using only <table_name>
		table = ''
		with open(self.table_list, "r") as fp:
			for line in iter(fp.readline, ''):
				# refactor with contains...
				if line[:2] == '++':
					if line.split(',')[0][2:] == arg[0]:
						table = line.split(',')[1]
				if line[:1] == '+':
					if line.split(',')[0][1:] == arg[0]:
						table = line.split(',')[1]
		if table:
			self.oclient.get_table_columns(table)
			return True
		else:
			return False

	def view_table_choices(self, arg):
		#open file, print off first before comma
		with open(self.table_list, "r") as fp:
			for line in iter(fp.readline, ''):
				if line[:2] == '++':
					print('    '+line.split(',')[0][2:]+'   [fact]')
				elif line[:1] == '+':
					print('    '+line.split(',')[0][1:])
		return True

	def get_modules(self, arg):
		if arg[1] == 'sales' or arg[1] == 'inventory':
			mod = (input('enter ''"monthly"'', ''"daily"'', or ''"transaction"'': ')).lower()
			mod = (arg[1]+'_'+mod)
		else:
			mod = arg[1]
		with open(self.table_list, "r") as fp:
			flag = False
			for line in iter(fp.readline, ''):
				if not flag and line[:2] == '++' and line.split(',')[0][2:] == mod:
					# found related table for module
					flag = True
					print('  related tables:')
				elif flag and line[1:2] == '-':
					key1 = line.split('[')[1][:-1]
					key2 = line.split('[')[2][:-2]
					print('\t'+line[2:].split('[')[0]+'  '+''.join(['shared key = ' + key1 if key2 =='*' else 'keys = ' + key1 + ', ' + key2]))
				else:
					flag = False
		return True

	def query_columns(self):
		return 'columns selected'

	def query_keys(self):
		return 'keys selected'

	def query_relationships(self):
		return 'relationships selected'


 
	def route(self, args):
		switch = {
			'choices': self.view_table_choices,
			'mod': self.get_modules,
			'table': self.get_table_columns,
			'single': self.get_table_single,
			'columns': self.query_columns,
			'keys': self.query_keys,
			'relationships': self.query_relationships,
		}

		if args[0] in switch:
			func = switch.get(args[0], lambda: 'invalid choice')
			hastable = func(args)
			if not hastable:
				print('\t***Check spelling and try again***')
			if args[0] == 'choices': 
				return True
			else: 
				return False
		else:
			func = switch.get('single', lambda: 'invalid choice')
			hastable = func(args)
			if not hastable:
				print('\t***Check spelling and try again***')


	def run(self):
		choices = False
		while True:
			if not choices:
				pick = input(self.options)
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