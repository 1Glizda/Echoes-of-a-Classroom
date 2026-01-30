# --- 1. DEFINE VARS & LOGIC ---
default smart = 50
default positiveness = 50
default confidence = 50
default current_tier = "medium"

init python:
    # Logic to calculate the Tier based on design doc: 
    # [cite_start]Low: 0-29% [cite: 18][cite_start], Medium: 30-59% [cite: 19][cite_start], High: 60-100% [cite: 20]
    def update_visual_state():
        # You can use an average, or a specific stat. Here is the average method:
        avg_stat = (store.smart + store.positiveness + store.confidence) / 3.0

        if avg_stat >= 60:
            store.current_tier = "high"
        elif avg_stat >= 30:
            store.current_tier = "medium"
        else:
            store.current_tier = "low"

    # Helper function to change stats cleanly in dialogue
    def change_stat(stat_name, amount):
        current_val = getattr(store, stat_name)
        # Clamp values between 0 and 100
        new_val = max(0, min(100, current_val + amount))
        setattr(store, stat_name, new_val)
        
        # Immediately recalculate the tier
        update_visual_state()

# --- 2. SHADER & TRANSFORMS ---
init python:
    renpy.register_shader("custom.radial_bar", variables="""
        uniform float u_progress;
        uniform float u_radius_crop;
        varying vec2 v_tex_coord;
        attribute vec2 a_tex_coord;
    """, vertex_200="""
        v_tex_coord = a_tex_coord;
    """, fragment_functions="""
        float get_angle(vec2 pos) {
            float angle = atan(pos.x, -pos.y);
            if (angle < 0.0) angle += 6.28318;
            return angle / 6.28318;
        }
    """, fragment_200="""
        vec2 center = vec2(0.5, 0.5);
        vec2 dist_vec = v_tex_coord - center;
        
        // 1. CIRCLE CROP
        if (length(dist_vec) > 0.495) {
            discard; 
        }

        // 2. RADIAL CROP
        if (u_radius_crop > 0.5) { 
            if (get_angle(dist_vec) > u_progress) {
                discard;
            }
        }
    """)

# Apply shader to the colored circles
transform radial_fill(score, total=100):
    shader "custom.radial_bar"
    u_progress (score / float(total))
    u_radius_crop 1.0 

# Apply shader to the white circles (just makes them round)
transform just_circle:
    shader "custom.radial_bar"
    u_progress 1.0
    u_radius_crop 0.0 

# --- 3. THE HUD SCREEN ---
screen status_hud():
    zorder 100
    
    hbox:
        xalign 0.05
        yalign 0.05
        spacing 25

        # --- SMART (Blue) ---
        fixed:
            xysize (100, 100)
            
            add Flatten(Solid("#2E5BFF")) at radial_fill(smart):
                xysize (100, 100) align (0.5, 0.5)
            
            add Flatten(Solid("#FFFFFF")) at just_circle:
                xysize (80, 80) align (0.5, 0.5)
                
            add "gui/hud/icon_smart.png":
                align (0.5, 0.5) fit "contain" zoom 0.6

        # --- CONFIDENCE (Yellow) ---
        fixed:
            xysize (100, 100)
            
            add Flatten(Solid("#FFD700")) at radial_fill(confidence):
                xysize (100, 100) align (0.5, 0.5)
            
            add Flatten(Solid("#FFFFFF")) at just_circle:
                xysize (80, 80) align (0.5, 0.5)
                
            add "gui/hud/icon_confidence.png":
                align (0.5, 0.5) fit "contain" zoom 0.6

        # --- POSITIVENESS (Red) ---
        fixed:
            xysize (100, 100)
            
            add Flatten(Solid("#FF4B2B")) at radial_fill(positiveness):
                xysize (100, 100) align (0.5, 0.5)
            
            add Flatten(Solid("#FFFFFF")) at just_circle:
                xysize (80, 80) align (0.5, 0.5)
            
            add "gui/hud/icon_positiveness.png":
                align (0.5, 0.5) fit "contain" zoom 0.6

# --- 4. ASSET DEFINITION ---
# Added 'transition=dissolve for the smooth fade.

