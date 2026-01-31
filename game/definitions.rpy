# --- 1. DEFINE VARS & LOGIC ---
default smart = 4
default positiveness = 4
default confidence = 4
default current_tier = "medium"
default last_music_tier = "low"
default new_tier = "medium"

# --- VISUAL & AUDIO STATE MANAGER ---
init python:
    import random

    # --- DEFINE MUSIC PLAYLISTS ---
    playlist_high = ["audio/music/happy_1.mp3", "audio/music/happy_2.mp3", "audio/music/happy_3.mp3"]
    
    playlist_med  = ["audio/music/neutral_1.mp3", "audio/music/neutral_2.mp3"]
    
    playlist_low  = ["audio/music/sad_1.mp3", "audio/music/sad_2.mp3", "audio/music/sad_3.mp3"]

    def update_visual_state():
        # Calculate the Tier
        avg_stat = (store.smart + store.positiveness + store.confidence) / 3.0

        if avg_stat >= 6:
            store.current_tier = "high"
        elif avg_stat >= 3:
            store.current_tier = "medium"
        else:
            store.current_tier = "low"  
            
        update_music_state(store.current_tier)

    def update_music_state(new_tier):
        # FIXED: We use 'store.last_music_tier' to access the saved variable
        if new_tier != store.last_music_tier:            
            if new_tier == "high":
                track = renpy.random.choice(playlist_high)
            elif new_tier == "medium":
                track = renpy.random.choice(playlist_med)
            else: # low
                track = renpy.random.choice(playlist_low)
            
            # Play the track
            if track:
                renpy.music.play(track, fadeout=2.0, fadein=2.0, loop=True)
            
            # Update the saved variable
            store.last_music_tier = new_tier

    # Helper function to change stats cleanly in dialogue
    def change_stat(stat_name, amount):
        current_val = getattr(store, stat_name)
        new_val = max(0, min(10, current_val + amount))
        setattr(store, stat_name, new_val)
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
transform radial_fill(score, total=10):
    shader "custom.radial_bar"
    u_progress (score / float(total))
    u_radius_crop 1.0 

# Apply shader to the white circles (just makes them round)
transform just_circle:
    shader "custom.radial_bar"
    u_progress 1.0
    u_radius_crop 0.0 

# This makes an element pop out and fade (0.5 seconds duration)
transform stat_pulse_effect:
    alpha 0.0 zoom 1.0
    parallel:
        easein 0.1 alpha 0.6  # Flash in
        easeout 0.4 alpha 0.0 # Fade out
    parallel:
        easeout 0.5 zoom 1.3  # Expand outward

# --- 3. ASSET DEFINITION ---
# Added 'transition=Dissolve(2.0) for the smooth fade.

# BACKGROUNDS
image bg classroom1 = ConditionSwitch(
    "current_tier == 'high'", "images/bg/CLASS 1 ( watercolor state).jpeg",
    "current_tier == 'medium'", "images/bg/class 1 neutral state.jpeg",
    "current_tier == 'low'", "images/bg/CLASS 1 ( grey state).jpeg",
    transition=Dissolve(2.0)
)

image bg classroom2 = ConditionSwitch(
    "current_tier == 'high'", "images/bg/CLASS 2 ( watercolor state).jpeg",
    "current_tier == 'medium'", "images/bg/CLASS 2 ( neutral state).jpeg",
    "current_tier == 'low'", "images/bg/CLASS 2 ( grey state).jpeg",
    transition=Dissolve(2.0)
)

image bg walkhome = ConditionSwitch(
    "current_tier == 'high'", "images/bg/WALK HOME(watercolor state).jpeg",
    "current_tier == 'medium'", "images/bg/WALK HOME( neutral state).jpeg",
    "current_tier == 'low'", "images/bg/WALK HOME ( grey state).jpeg",
    transition=Dissolve(2.0)
)

# Static Images
image bg shop = "images/bg/SHOP (grey state ).jpeg"
image bg room = "images/bg/room grey state.jpeg"
image bg school gate = "images/bg/SCHOOL GATE ( grey state).jpeg"

