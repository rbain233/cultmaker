import os
import pickle

os.chdir("C:/lab/cultmaker") #AHA!
#object = open("./save.p", "r+") 

print "saving colors."
favorite_color = { "lion": "yellow", "kitty": "red" }
pickle.dump( favorite_color, open( "save.p", "wb+" ) )

print "loading colors."
loaded_color = pickle.load( open( "save.p", "rb" ) )
print loaded_color

#IT WORKS!