# BACKGROUNDS
image bg classroom1 = ConditionSwitch(
    "current_tier == 'high'", "images/bg/CLASS 1 ( watercolor state).png",
    "current_tier == 'medium'", "images/bg/class 1 neutral state.png",
    "current_tier == 'low'", "images/bg/CLASS 1 ( grey state).png",
    transition=dissolve
)

image bg classroom2 = ConditionSwitch(
    "current_tier == 'high'", "images/bg/CLASS 2 ( watercolor state).png",
    "current_tier == 'medium'", "images/bg/CLASS 2 ( neutral state).png",
    "current_tier == 'low'", "images/bg/CLASS 2 ( grey state).png",
    transition=dissolve
)

image bg walkhome = ConditionSwitch(
    "current_tier == 'high'", "images/bg/WALK HOME(watercolor state).png",
    "current_tier == 'medium'", "images/bg/WALK HOME( neutral state).png",
    "current_tier == 'low'", "images/bg/WALK HOME ( grey state).png",
    transition=dissolve
)

# Static Images
image bg shop = "images/bg/SHOP (grey state ).png"
image bg room = "images/bg/room grey state.png"
image bg school gate = "images/bg/SCHOOL GATE ( grey state).png"

# CHARACTERS
# LIA POSES
image lia fullbody= ConditionSwitch(
    "current_tier == 'high'", "images/fullbody/watercolor state/lia fullbody watercolor.PNG",
    "current_tier == 'medium'", "images/fullbody/neutral state/lia fullbody neutral.PNG",
    "current_tier == 'low'", "images/fullbody/grey state/lia fullbody grey.PNG",
    transition=dissolve
)

image lia neutral = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/lia/lia neutral face watercolor.PNG",
    "current_tier == 'medium'", "images/halfbody/neutral state/lia/lia neutral face neutral.PNG",
    "current_tier == 'low'", "images/halfbody/grey state/lia/lia neutral face grey.PNG",
    transition=dissolve
)

image lia thinking = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/lia/lia pensive watercolor.PNG",
    "current_tier == 'medium'", "images/halfbody/neutral state/lia/lia pensive neutral.PNG",
    "current_tier == 'low'", "images/halfbody/grey state/lia/lia pensive grey.PNG",
    transition=dissolve
)

image lia sad = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/lia/lia sad watercolor.PNG",
    "current_tier == 'medium'", "images/halfbody/neutral state/lia/lia sad neutral.PNG",
    "current_tier == 'low'", "images/halfbody/grey state/lia/lia sad grey.PNG",
    transition=dissolve
)

image lia smiling = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/lia/lia smiling watercolor.PNG",
    "current_tier == 'medium'", "images/halfbody/neutral state/lia/lia smiling neutral.PNG",
    "current_tier == 'low'", "images/halfbody/grey state/lia/lia smiling grey.PNG",
    transition=dissolve
)

# ANA POSES
image ana fullbody = ConditionSwitch(
    "current_tier == 'high'", "images/fullbody/watercolor state/ana fullbody watercolor.PNG",
    "current_tier == 'medium'", "images/fullbody/neutral state/ana fullbody neutral.PNG",
    "current_tier == 'low'", "images/fullbody/grey state/ana fullbody grey.PNG",
    transition=dissolve
)

image ana frowning = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/ana/ana frowning watercolor .PNG",
    "current_tier == 'medium'", "images/halfbody/neutral state/ana/ana frowning neutral.PNG",
    "current_tier == 'low'", "images/halfbody/grey state/ana/ana frowning grey.PNG",
    transition=dissolve
)

image ana neutral = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/ana/ana neutral face watercolor.PNG",
    "current_tier == 'medium'", "images/halfbody/neutral state/ana/ana neutral face neutral.PNG",
    "current_tier == 'low'", "images/halfbody/grey state/ana/ana neutral face grey.PNG",
    transition=dissolve
)

image ana sad = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/ana/ana sad watercolor.PNG",
    "current_tier == 'medium'", "images/halfbody/neutral state/ana/ana sad neutral.PNG",
    "current_tier == 'low'", "images/halfbody/grey state/ana/ana sad grey.PNG",
    transition=dissolve
)

image ana smiling = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/ana/ana smiling watercolor .PNG",
    "current_tier == 'medium'", "images/halfbody/neutral state/ana/ana smiling neutral.PNG",
    "current_tier == 'low'", "images/halfbody/grey state/ana/ana smiling grey.PNG",
    transition=dissolve
)

