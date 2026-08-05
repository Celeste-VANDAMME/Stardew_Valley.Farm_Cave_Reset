# [>] LIBRARIES & DEPENDENCIES
# ------------------------------
from pathlib import Path
from dataclasses import dataclass
import os
from  zipfile import ZipFile
from datetime import datetime

# [>] DATACLASS
# ------------------------------
@dataclass
class SaveFile:
    name: str
    raw_name: str
    path: Path


# [>] GLOBAL VARIABLES
# ------------------------------
DEBUG_MODE = False 
"""Display detailled logs of every action in the code."""

BACKUP_BASE_DIR = Path("Stardew-Backups/")


# [>] FUNCTIONS
# ------------------------------
def saveDir_autoDetector( ) -> list[SaveFile]:

    save_directory = Path(os.environ["APPDATA"]) / "StardewValley" / "Saves"

    if ( save_directory.exists() and save_directory.is_dir() ):

        saves_available = [
            SaveFile(
                name = "_".join(save.name.split("_")[0:-1]),
                raw_name=save.name,
                path = save,
            )

            for save in save_directory.iterdir() 
            if ( save.is_dir() ) 
            ]
        
        return saves_available

    else:
        print( "/!/ Saving location not found in %APPDATA%" )
        return []


def saves_display( saveList:list[SaveFile] ):

    print( "[>] AVAILABLE SAVES:")
    print( "--------------" )
    
    for index, save in enumerate(saveList, 1):
        print(f"{index} - {save.name}")

    return


def saves_selection( saveNB:int ):

    userChoice_str = ""
    loopCounter = 0

    while( loopCounter < 10 ):
        userChoice_str = input( "[?] Choose a save: ")

        if( not userChoice_str.isdigit() ):
            print("[!] Error on input, please select a number (example: '4')")

            loopCounter += 1
            continue


        userChoice = int(userChoice_str) - 1

        if( userChoice in range(0, saveNB) ): # --- Proper exit of the while( ... )
            return userChoice

        else:
            print("[!] ERROR: The input number is out of range from the available saves...")

            loopCounter += 1
            continue

    
    raise Exception("[!] ERROR: Too many tries, stopping the program.") # TODO: Add a proper exception handling.
    return -1


def save_backup( save:SaveFile ):

    # Let's prepare the folder:
    BACKUP_BASE_DIR.mkdir(exist_ok=True)

    backup_path = BACKUP_BASE_DIR / (
    save.name + "_" +
    datetime.now().strftime("%Y-%m-%d_%H-%M-%S") +
    ".zip"
    )

    # print(backup_dir)

    # We're now ready to create the archive!
    with ZipFile(backup_path, mode="w") as archive:
        for content in save.path.rglob("*"):

            if content.is_file():
                    # print(file.relative_to(save.path) )
                    archive.write( content, content.relative_to(save.path) )


    return


def save_cave_reset( save:SaveFile ):
    """
    Reset the Farm Cave choice for a Stardew Valley save.
    """

    # Algorithm overview
    # ------------------
    # 1. Open the save.
    # 2. Remove "event 65".
    # 3. Remove "Farm Cave objects".
    # 4. Save the modified file.

    # 1.

    savefile_content_path = save.path / save.raw_name

    with open(savefile_content_path, "r", encoding="utf-8") as f:
        data = f.read()


    # 2
    str_eventSeen = "<eventsSeen>"
    str_int65 = "<int>65</int>"

    pos_eventSeen = data.find(str_eventSeen)
    pos_int65 = data.find(str_int65, pos_eventSeen)

    data_noEvent = data[ :pos_int65] + data[(pos_int65+len(str_int65)): ]

    # print("<int> REMOVED: ", data[pos_int65:pos_int65+len(str_int65)])


    # 3
    str_caveLocation = '<GameLocation xsi:type="FarmCave">'
    str_objects = "<objects>"
    str_objects_end = "</objects>"

    pos_caveLocation = data_noEvent.find(str_caveLocation)

    pos_objects = data_noEvent.find( str_objects, pos_caveLocation )
    pos_objects_end = data_noEvent.find( str_objects_end, pos_objects )

    # str_objects_content = data_noEvent[pos_objects:pos_objects_end+len(str_objects_end)] # Optionnal, I just keep it for debugging sake
    data_noEvent_noObject = data_noEvent[ :pos_objects] + data_noEvent[pos_objects_end+len(str_objects_end): ]

    # print("POS. OBJECT START:", pos_objects, " /// POS END: ", pos_objects_end)
    # print( data_without_event[pos_objects:pos_objects+len(str_objects)] )
    # print(str_objects_content)


    # 4.
    with open(savefile_content_path, "w", encoding="utf-8") as f:
        f.write(data_noEvent_noObject)



# [>] MAIN PROGRAM
# ------------------------------

def main() -> int:

    saveList = saveDir_autoDetector()

    # In case no save files were found:
    if len(saveList) == 0:
        print("/!/ Error while automatically finding the saves. :(")
        # TODO: Add a system to manually input the value from user (with a "browse"... window?).
    

    saves_display( saveList )
    selectedSave = saveList[ saves_selection( len(saveList) ) ]

    save_backup( selectedSave )
    save_cave_reset( selectedSave )

    return 0


# [>] main() launcher
# ------------------------------
if __name__ == "__main__":
    main()