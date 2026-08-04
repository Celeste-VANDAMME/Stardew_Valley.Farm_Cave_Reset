
# <!> User Input
# --------------
# Replace with your save data here:

data_directory = "save.txt"
DEBUG_MODE = False



# Program summary:
# ------------------------------------------
# 1. We open the save file at the specified location in the "data_directory" variable.
# 
# 2. a. Find the first "<eventsSeen>" of the file data.
#    b. Remove the value of "int 65" (which is linked to Demetrius cave choice event)
# 
# 3. OPTIONNAL: If the cave had objects in the past (such as the mushroom pots from a previous mushroom cave), we can REMOVE them.
#    a. Find the area in the save where the cave data location is ("<GameLocation xsi:type="FarmCave">").
#    b. Remove every "<objects>" in this area.
#
# 4. We save the final content onto a new file, ready to be used for Stardew Valley.
#
# 5. Once you've run the program, you can boot up the game and start a new day.
#    Demetrius should come up to your door and ask you for a new cave type.
# ------------------------------------------

# 1.
with open(data_directory, "r", encoding="utf-8") as f:
    data = f.read()


# 2.a. + 2.b.
str_eventSeen = "<eventsSeen>"
str_int65 = "<int>65</int>"

pos_eventSeen = data.find(str_eventSeen)
pos_int65 = data.find(str_int65, pos_eventSeen)

data_noEvent = data[ :pos_int65] + data[(pos_int65+len(str_int65)): ]

# print("<int> REMOVED: ", data[pos_int65:pos_int65+len(str_int65)])


# 3.a + 3.b
str_caveLocation = '<GameLocation xsi:type="FarmCave">'
str_objects = "<objects>"
str_objects_end = "</objects>"

pos_caveLocation = data_noEvent.find(str_caveLocation)

pos_objects = data_noEvent.find( str_objects, pos_caveLocation )
pos_objects_end = data_noEvent.find( str_objects_end, pos_objects )

str_objects_content = data_noEvent[pos_objects:pos_objects_end+len(str_objects_end)] # Optionnal, I just keep it for debugging sake
data_noEvent_noObject = data_noEvent[ :pos_objects] + data_noEvent[pos_objects_end+len(str_objects_end): ]

# print("POS. OBJECT START:", pos_objects, " /// POS END: ", pos_objects_end)
# print( data_without_event[pos_objects:pos_objects+len(str_objects)] )
# print(str_objects_content)


# 4.
output_directory = "save_modified.txt"

with open(output_directory, "w", encoding="utf-8") as f:
    f.write(data_noEvent_noObject)

