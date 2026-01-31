# --- 1. THE CLASSROOM INTERACTION SCREEN ---
screen classroom_selector(available_chars):

    # --- A. DYNAMIC SLOT CALCULATION ---
    # We count the characters to decide which layout to use.
    $ num_chars = len(available_chars)

    # 1. DEFINE LAYOUTS
    if num_chars == 3:
        $ current_slots = [
            (100, 400, 0.65), 
            (600,  400, 0.65), 
            (1000, 400, 0.65)
        ]
        $ use_xalign = True # Flag to tell the button to use xalign

    elif num_chars == 2:
        $ current_slots = [
            (300, 400, 0.65), 
            (800, 400, 0.65)
        ]
        $ use_xalign = True

    elif num_chars == 1:
        $ current_slots = [(600, 400, 0.65)]
        $ use_xalign = True

    elif num_chars == 0:
        timer 0.1 action Return("next_scene")

    else: 
        # --- DEFAULT LAYOUT (Using your original xpos pixels) ---
        # Used for 4 characters (or 1, or 5+)
        $ current_slots = [
            (-200, 400, 0.65),
            (350, 400, 0.65),
            (850, 400, 0.65),
            (1200, 400, 0.65)
        ]
        $ use_xalign = False

    # --- B. DEFINE HOVER EXPRESSIONS ---
    $ hover_map = {
        "lia": "thinking",
        "dorian": "smirking",
        "ana": "smiling",
        "mara": "smiling",
        "jacob": "frowning",
        "sofia": "smiling"
    }

    # --- C. RENDER LOOP ---
    for index, char_name in enumerate(available_chars):

        if index < len(current_slots):
            
            # Get data for this specific seat
            $ slot_x, slot_y, slot_zoom = current_slots[index]
            $ current_hover_expression = hover_map.get(char_name, "neutral")

            imagebutton:
                idle char_name + " neutral"
                hover char_name + " " + current_hover_expression

                # --- D. CONDITIONAL POSITIONING ---
                # This switches between 'xalign' (centering) and 'xpos' (manual pixels)
                if use_xalign:
                    xpos slot_x 
                else:
                    xpos slot_x
                
                ypos slot_y
                
                focus_mask True
                
                # --- INTERACTION ---
                # Use this if you want them to leave the room (triggering the realign):
                # action [RemoveFromSet(available_chars, char_name), Return()]
                
                # Use this if you just want to select them:
                action Return(char_name)

                at transform:
                    zoom slot_zoom

    # NEXT SCENE BUTTON
    textbutton "Go to Next Scene":
        xalign 0.98 yalign 0.05
        padding (20, 20)
        background "#00000088"
        action Return("next_scene")


screen status_hud():
    zorder 100
    
    # --- CHANGE DETECTION VARIABLES ---
    # These track the values from the previous frame. 
    # If 'smart' changes, 'smart != last_smart' becomes True.
    default last_smart = smart
    default last_confidence = confidence
    default last_positiveness = positiveness

    hbox:
        xalign 0.05
        yalign 0.05
        spacing 25

        # --- SMART (Blue) ---
        fixed:
            xysize (100, 100)
            
            # 1. The Background Circle (Optional, keeps it clean)
            add Flatten(Solid("#00000044")) at just_circle:
                xysize (100, 100) align (0.5, 0.5)

            # 2. The Stat Bar (Original)
            add Flatten(Solid("#2E5BFF")) at radial_fill(smart):
                xysize (100, 100) align (0.5, 0.5)

            # 3. THE GLOW EFFECT (New)
            if smart != last_smart:
                # Creates a white circle that expands and fades
                add Flatten(Solid("#FFFFFF")) at just_circle, stat_pulse_effect:
                    xysize (100, 100) align (0.5, 0.5)
                
                # Reset the tracker after 0.5s so the glow stops
                timer 0.5 action SetScreenVariable("last_smart", smart)

            # 4. The White Inner Circle (Original)
            add Flatten(Solid("#FFFFFF")) at just_circle:
                xysize (80, 80) align (0.5, 0.5)
                
            # 5. The Icon (Original)
            add "gui/hud/icon_smart.png":
                align (0.5, 0.5) fit "contain" zoom 0.6

        # --- CONFIDENCE (Yellow) ---
        fixed:
            xysize (100, 100)
            
            add Flatten(Solid("#00000044")) at just_circle:
                xysize (100, 100) align (0.5, 0.5)

            add Flatten(Solid("#FFD700")) at radial_fill(confidence):
                xysize (100, 100) align (0.5, 0.5)
            
            # THE GLOW EFFECT
            if confidence != last_confidence:
                add Flatten(Solid("#FFFFFF")) at just_circle, stat_pulse_effect:
                    xysize (100, 100) align (0.5, 0.5)
                timer 0.5 action SetScreenVariable("last_confidence", confidence)

            add Flatten(Solid("#FFFFFF")) at just_circle:
                xysize (80, 80) align (0.5, 0.5)
                
            add "gui/hud/icon_confidence.png":
                align (0.5, 0.5) fit "contain" zoom 0.6

        # --- POSITIVENESS (Red) ---
        fixed:
            xysize (100, 100)
            
            add Flatten(Solid("#00000044")) at just_circle:
                xysize (100, 100) align (0.5, 0.5)

            add Flatten(Solid("#FF4B2B")) at radial_fill(positiveness):
                xysize (100, 100) align (0.5, 0.5)
            
            # THE GLOW EFFECT
            if positiveness != last_positiveness:
                add Flatten(Solid("#FFFFFF")) at just_circle, stat_pulse_effect:
                    xysize (100, 100) align (0.5, 0.5)
                timer 0.5 action SetScreenVariable("last_positiveness", positiveness)

            add Flatten(Solid("#FFFFFF")) at just_circle:
                xysize (80, 80) align (0.5, 0.5)
            
            add "gui/hud/icon_positiveness.png":
                align (0.5, 0.5) fit "contain" zoom 0.6