# CHARACTERS
# LIA POSES
image lia fullbody= ConditionSwitch(
    "current_tier == 'high'", "images/fullbody/watercolor state/lia fullbody watercolor.png",
    "current_tier == 'medium'", "images/fullbody/neutral state/lia fullbody neutral.png",
    "current_tier == 'low'", "images/fullbody/grey state/lia fullbody grey.png",
    transition=Dissolve(2.0) 
)

image lia neutral = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/lia/lia neutral face watercolor.png",
    "current_tier == 'medium'", "images/halfbody/neutral state/lia/lia neutral face neutral.png",
    "current_tier == 'low'", "images/halfbody/grey state/lia/lia neutral face grey.png",
    transition=Dissolve(2.0)
)

image lia thinking = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/lia/lia pensive watercolor.png",
    "current_tier == 'medium'", "images/halfbody/neutral state/lia/lia pensive neutral.png",
    "current_tier == 'low'", "images/halfbody/grey state/lia/lia pensive grey.png",
    transition=Dissolve(2.0)
)

image lia sad = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/lia/lia sad watercolor.png",
    "current_tier == 'medium'", "images/halfbody/neutral state/lia/lia sad neutral.png",
    "current_tier == 'low'", "images/halfbody/grey state/lia/lia sad grey.png",
    transition=Dissolve(2.0)
)

image lia smiling = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/lia/lia smiling watercolor.png",
    "current_tier == 'medium'", "images/halfbody/neutral state/lia/lia smiling neutral.png",
    "current_tier == 'low'", "images/halfbody/grey state/lia/lia smiling grey.png",
    transition=Dissolve(2.0)
)

# ANA POSES
image ana fullbody = ConditionSwitch(
    "current_tier == 'high'", "images/fullbody/watercolor state/ana fullbody watercolor.png",
    "current_tier == 'medium'", "images/fullbody/neutral state/ana fullbody neutral.png",
    "current_tier == 'low'", "images/fullbody/grey state/ana fullbody grey.png",
    transition=Dissolve(2.0)
)

image ana frowning = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/ana/ana frowning watercolor .png",
    "current_tier == 'medium'", "images/halfbody/neutral state/ana/ana frowning neutral.png",
    "current_tier == 'low'", "images/halfbody/grey state/ana/ana frowning grey.png",
    transition=Dissolve(2.0)
)

image ana neutral = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/ana/ana neutral face watercolor.png",
    "current_tier == 'medium'", "images/halfbody/neutral state/ana/ana neutral face neutral.png",
    "current_tier == 'low'", "images/halfbody/grey state/ana/ana neutral face grey.png",
    transition=Dissolve(2.0)
)

image ana sad = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/ana/ana sad watercolor.png",
    "current_tier == 'medium'", "images/halfbody/neutral state/ana/ana sad neutral.png",
    "current_tier == 'low'", "images/halfbody/grey state/ana/ana sad grey.png",
    transition=Dissolve(2.0)
)

image ana smiling = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/ana/ana smiling watercolor .png",
    "current_tier == 'medium'", "images/halfbody/neutral state/ana/ana smiling neutral.png",
    "current_tier == 'low'", "images/halfbody/grey state/ana/ana smiling grey.png",
    transition=Dissolve(2.0)
)

# DORIAN POSES
image dorian fullbody = ConditionSwitch(
    "current_tier == 'high'", "images/fullbody/watercolor state/dorian fullbody watercolor.png",
    "current_tier == 'medium'", "images/fullbody/neutral state/dorian fullbody neutral.png",
    "current_tier == 'low'", "images/fullbody/grey state/dorian fullbody grey.png",
    transition=Dissolve(2.0)
)

image dorian frowning = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/dorian/dorian frowning watercolor.png",
    "current_tier == 'medium'", "images/halfbody/neutral state/dorian/dorian frowning neutral.png",
    "current_tier == 'low'", "images/halfbody/grey state/dorian/dorian frowning grey.png",
    transition=Dissolve(2.0)
)

image dorian neutral = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/dorian/dorian neutral face watercolor.png",
    "current_tier == 'medium'", "images/halfbody/neutral state/dorian/dorian neutral face neutral.png",
    "current_tier == 'low'", "images/halfbody/grey state/dorian/dorian neutral face grey.png",
    transition=Dissolve(2.0)
)

