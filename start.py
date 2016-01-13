import random
import math
import foo
from person import Person, LaborPool
from cult import Cult

"""Base class for all the "boring stuff" the game does & keeps track of.
Needs to keep track of all game elements."""
class Game:

    def __init__(self):
        #start a new game.
        self.enemies = []  #Cult has no enemies yet.
    
    """Load & save a game's info to/from disk."""
    def load(self):
        pass

    def save(self):
        pass



"""Takes an dictionary of options, displays them numbered 1 to X.
If cancelflag, also displays 0: cancel
Prompt for reply, loop on nonvalid replies.

BUG: Numbermenu bugs out if there's only one option if written like:
recruit_method = numbermenu("How will you recruit?", ((1,"Street Preaching")), 
I think the ((X,Y)) is getting simplified to (X,Y), not ((X,Y),).
So do it as [(1,"")], which works. """
def numbermenu(prompt, options_dict, cancelflag):
    reply = ''
    menutext = prompt + "\n"
    valid_options = []
    reply_list = []
    ii = 1
    if cancelflag != 0:
        menutext += "0: Cancel\n"
        valid_options.append(0)
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
    #print str(reply_list) #debug
    #print str(valid_options) #debug
    while reply not in valid_options:
        print menutext
        raw_reply = raw_input("> ")
        if raw_reply.isdigit():
            reply = int(raw_reply)
    else:
        return reply_list[reply]


def numberPrompt(prompt_text, min_num, max_num):
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
def letterandnumbermenu(prompt, options_list, cancelflag):
    pass
#r = numbermenu("Pick a number, one to three.", (("a","one"), ("b","two") , ("c","three")), 1)
#print "You chose ", r
#r = numbermenu("Pick a number, one to three.", ("one", "two", "three"), 1)
#print "You chose ", r

def monthlyIndoctrination(pool, cult):
    students = cult.getRecruits() + cult.getNoobs()
    """
    if "recruit students" in cult.departments:
        students = cult.departments["recruit students"].people
        if (len(students) < 1):
            #print students
            #print cult.departments["recruit students"]
            return "Error: No students?"
            #DEBUG: This is failing when only one student is assigned.  I need to figure out why.
    else:
        return "Error: How did we end up with teachers but no students?"
    """
    #Runs on teacher
    for teacher in pool.people:
        teaching = (teacher.fanaticism + 25 + (teacher.charisma * 10)) / 2
        ii = 0
        while ii < teaching:
            if len(students) > 1:
                student = random.choice(students)
            else:
                student = students[0]
            if not student.percentCheck(student.fanaticism):
                student.fanaticism += random.randint(1, 6)
            ii += 1
    return str(len(pool.people)) + " indoctrinated " + str(len(students)) + " recruit(s).\n"

print '"In a cult, there is someone at the top who knows the whole thing is a scam.'
print 'In a religion, that person is dead. - Anonymous"'
print
print """You have had a revelation.
Maybe it was contact with the Space Brothers.
Maybe it was a message from Jesus.
Perhaps it was a spontaneous upwelling from the Collective Subconscious.
Maybe it was that there's a lot of gullible people out there with money.
Whatever it was, you have decided to start your own cult!"""
print "So, tell us a bit about yourself."
leader = Person()
leader.name = ''
while len(leader.name) == 0:
    print "What is your name?"
    leader.name = raw_input()

leader.rank = 'leader'
leader.charisma = 2

cult = Cult()
cult.membership = [leader]
cult.fame = 0
cult.popularity = 0
cult.wealth = 1000
cult.doctrine = 10
cult.weirdness = 0
cult.leader = leader

reply = ''
while not reply in ('1','2','3','4','5','6','7','8','9'):
    print "What sort of cult are you starting, %s?" % leader.name
    print "1: Christian"
    print "2: Magjickk"
    print "3: New Age"
    print "4: Pagan"
    print "5: Political"
    print "6: Satanic"
    print "7: Self-Help"
    print "8: UFO"
    print "9: Based entirely on my own delusions"
    reply = raw_input()
else:
    if reply == '1':
        cult.base = 'Christian'
        cult.popularity = 20
        cult.weirdness = -10
        cult.term = 'Church'
    elif reply == '2':
        cult.weirdness = 10
        cult.base = 'Magjickk'
        cult.term = 'Circle'
    elif reply == '3':
        cult.base = 'New Age'
        cult.term = 'School'
    elif reply == '4':
        cult.base = 'Pagan'
        cult.term = 'Faith'
    elif reply == '5':
        cult.base = 'Political'
        cult.weirdness = -10
        cult.term = 'Movement'
    elif reply == '6':
        cult.base = 'Satanic'
        cult.popularity = -20
        cult.term = 'Church'
    elif reply == '7':
        cult.base = 'Self-Help'
        cult.term = 'Society'
    elif reply == '8':
        cult.base = 'UFO'
        cult.term = 'Society'
    elif reply == '9':
        cult.base = 'Original'
        cult.term = 'Cult'
        cult.weirdness = 20
        cult.doctrine = 0 #starting from scratch, here

print "What is the name of your %s %s?" % (cult.base, cult.term)
cult.name = ''
while len(cult.name) == 0:
    cult.name = raw_input()

reply = 0
while not reply in ('1','2','3'):
    print "Do you actually believe this stuff?"
    print "1: No. It's just a scam."
    print "2: I... think so?"
    print "3: Yes. This is THE TRUTH!"
    reply = raw_input()
