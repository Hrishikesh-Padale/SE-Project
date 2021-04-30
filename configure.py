def read_settings():
	try:
		file = open("game.ini","r+")
		settings = {}
		for each in file:
			i = each.split(":")
			i = [j.strip() for j in i]
			if bool(i[0]):
				settings[i[0]]=i[1]
		#print(settings)
		file.close()
		return settings
	except:
		print("File does not exist!")
		return


def update_settings(**kwargs):
	try:
		file = open("game.ini","r+")

		settings = {}
		for each in file:
			i = each.split(":")
			i = [j.strip() for j in i]
			if bool(i[0]):
				settings[i[0]]=i[1]

		if 'UserID' in kwargs and kwargs['UserID']:
			settings['UserID'] = kwargs['UserID']
			settings['Password'] = kwargs['Password']
			settings['Remember Credentials'] = 'True'

			file.seek(0)
			for i in settings:
				file.write("\n{}:{}".format(i,settings[i]))
			file.truncate()

		else:
			settings['UserID'] = ''
			settings['Password'] = ''
			settings['Remember Credentials'] = 'False'

		if 'music' in kwargs:
			settings['Music'] = kwargs['music']
			settings['Piece Appearance'] = kwargs['ptype']
			settings['Board Theme'] = kwargs['ctype']
			settings['Volume'] = kwargs['volume']

			file.seek(0)
			for i in settings:
				file.write("\n{}:{}".format(i,settings[i]))
			file.truncate()

		

		

		file.close()
		read_settings()

	except:
		print("\nConf file does not exist\nCreating game.ini...")
		try:
			print("game.ini created successfully!")
			file = open("game.ini","w")
			file.write("\nUserID:")
			file.write("\nPassword:")
			file.write("\nMusic:ON")
			file.write("\nPiece Appearance:3")
			file.write("\nBoard Theme:2")
			file.write("\nVolume:50")
			file.write("\nRemember Credentials:False")
			file.close()
		except:
			print("Error in creating game.conf!")
			return
	return