image dorian smiling = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/dorian/dorian smiling watercolor .png",
    "current_tier == 'medium'", "images/halfbody/neutral state/dorian/dorian smiling neutral.png",
    "current_tier == 'low'", "images/halfbody/grey state/dorian/dorian smiling grey.png",
    transition=Dissolve(2.0)
)

image dorian smirking = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/dorian/dorian smirking watercolor.png",
    "current_tier == 'medium'", "images/halfbody/neutral state/dorian/dorian smirking neutral.png",
    "current_tier == 'low'", "images/halfbody/grey state/dorian/dorian smirking grey.png",
    transition=Dissolve(2.0)
)

# JACOB POSES
# Note: I matched the extra space in "neutral .png" and the typos "movking" and "javob"
image jacob fullbody = ConditionSwitch(
    "current_tier == 'high'", "images/fullbody/watercolor state/jacob fullbody watercolor.png",
    "current_tier == 'medium'", "images/fullbody/neutral state/jacob fullbody neutral .png",
    "current_tier == 'low'", "images/fullbody/grey state/jacob fullbody grey.png",
    transition=Dissolve(2.0)
)

image jacob frowning = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/jacob/javob frowning watercolor.png",
    "current_tier == 'medium'", "images/halfbody/neutral state/jacob/jacob frowning neutral.png",
    "current_tier == 'low'", "images/halfbody/grey state/jacob/jacob frowning grey.png",
    transition=Dissolve(2.0)
)

image jacob mocking = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/jacob/jacob mocking watercolor.png",
    "current_tier == 'medium'", "images/halfbody/neutral state/jacob/jacob mocking neutral.png",
    "current_tier == 'low'", "images/halfbody/grey state/jacob/jacob movking grey.png",
    transition=Dissolve(2.0)
)

image jacob neutral = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/jacob/jacob neutral face watercolor.png",
    "current_tier == 'medium'", "images/halfbody/neutral state/jacob/jacob neutral face neutral.png",
    "current_tier == 'low'", "images/halfbody/grey state/jacob/jacob neutral face grey.png",
    transition=Dissolve(2.0)
)

image jacob smiling = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/jacob/jacob smiling watercolor.png",
    "current_tier == 'medium'", "images/halfbody/neutral state/jacob/jacob smiling neutral.png",
    "current_tier == 'low'", "images/halfbody/grey state/jacob/jacob smiling grey.png",
    transition=Dissolve(2.0)
)

# MARA POSES
image mara fullbody = ConditionSwitch(
    "current_tier == 'high'", "images/fullbody/watercolor state/mara fullbody watercolor.png",
    "current_tier == 'medium'", "images/fullbody/neutral state/mara fullbody neutral.png",
    "current_tier == 'low'", "images/fullbody/grey state/mara fullbody grey.png",
    transition=Dissolve(2.0)
)

image mara neutral = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/mara/mara neutral face watercolor.png",
    "current_tier == 'medium'", "images/halfbody/neutral state/mara/mara neutral face neutral.png",
    "current_tier == 'low'", "images/halfbody/grey state/mara/mara neutral face grey.png",
    transition=Dissolve(2.0)
)

image mara sad = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/mara/mara sad watercolor.png",
    "current_tier == 'medium'", "images/halfbody/neutral state/mara/mara sad neutral.png",
    "current_tier == 'low'", "images/halfbody/grey state/mara/mara sad grey.png",
    transition=Dissolve(2.0)
)

image mara smiling = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/mara/mara smiling watercolor.png",
    "current_tier == 'medium'", "images/halfbody/neutral state/mara/mara smiling neutral.png",
    "current_tier == 'low'", "images/halfbody/grey state/mara/mara smiling grey.png",
    transition=Dissolve(2.0)
)

# SOFIA POSES
image sofia fullbody = ConditionSwitch(
    "current_tier == 'high'", "images/fullbody/watercolor state/sofia fullbody watercolor.png",
    "current_tier == 'medium'", "images/fullbody/neutral state/sofia fullbody neutral.png",
    "current_tier == 'low'", "images/fullbody/grey state/sofia fullbody grey.png",
    transition=Dissolve(2.0)
)