else:
    if reply == '1':
        print "How cynical of you."
        leader.fanaticism = 10
    elif reply == '2':
        print "How openminded of you."
        leader.fanaticism = 40
    else: #reply == 3
        print "How certain of you."
        leader.fanaticism = 70
leader.dirt = 100 #ALL the dirt.  (At least at first?  Possible to get locked out of the loop later...)
print "Sadly, right now the only member of %s is you, %s.  You need to recruit!" % (cult.name, leader.name)

done = False
while not done:
    #any random events that hit this month
    #check for media, government, and enemy actions.
    print cult.doMonth()
    #cult status for the month.
    print cult.reportStatus()
    #what's the leader doing this month?
    leader_jobs = cult.monthlyCheckForDepartmentsAvailableToCultists(True)
    #Once you have more members, you can issue edicts.
    leader_action = numbermenu("What will you do this month?", ((1,"Recruit"),(2, "Indoctrinate recruits"),(3,"quit")), 0)
    if (leader_action == 1):
        #recruit_method = numbermenu("How will you recruit?", ((1,"Street Preaching"), (2,"Postering")), 0)
        recruit_method = numbermenu("How will you recruit?", [(1,"Street Preaching")], 0)
        if (recruit_method == 1):
            new_recruits = cult.proselytize([leader],100, True)
            if (len(new_recruits) > 1):
                print "You recruited", len(new_recruits), "new people!"
                cult.membership.extend(new_recruits)
            elif (len(new_recruits) == 1):
                print "You recruited", len(new_recruits), "new person!"
                cult.membership.extend(new_recruits)
            else:
                print "You were unable to recruit any new members."
        if (recruit_method == 2):
            new_recruits = cult.proselytize([leader],100, False)
            if (len(new_recruits) > 0):
                print "You recruited", len(new_recruits), "new people!"
                cult.membership.extend(new_recruits)
            else:
                print "You were unable to recruit any new members."
    elif (leader_action == 2):
        d = cult.assignLabor("recruit teachers", [leader])
        d.setPermanence(False)
        d.monthly_function = monthlyIndoctrination #Whoo, it worked!
        recruits = cult.getRecruits()
        recruit_count = len(recruits)
        if (recruit_count > 10):
            print "You can only teach a maximum of 10 recruits personally a month right now."
            recruit_count = 10
        number_to_indoctrinate = numberPrompt("How many recruits do you want to personally indoctrinate?", 0, recruit_count)
        if (number_to_indoctrinate > 0):
            d = cult.assignLabor("recruit students", recruits[0:number_to_indoctrinate])
            d.setPermanence(False)
            print len(d.people), "people in", d.name
            #DEBUG: For some reason, if only one cultist is set to 'recruit students', this fails.
               
    elif (leader_action == 3):
        done = True
        print "We're outta here!"
    #assign cultist labor for the month
    if (len(cult.membership) > 1):
        print "Assign work to cultists....later"
        cultist_jobs = cult.monthlyCheckForDepartmentsAvailableToCultists()
                                        
    """TODO: If a cult is famous/loved, there should be a non-zero chance
    of random people spontaneously joining."""
    """TODO: Raising fame/popularity shouldn't be automatic -
    make it a random roll that has to exceed the current value?"""
    
#main loop


"""Step one: The Leader
choose name, gender.  Everything else is random.
Gets a nice boost to persuasiveness."""

"""Possible random effects for starting cults:
Leader starts out rich.
Leader starts with a few followers.
Leader has a criminal record.
Leader is already a fanatic."""

"""Main loop:
Start current month(?)
Spread the Word! (Advertising)
Check to see how many people heard the Word.
How many of those are interested?
How many are repulsed? (much smaller)
Generate new recruits, add them to membership.

Check how the Happy Workers are doing.
Jobs:
Recruitment
Indoctrination
Fund-Raising/Day Jobs
Security
PR
Legal (or have to hire pros for this?)
Maintenance (Includes making food, repairs, etc.)
Rituals

reassign workers:
Look for talent among the recruits, recommend some for promotion/assignment
Track their stats - more or less fanatical, more or less stressed, etc....

Accounting
Money earned/donated to the cult
money spent
You can go into debt, but if it's too much, you're screwed.

Accountability
Chance of high fantaticism cultists getting in legal trouble - or doing crimes at your command.
The bigger you get, the more attention you get
Law enforcement attention is a hidden stat, until they show up at someone's door.
Media attention - free publicity and/or reputation ruining.
Rival cults defame you and cut into the sucker pool.

Random events
A SIGN FROM ABOVE!
Leader gets too high-fanaticism, says or does something crazy.
Random cult member says/does something crazy.
Schism?! (Cult needs to get pretty big, first)
Unexpected expenses
Unexpected windfall
Sudden inspiration!"""

"""Leader actions:
Recruit
Preach
Issue edict
    demand tithes
    forbid behavior - increases stress & fanaticism, weeds out the unfaithful
    
What else?
Set living standards for full-time cultists (need a place for them to sleep, too)
Buy stuff with cult money
"""

"""Dogmas:
Different things the cult doctrine has.
When you start a cult, you pick one (or more?)
Can be politics, social, whatevs

Liberal, Conservative
Free-Love, Abstinent
Peaceful, Militant
Free-Enterprise, Socialist
Racist, Sexist, Eglitarian
Drugs, Straight-edge
Paranoid
Consumerist, Ascetic
Or just things you believe in:
Atlantis
Psychic
UFO
Doomsday
Majjyck
Hollow earth
Reincarnation, afterlife, one-shot
pessimistic, optmistic
Transhumanist
Spirit warfare
"""