# 3. --- QUIZ VARIABLES ---
# These are used only within the screen logic
default timer_phase = 0
default show_hint = False

transform ui_fade_appear:
    on show:
        alpha 0.0
        linear 0.5 alpha 1.0  # Fades in over 2.0 seconds
    on hide:
        linear 0.5 alpha 0.0  # Fades out quickly when done

screen quiz_screen(question_data):
    modal True
    
    # --- 1. SETUP: Variables & Sound ---
    # FIXED: Defined INSIDE the screen so 'ScreenVariable' actions work
    default timer_phase = 0
    default show_hint = False
    
    default time_per_phase = 2.0 # 2 seconds for every tick on the clock. Total of 16 seconds per question.
    
    # Audio Logic
    on "show" action Play("music", audio.sfx_clock_ticking_bg, loop=True, fadeout=1.0)
    on "hide" action Stop("music", fadeout=0.5)

    # --- 2. TIMER LOGIC ---
    timer time_per_phase repeat True:
        action If(
            timer_phase < 8,
            # Increment phase & Play Tick
            true=[SetScreenVariable("timer_phase", timer_phase + 1), Play("sound", audio.sfx_timer_tick)],
            # Time up
            false=[Play("sound", audio.sfx_time_over), Return("timeout")]
        )

    # --- 3. UI LAYOUT ---
    frame:
        at ui_fade_appear # Apply the fade transform here
        background "#000000cc" 
        xfill True yfill True
        padding (50, 50)

        vbox:
            align (0.5, 0.5)
            spacing 30
            
            # --- TIMER VISUALS (FIXED) ---
            fixed:
                xysize (130, 130)
                align (0.5, 0.0)
                
                # FIXED: We construct the image name dynamically based on the current phase
                # Images must be named 1.png, 2.png ... 8.png in 'images/timer/'
                # We use timer_phase + 1 because the variable starts at 0, but files usually start at 1.
                add "images/timer/" + str(timer_phase + 1) + ".png":
                    align (0.5, 0.5) fit "contain"
            
            # --- QUESTION TEXT ---
            text question_data["q"]:
                xalign 0.5 text_align 0.5
                size 40 color "#ffffff"
                layout "subtitle"
                xsize 1000

            # --- HINT BUTTON & TEXT ---
            textbutton "💡 Hint":
                # This now works because 'show_hint' is defined inside the screen
                action ToggleScreenVariable("show_hint")
                align (0.5, 0.0)
                text_size 25
                text_color "#FFFF00"
            
            if show_hint:
                text question_data["hint"]:
                    xalign 0.5 text_align 0.5
                    color "#FFFF00" size 25 italic True

            null height 20

            # --- ANSWER OPTIONS ---
            grid 2 2:
                align (0.5, 0.5)
                spacing 20
                xsize 800
                
                for opt in question_data["options"]:
                    textbutton opt:
                        xfill True
                        padding (20, 20)
                        background "#ffffff22"
                        text_xalign 0.5  # Centers the text horizontally (0.0 is Left, 1.0 is Right)
                        text_yalign 0.5  # Centers the text vertically (optional, but good practice)
                        text_text_align 0.5
                        
                        if opt == question_data["correct"]:
                            action [Play("sound", audio.sfx_quiz_correct), Return("correct")]
                        else:
                            action [Play("sound", audio.sfx_quiz_wrong), Return("wrong")]

# --- FEEDBACK SCREEN (Post-Quiz) ---
screen quiz_feedback(is_correct, explanation):
    modal True
    
    frame:
        background "#000000ee"
        align (0.5, 0.5)
        padding (60, 60)
        xsize 800
        
        vbox:
            spacing 20
            
            if is_correct:
                text "Exactly!" color "#23c552" size 60 xalign 0.5 bold True
            else:
                text "Not quite..." color "#f84f32" size 60 xalign 0.5 bold True
            
            null height 10
            
            text explanation:
                xalign 0.5 text_align 0.5
                size 30
            
            null height 30
            
            textbutton "Continue":
                xalign 0.5
                padding (30, 15)
                background "#ffffff44"
                action Return()