image sofia neutral = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/sofia/sofia neutral face watercolor.png",
    "current_tier == 'medium'", "images/halfbody/neutral state/sofia/sofia neutral face neutral.png",
    "current_tier == 'low'", "images/halfbody/grey state/sofia/sofia neutral face grey.png",
    transition=Dissolve(2.0)
)

image sofia sad = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/sofia/sofia sad watercolor.png",
    "current_tier == 'medium'", "images/halfbody/neutral state/sofia/sofia sad neutral.png",
    "current_tier == 'low'", "images/halfbody/grey state/sofia/sofia sad grey.png",
    transition=Dissolve(2.0)
)

image sofia smiling = ConditionSwitch(
    "current_tier == 'high'", "images/halfbody/watercolor state/sofia/sofia smiling watercolor.png",
    "current_tier == 'medium'", "images/halfbody/neutral state/sofia/sofia smiling neutral.png",
    "current_tier == 'low'", "images/halfbody/grey state/sofia/sofia smiling grey.png",
    transition=Dissolve(2.0)
)

# LADY AT THE STORE
image shoplady = ConditionSwitch(
    "current_tier == 'high'", "images/doamna de la magazin/watercolor.png",
    "current_tier == 'medium'", "images/doamna de la magazin/neutral.png",
    "current_tier == 'low'", "images/doamna de la magazin/grey.png",
    transition=Dissolve(2.0)
)

# TIMER IMAGES
image quiz_timer_graphic = ConditionSwitch(
    "timer_phase == 0", "images/timer/1.png",
    "timer_phase == 1", "images/timer/2.png",
    "timer_phase == 2", "images/timer/3.png",
    "timer_phase == 3", "images/timer/4.png",
    "timer_phase == 4", "images/timer/5.png",
    "timer_phase == 5", "images/timer/6.png",
    "timer_phase == 6", "images/timer/7.png",
    "timer_phase == 7", "images/timer/8.png",
    "True", "images/timer/9.png",
    transition=Dissolve(2.0)
)

# AUDIO DEFINITIONS FOR QUIZ
define audio.sfx_quiz_correct = "audio/sfx/quiz_correct.mp3"
define audio.sfx_quiz_wrong = "audio/sfx/quiz_wrong.mp3"
define audio.sfx_timer_tick = "audio/sfx/timer_tick.mp3"
define audio.sfx_time_over = "audio/sfx/time_over.mp3"
define audio.sfx_clock_ticking_bg = "audio/sfx/clock_ticking_loop.mp3" # Background loop

