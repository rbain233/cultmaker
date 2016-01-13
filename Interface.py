
class Interface:
	"""Takes an dictionary of options, displays them numbered 1 to X.
	If cancelflag, also displays 0: cancel
	Prompt for reply, loop on nonvalid replies.

	BUG: Numbermenu bugs out if there's only one option if written like:
	recruit_method = numbermenu("How will you recruit?", ((1,"Street Preaching")), 
	I think the ((X,Y)) is getting simplified to (X,Y), not ((X,Y),).
	So do it as [(1,"")], which works. """
	def numbermenu(self, prompt, options_dict, cancelflag = 0):
		reply = ''
		menutext = prompt + "\n"
		valid_options = []
		reply_list = []
		ii = 1
		reply_list.append("cancel") #have it on the list whether it's valid or not, to avoid off-by-one error.
		for line in options_dict:
			if isinstance(line, tuple):  #if a line is a (a,b), the first one is the code to return, second is text to display.
				reply_list.append(line[0])
				menutext += str(ii) + ": " + line[1] + "\n"
			else: #if it's a single string, use that for display and return.'
				reply_list.append(line)
				menutext += str(ii) + ": " + line + "\n"            
			valid_options.append(ii)
			ii = ii + 1
		if cancelflag != 0:
			menutext += "0: Cancel\n"
			valid_options.append(0)
		#print str(reply_list) #debug
		#print str(valid_options) #debug
		while reply not in valid_options:
			print menutext
			raw_reply = raw_input("> ")
			if raw_reply.isdigit():
				reply = int(raw_reply)
		else:
			return reply_list[reply]


	def numberPrompt(self, prompt_text, min_num, max_num):
		print prompt_text + " (" + str(min_num) + " - " + str(max_num) + ")"
		while True:
			raw_reply = raw_input()
			if (raw_reply.isdigit()):
				raw_reply = int(raw_reply)
				if (raw_reply >= min_num and raw_reply <= max_num):
					return raw_reply

	"""Takes a list of options.
	Options consist of a key to hit (If zero, one will be assigned),
	A code to return,
	and a desc to be displayed
	Also, a prompt to show the user, and whetehr or not 'cancel' is an option."""
	def letterandnumbermenu(self, prompt, options_list, cancelflag):
		pass
	#r = numbermenu("Pick a number, one to three.", (("a","one"), ("b","two") , ("c","three")), 1)
	#print "You chose ", r
	#r = numbermenu("Pick a number, one to three.", ("one", "two", "three"), 1)
	#print "You chose ", r
