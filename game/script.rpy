# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define a = Character("Ana")


# The game starts here.

label start:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene class 1 neutral state with fade

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.

    show ana fullbody neutral:
        # 1. Zoom in significantly to crop the legs out
        zoom 0.75 
        
        # 2. Keep her horizontally centered
        xalign 0.5 
        
        # 3. Use yalign to bring her head down into view. 
        # 0.0 is the top of the image. 0.1-0.2 usually puts the head near the top of the screen.
        yalign -0.1

    # These display lines of dialogue.

    a "You've created a new Ren'Py game." with hpunch

    a "Once you add a story, pictures, and music, you can release it to the world!"

    # This ends the game.

    return