# --- QUIZ DATABASE ---
init python:
    # Structure: Subject -> List of Dicts
    quiz_db = {
        "Literature": [
            {
                "q": "Which playwright is famously known as the 'Bard of Avon' and wrote 'Romeo and Juliet'?",
                "options": ["Jane Austen", "Charles Dickens", "Geoffrey Chaucer", "William Shakespeare"],
                "correct": "William Shakespeare",
                "hint": "Think of the most famous author associated with the Globe Theatre.",
                "explanation": "He is widely regarded as the greatest writer in the English language and was born in Stratford-upon-Avon."
            },
            {
                "q": "In the novel 'Pride and Prejudice', who is the female protagonist looking for love and social standing?",
                "options": ["Hester Prynne", "Jane Eyre", "Catherine Earnshaw", "Elizabeth Bennet"],
                "correct": "Elizabeth Bennet",
                "hint": "She has four sisters and a very determined mother.",
                "explanation": "She is the witty and independent lead character whose relationship with Mr. Darcy drives the plot."
            },
            {
                "q": "Which of these is a famous type of poem consisting of 14 lines, often used by Shakespeare?",
                "options": ["Haiku", "Epic", "Limerick", "Sonnet"],
                "correct": "Sonnet",
                "hint": "The name comes from the Italian word 'sonetto', meaning 'little song'.",
                "explanation": "A sonnet is a 14-line poem with a specific rhyme scheme and iambic pentameter meter."
            },
            {
                "q": "In Charles Dickens' 'A Christmas Carol', who is the miserly old man visited by three ghosts?",
                "options": ["Sherlock Holmes", "David Copperfield", "Ebenezer Scrooge", "Oliver Twist"],
                "correct": "Ebenezer Scrooge",
                "hint": "He famously says the phrase 'Bah! Humbug!'",
                "explanation": "His name has become synonymous with a person who is stingy or lacks Christmas spirit."
            },
            {
                "q": "What is the name of the fantasy world created by C.S. Lewis in his famous children's book series?",
                "options": ["Narnia", "Wonderland", "Neverland", "Middle-earth"],
                "correct": "Narnia",
                "hint": "The first book involves a Lion, a Witch, and a Wardrobe.",
                "explanation": "Narnia is the magical land accessed through a wardrobe in the first book of the series."
            }
        ],
        "Math": [
            {
                "q": "What is the name of a polygon that has exactly three sides?",
                "options": ["N-Gon", "Hexagon", "Triangle", "Pentagon"],
                "correct": "Triangle",
                "hint": "The prefix of this word means 'three'.",
                "explanation": "A triangle is defined by its three sides and three internal angles that sum to 180 degrees."
            },
            {
                "q": "What is the result of multiplying any number by zero?",
                "options": ["One", "Infinity", "Zero", "The number itself"],
                "correct": "Zero",
                "hint": "Think about what happens if you have five groups of 'nothing'.",
                "explanation": "The zero property of multiplication states that the product of zero and any number is always zero."
            },
            {
                "q": "In the equation 2x=10, what is the value of x?",
                "options": ["5", "2", "20", "8"],
                "correct": "5",
                "hint": "What number do you need to double to reach ten?",
                "explanation": "Dividing both sides of the equation by 2 isolates the variable, resulting in 10 / 2 = 5."
            },
            {
                "q": "What is the value of a right angle in degrees?",
                "options": ["45°", "90°", "180°", "360°"],
                "correct": "90°",
                "hint": "It is the angle found at the corners of a standard sheet of paper.",
                "explanation": "A right angle is an angle of exactly 90 degrees, forming a square corner."
            },
            {
                "q": "Which of these is the smallest prime number?",
                "options": ["0", "1", "2", "3"],
                "correct": "2",
                "hint": "It is the only prime number that is also an even number.",
                "explanation": "Two is the only even prime number and the smallest number with exactly two factors: 1 and itself."
            }
        ],
        "Physics": [
            {
                "q": "Which of Isaac Newton's laws states that for every action, there is an equal and opposite reaction?",
                "options": ["First Law", "Second Law", "Third Law", "Law of Gravity"],
                "correct": "Third Law",
                "hint": "Think about what happens to your feet when you push against the ground to walk forward.",
                "explanation": "This law describes the interaction between two objects, where the forces they exert on each other are equal and opposite."
            },
            {
                "q": "What is the standard unit of measurement for force in the International System of Units (SI)?",
                "options": ["Joule", "Watt", "Pascal", "Newton"],
                "correct": "Newton",
                "hint": "It shares its name with the scientist who famously studied gravity and motion.",
                "explanation": "Named after Sir Isaac Newton, the Newton (N) is defined as the force needed to accelerate 1 kg of mass at 1 m/s²."
            },
            {
                "q": "Which type of energy is possessed by an object due to its motion?",
                "options": ["Chemical", "Kinetic", "Thermal", "Potential"],
                "correct": "Kinetic",
                "hint": "The word comes from the Greek word 'kinesis', meaning movement.",
                "explanation": "Kinetic energy is the energy of movement, calculated based on an object's mass and the square of its velocity."
            },
            {
                "q": "What force acts between two surfaces that are sliding, or trying to slide, across each other?",
                "options": ["Friction", "Magnetism", "Gravity", "Tension"],
                "correct": "Friction",
                "hint": "This is why your hands get warm when you rub them together quickly.",
                "explanation": "Friction is the resistance to motion of one object moving relative to another."
            },
            {
                "q": "In Physics, what does 'acceleration' specifically measure?",
                "options": ["Amount of matter", "Speed", "Distance", "Rate of change of velocity"],
                "correct": "Rate of change of velocity",
                "hint": "If a car is 'accelerating', it is either speeding up, slowing down, or turning.",
                "explanation": "Acceleration describes how quickly an object's speed or direction changes over time."
            }
        ],
        "Chemistry": [
            {
                "q": "What is the smallest unit of an element that retains all the chemical properties of that element?",
                "options": ["Molecule", "Atom", "Proton", "Cell"],
                "correct": "Atom",
                "hint": "It comes from the Greek word 'atomos', meaning indivisible.",
                "explanation": "An atom consists of a nucleus and electrons and is the basic building block of matter."
            },
            {
                "q": "On the Periodic Table, what does the 'Atomic Number' of an element represent?",
                "options": ["Total weight", "Electron shells", "Neutrons", "Number of protons"],
                "correct": "Number of protons",
                "hint": "One could say it is overwhelmingly positive.",
                "explanation": "The atomic number is unique to each element and defines its identity based on the proton count."
            },
            {
                "q": "Which state of matter has a definite volume but takes the shape of its container?",
                "options": ["Solid", "Liquid", "Gas", "Plasma"],
                "correct": "Liquid",
                "hint": "Many consider jokingly that cats are in this state.",
                "explanation": "Particles in a liquid are close together but can move past one another, allowing the substance to flow."
            },
            {
                "q": "What is the pH value of pure water, which is considered neutral?",
                "options": ["1", "14", "7", "0"],
                "correct": "7",
                "hint": "The pH scale goes from 1 as most acidic all the way to 14 as most alkaline.",
                "explanation": "The pH scale ranges from 0 to 14, with 7 being the neutral midpoint."
            },
            {
                "q": "What is the chemical symbol for the element Gold?",
                "options": ["Fe", "Au", "Ag", "Gd"],
                "correct": "Au",
                "hint": "One could think of pain as it starts all the same.",
                "explanation": "The symbol 'Au' comes from 'aurum', the Latin word for gold."
            }
        ],
        "Geography": [
            {
                "q": "Which imaginary lines on a map run east and west and measure distance north or south of the Equator?",
                "options": ["Prime Meridian", "Date Line", "Longitude", "Latitude"],
                "correct": "Latitude",
                "hint": "Think of these lines like the rungs of a 'ladder' climbing up or down the globe.",
                "explanation": "Latitude lines are parallel circles that wrap around the Earth, with the Equator at 0°."
            },
            {
                "q": "What is the name of the supercontinent that existed roughly 335 million years ago?",
                "options": ["Atlantis", "Pangaea", "Eurasia", "Gondwana"],
                "correct": "Pangaea",
                "hint": "The name comes from Greek words meaning 'all lands'.",
                "explanation": "Pangaea was a massive landmass that incorporated almost all of Earth's land area."
            },
            {
                "q": "Which of Earth's layers is composed mostly of liquid iron and nickel and creates the magnetic field?",
                "options": ["Mantle", "Inner Core", "Crust", "Outer Core"],
                "correct": "Outer Core",
                "hint": "The mantle is the thickest layer of Earth, composed of semi-solid rock.",
                "explanation": "The Outer Core is a fluid layer about 2,200 km thick; its movement generates Earth's magnetosphere."
            },
            {
                "q": "What is the process where water vapor cools and changes back into liquid water droplets?",
                "options": ["Evaporation", "Condensation", "Precipitation", "Transpiration"],
                "correct": "Condensation",
                "hint": "You see this same process when 'steam' from a hot shower turns into water on a cold mirror.",
                "explanation": "Condensation is the phase change from gas to liquid, a critical step in cloud formation."
            },
            {
                "q": "Which type of map is designed to show the elevation and shape of the land?",
                "options": ["Topographic", "Road", "Thematic", "Political"],
                "correct": "Topographic",
                "hint": "Hikers and engineers use these maps to understand how steep a hill or mountain is.",
                "explanation": "Topographic maps use contour lines to represent the three-dimensional landscape."
            }
        ],
        "History": [
            {
                "q": "Which ancient civilization is credited with building the Great Pyramids of Giza?",
                "options": ["Egyptians", "Aztecs", "Mesopotamians", "Romans"],
                "correct": "Egyptians",
                "hint": "This civilization flourished along the banks of the Nile River.",
                "explanation": "The pyramids were constructed during the Old and Middle Kingdoms as monumental tombs."
            },
            {
                "q": "Who was the primary author of the American Declaration of Independence in 1776?",
                "options": ["Benjamin Franklin", "George Washington", "Thomas Jefferson", "Abraham Lincoln"],
                "correct": "Thomas Jefferson",
                "hint": "Lincoln was the 16th president and lived nearly a century later.",
                "explanation": "Jefferson was chosen to draft the document, which outlined the colonies' grievances."
            },
            {
                "q": "The 'French Revolution' began in 1789 with the storming of which famous prison?",
                "options": ["Tower of London", "Robben Island", "Alcatraz", "The Bastille"],
                "correct": "The Bastille",
                "hint": "The name of this fortress is now synonymous with the start of the Revolution.",
                "explanation": "The storming of the Bastille symbolized the uprising against the absolute monarchy."
            },
            {
                "q": "Which global conflict, lasting from 1914 to 1918, was originally known as 'The Great War'?",
                "options": ["Cold War", "Vietnam War", "Napoleonic Wars", "World War I"],
                "correct": "World War I",
                "hint": "This war was characterized by trench warfare in Europe.",
                "explanation": "It was called the Great War because of its unprecedented scale until World War II."
            },
            {
                "q": "In World War II what were the great opposing powers called?",
                "options": ["Nazis & Americans", "Russians & Fascists", "Antanta & Axis", "Axis & Allied Powers"],
                "correct": "Axis & Allied Powers",
                "hint": "The remaining great powers had to gather and negotiate a pact in order to resist.",
                "explanation": "This war was characterized by worldwide incursions and multiple operations theatres."
            }
        ],
        "Arts": [
            {
                "q": "The 'Renaissance' was a period of cultural rebirth that began in which European country?",
                "options": ["Germany", "England", "Italy", "France"],
                "correct": "Italy",
                "hint": "Think of the country where Leonardo da Vinci and Michelangelo lived.",
                "explanation": "The Renaissance began in Italian city-states like Florence due to their wealth and history."
            },
            {
                "q": "Which is the Famous composer that wrote the Requiem?",
                "options": ["Bach", "Mozart", "Vivaldi", "Beethoven"],
                "correct": "Mozart",
                "hint": "Many called him a child prodigy.",
                "explanation": "Mozart composed the Requiem as his final piece."
            },
            {
                "q": "Which Italian Renaissance artist painted the ceiling of the Sistine Chapel?",
                "options": ["Donatello", "Leonardo da Vinci", "Raphael", "Michelangelo"],
                "correct": "Michelangelo",
                "hint": "He also sculpted the famous marble 'David' in Florence.",
                "explanation": "He spent four years painting the complex biblical scenes, including the 'Creation of Adam'."
            },
            {
                "q": "Which art movement is characterized by small, thin brushstrokes and emphasis on light?",
                "options": ["Cubism", "Baroque", "Impressionism", "Surrealism"],
                "correct": "Impressionism",
                "hint": "Claude Monet is often considered the father of this movement.",
                "explanation": "This movement focused on capturing the 'impression' of a moment and shifting light."
            },
            {
                "q": "The Taj Mahal, a renowned example of Mughal architecture, is located in which country?",
                "options": ["Pakistan", "Turkey", "Iran", "India"],
                "correct": "India",
                "hint": "It is located in the city of Agra, near the Yamuna River.",
                "explanation": "It was built in Agra by Emperor Shah Jahan as a tomb for his favorite wife."
            }
        ]
    }

    def restore_game_music():
        """
        Forces the background music to restart based on the current tier.
        Call this after a minigame or quiz stops the music.
        """
        # 1. Reset the 'memory' of the last tier so the system thinks it's a new change
        store.last_music_tier = None
        
        # 2. Trigger the standard visual/music update to play the correct track
        update_visual_state()