# DORIAN POSES
image dorian fullbody = ConditionSwitch(
    "current_tier == 'high'", "images/fullbody/watercolor state/dorian fullbody watercolor.PNG",
    "current_tier == 'medium'", "images/fullbody/neutral state/dorian fullbody neutral.PNG",
    "current_tier == 'low'", "images/fullbody/grey state/dorian fullbody grey.PNG",
    transition=dissolve
)

image dorian frowning = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/dorian/dorian frowning watercolor.PNG",
    "current_tier == 'medium'", "images/halfbody/neutral state/dorian/dorian frowning neutral.PNG",
    "current_tier == 'low'", "images/halfbody/grey state/dorian/dorian frowning grey.PNG",
    transition=dissolve
)

image dorian neutral = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/dorian/dorian neutral face watercolor.PNG",
    "current_tier == 'medium'", "images/halfbody/neutral state/dorian/dorian neutral face neutral.PNG",
    "current_tier == 'low'", "images/halfbody/grey state/dorian/dorian neutral face grey.PNG",
    transition=dissolve
)

image dorian smiling = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/dorian/dorian smiling watercolor .PNG",
    "current_tier == 'medium'", "images/halfbody/neutral state/dorian/dorian smiling neutral.PNG",
    "current_tier == 'low'", "images/halfbody/grey state/dorian/dorian smiling grey.PNG",
    transition=dissolve
)

image dorian smirking = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/dorian/dorian smirking watercolor.PNG",
    "current_tier == 'medium'", "images/halfbody/neutral state/dorian/dorian smirking neutral.PNG",
    "current_tier == 'low'", "images/halfbody/grey state/dorian/dorian smirking grey.PNG",
    transition=dissolve
)

# JACOB POSES
# Note: I matched the extra space in "neutral .PNG" and the typos "movking" and "javob"
image jacob fullbody = ConditionSwitch(
    "current_tier == 'high'", "images/fullbody/watercolor state/jacob fullbody watercolor.PNG",
    "current_tier == 'medium'", "images/fullbody/neutral state/jacob fullbody neutral .PNG",
    "current_tier == 'low'", "images/fullbody/grey state/jacob fullbody grey.PNG",
    transition=dissolve
)

image jacob frowning = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/jacob/javob frowning watercolor.PNG",
    "current_tier == 'medium'", "images/halfbody/neutral state/jacob/jacob frowning neutral.PNG",
    "current_tier == 'low'", "images/halfbody/grey state/jacob/jacob frowning grey.PNG",
    transition=dissolve
)

image jacob mocking = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/jacob/jacob mocking watercolor.PNG",
    "current_tier == 'medium'", "images/halfbody/neutral state/jacob/jacob mocking neutral.PNG",
    "current_tier == 'low'", "images/halfbody/grey state/jacob/jacob movking grey.PNG",
    transition=dissolve
)

image jacob neutral = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/jacob/jacob neutral face watercolor.PNG",
    "current_tier == 'medium'", "images/halfbody/neutral state/jacob/jacob neutral face neutral.PNG",
    "current_tier == 'low'", "images/halfbody/grey state/jacob/jacob neutral face grey.PNG",
    transition=dissolve
)

image jacob smiling = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/jacob/jacob smiling watercolor.PNG",
    "current_tier == 'medium'", "images/halfbody/neutral state/jacob/jacob smiling neutral.PNG",
    "current_tier == 'low'", "images/halfbody/grey state/jacob/jacob smiling grey.PNG",
    transition=dissolve
)

# MARA POSES
image mara fullbody = ConditionSwitch(
    "current_tier == 'high'", "images/fullbody/watercolor state/mara fullbody watercolor.PNG",
    "current_tier == 'medium'", "images/fullbody/neutral state/mara fullbody neutral.PNG",
    "current_tier == 'low'", "images/fullbody/grey state/mara fullbody grey.PNG",
    transition=dissolve
)

image mara neutral = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/mara/mara neutral face watercolor.PNG",
    "current_tier == 'medium'", "images/halfbody/neutral state/mara/mara neutral face neutral.PNG",
    "current_tier == 'low'", "images/halfbody/grey state/mara/mara neutral face grey.PNG",
    transition=dissolve
)

image mara sad = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/mara/mara sad watercolor.PNG",
    "current_tier == 'medium'", "images/halfbody/neutral state/mara/mara sad neutral.PNG",
    "current_tier == 'low'", "images/halfbody/grey state/mara/mara sad grey.PNG",
    transition=dissolve
)

image mara smiling = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/mara/mara smiling watercolor.PNG",
    "current_tier == 'medium'", "images/halfbody/neutral state/mara/mara smiling neutral.PNG",
    "current_tier == 'low'", "images/halfbody/grey state/mara/mara smiling grey.PNG",
    transition=dissolve
)

# SOFIA POSES
image sofia fullbody = ConditionSwitch(
    "current_tier == 'high'", "images/fullbody/watercolor state/sofia fullbody watercolor.PNG",
    "current_tier == 'medium'", "images/fullbody/neutral state/sofia fullbody neutral.PNG",
    "current_tier == 'low'", "images/fullbody/grey state/sofia fullbody grey.PNG",
    transition=dissolve
)

image sofia neutral = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/sofia/sofia neutral face watercolor.PNG",
    "current_tier == 'medium'", "images/halfbody/neutral state/sofia/sofia neutral face neutral.PNG",
    "current_tier == 'low'", "images/halfbody/grey state/sofia/sofia neutral face grey.PNG",
    transition=dissolve
)

image sofia sad = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/sofia/sofia sad watercolor.PNG",
    "current_tier == 'medium'", "images/halfbody/neutral state/sofia/sofia sad neutral.PNG",
    "current_tier == 'low'", "images/halfbody/grey state/sofia/sofia sad grey.PNG",
    transition=dissolve
)

image sofia smiling = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/sofia/sofia smiling watercolor.PNG",
    "current_tier == 'medium'", "images/halfbody/neutral state/sofia/sofia smiling neutral.PNG",
    "current_tier == 'low'", "images/halfbody/grey state/sofia/sofia smiling grey.PNG",
    transition=dissolve
)

# LADY AT THE STORE
image shoplady = ConditionSwitch(
    "current_tier == 'high'", "images/doamna de la magazin/watercolor.PNG",
    "current_tier == 'medium'", "images/doamna de la magazin/neutral.PNG",
    "current_tier == 'low'", "images/doamna de la magazin/grey.PNG",
    transition=dissolve
)

# --- 5. CHARACTERS ---
define lia = Character("Lia")
define dorian = Character("Dorian")
define ana = Character("Ana")
define mara = Character("Mrs. Mara")
define jacob = Character("Jacob")
define sofia = Character("Miss Sofia")
define shoplady = Character("Shop Lady")

# --- 6. ACTUAL GAME ---
label start:
    # 1. Initialize logic
    $ update_visual_state()
    
    # 2. Show HUD and Background
    show screen status_hud

    scene bg room
    
    player "I woke up in my room. Another morning."

    scene bg classroom1 with dissolve

    # 3. Demonstrate State Change
    # Current stats are 50/50/50 (Medium). The background is Neutral.
    
    show lia fullbody with dissolve:
        zoom 0.5
        xalign 0.99
        yalign -0.2
    
    show ana fullbody with dissolve:
        zoom 0.5
        xalign 0.4
        yalign -0.2

    lia "Hey, you look okay today. (Medium Tier)" with dissolve

    menu:
        "Everything feels terrible. (Go to Low Tier)":
            # We use the helper function we made in Step 1
            $ change_stat("smart", -30)
            $ change_stat("positiveness", -30)
            $ change_stat("confidence", -30)
            # This drops avg to 20. Tier becomes "low".
            # Background and Lia will AUTOMATICALLY dissolve to grey/sketch style.
            
            ana "Oh... you look really lost now. (Low Tier)"

        "Try my best (+30 to all stats)":
            $ change_stat("smart", 30)
            $ change_stat("positiveness", 30)
            $ change_stat("confidence", 30)
            # This raises avg to 80. Tier becomes "high".
            # Background and Lia will AUTOMATICALLY dissolve to watercolor style.
            
            lia "Wow! You're glowing! (High Tier)"

    player "My HUD should update, and the art style should have changed instantly."

    return