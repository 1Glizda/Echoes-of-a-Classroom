
# --- 1. THE LOGIC CONTROLLER ---
default current_quiz_number = 1

label run_post_quiz_logic:
    # 1. Define everyone who is present
    $ available_chars = ['lia', 'dorian', 'ana', 'mara', 'jacob', 'sofia']
    
    # 2. Shuffle the list so the forced dialogues are random
    $ renpy.random.shuffle(available_chars)
    
    # 3. FORCE DIALOGUE 1 (Pop a character from the list)
    $ char1 = available_chars.pop()
    call expression "interact_" + char1 from _call_expression_1
    
    # 4. FORCE DIALOGUE 2
    $ char2 = available_chars.pop()
    call expression "interact_" + char2 from _call_expression_2

    # 5. FREE ROAM LOOP
    label .classroom_loop:
        # Show the screen with whoever is left in the list
        call screen classroom_selector(available_chars)
        
        $ result = _return

        if result == "next_scene":
            return # Exit the loop and continue the story
        
        else:
            # Talk to the chosen character
            call expression "interact_" + result from _call_expression_3
            
            # Remove them from the list so we don't talk to them again (optional)
            # If you WANT to talk to them again, remove the next line.
            $ if result in available_chars: available_chars.remove(result)
            
            jump .classroom_loop


# --- 2. CHARACTERS ---
define player = Character("The Protagonist")
define lia = Character("Lia")
define dorian = Character("Dorian")
define ana = Character("Ana")
define mara = Character("Mrs. Mara")
define jacob = Character("Jacob")
define sofia = Character("Miss Sofia")
define shoplady = Character("Shop Lady")

# ==========================================
# === 3. ACTUAL GAME LOOP ===
# ==========================================
label start:
    # Initialize Visuals & Music at the start
    $ update_visual_state()
    show screen status_hud
    
    # [cite: 53-58] Introduction
    scene bg room
    player "Another morning. Another day I'm supposed to learn something... but lately I'm feeling I'm not learning anything at all."
    "{i}Some days feel darker than others. Maybe today I'll change that... or make it worse.{/i}"

    # [cite: 59-61] Commute
    scene bg walkhome with dissolve
    player "I don't even know what to expect from this school year. Everything feels bigger than me."
    player "Teachers, classmates... it's like they can shape me before I even sit in a classroom, can I even handle everything all at once?"
    player "I hope I make the right choices... somehow. I don't want to mess up and let someone else's bad words stick to my head forever."

    scene bg school gate with dissolve
    player "Here goes nothing."

    # ==========================================
    # === QUIZ 1: LITERATURE ===
    # ==========================================
    $ current_quiz_number = 1
    scene bg classroom1 with dissolve
    
    "The first period starts. Mrs. Mara places the Literature quiz on your desk."
    
    # Calls the Literature quiz (Question index 0)
    call start_quiz("Literature")
    
    "The first quiz ends."
    call run_post_quiz_logic

    # ==========================================
    # === QUIZ 2: MATH ===
    # ==========================================
    $ current_quiz_number = 2
    scene bg classroom2 with dissolve
    
    "You move to the next class. Jacob is writing equations on the board."
    
    # Calls the Math quiz (Question index 0)
    call start_quiz("Math")

    "The second quiz ends."
    call run_post_quiz_logic

    # --- ENVIRONMENTAL BREAK 1 ---
    scene bg school gate with dissolve
    # [cite: 251-261]
    player "Funny how stepping outside doesn't really clear my mind. It's like I can still hear everyone's voices in my head."
    player "Teachers, classmates, everyone is tugging me in different directions."
    player "It hits me sometimes... I spend more hours with these people than my own family. They're basically raising me, since fifth grade, whether they mean or not."
    player "Mrs. Mara makes me feel like I'm worth slowing down for. Jacob makes me feel small without even trying."
    player "Lia gives me hope, Dorian gives me doubts... and I'm just trying to figure out whose words to actually trust."
    player "It's scary how easy it is to change who you are just because someone else tells you who they think you are."
    player "Am I actually growing or just getting changed by whatever environment I happen to be in?"

    # ==========================================
    # === QUIZ 3: PHYSICS ===
    # ==========================================
    $ current_quiz_number = 3
    scene bg classroom1 with dissolve
    
    "Back inside. The Physics test is waiting."
    
    # Calls the Physics quiz (Question index 0)
    call start_quiz("Physics")

    "The third quiz ends."
    call run_post_quiz_logic

    # ==========================================
    # === QUIZ 4: CHEMISTRY ===
    # ==========================================
    $ current_quiz_number = 4
    scene bg classroom2 with dissolve
    
    "The air smells faintly of chemicals. It's time for the next subject."
    
    # Calls the Chemistry quiz (Question index 0)
    call start_quiz("Chemistry")

    "The fourth quiz ends."
    call run_post_quiz_logic

    # --- ENVIRONMENTAL BREAK 2: GROCERY STORE ---
    scene bg shop with dissolve
    # [cite: 462-471]
    player "Why does everyone at school feel like they're carving pieces into me?"
    player "Lia trying to lift me up, Dorian pushing me down, Ana trying to tune my brain like it's homework, and the teachers... God, the teachers."
    player "I spend more time with them than with my own parents, no wonder their voices echo in my brain all the time.."
    player "It feels like every quiz rewrites how people see me. Maybe that's the part that scares me, the idea that who I am depends on who is talking to me."
    player "And even worse, I feel like I can't stop but copy the people around me. When someone's kind, I feel myself softening. When someone's harsh, I snap back without thinking."
    player "It's like I'm wired to mirror whatever I'm given. Whatever, I just need to eat before my thoughts start eating me alive."

    show shoplady at center with dissolve
    # [cite: 472-479]
    shoplady "Busy day at school? I can always tell by you kids coming in here walking like you carry bricks in your backpacks."
    menu:
        "Yeah... something like that.":
            pass
        "Guess school gets heavier the older you get.":
            pass
    shoplady "Well... whatever kind of day it was, don't forget to eat something. Brains run weird when the rest of you is running on fumes."
    hide shoplady

    # ==========================================
    # === QUIZ 5: GEOGRAPHY ===
    # ==========================================
    $ current_quiz_number = 5
    scene bg classroom1 with dissolve
    
    "You return for the afternoon sessions. A map is pulled down over the board."
    
    # Calls the Geography quiz (Question index 0)
    call start_quiz("Geography")

    "The fifth quiz ends."
    call run_post_quiz_logic

    # ==========================================
    # === QUIZ 6: HISTORY ===
    # ==========================================
    $ current_quiz_number = 6
    scene bg classroom2 with dissolve
    
    "Miss Sofia looks at the class with a gentle expression before starting the History test."
    
    # Calls the History quiz (Question index 0)
    call start_quiz("History")

    "The sixth quiz ends."
    call run_post_quiz_logic

    # ==========================================
    # === QUIZ 7: ARTS ===
    # ==========================================
    $ current_quiz_number = 7
    scene bg classroom1 with dissolve
    
    "The final subject of the day. You try to focus one last time."
    
    # Calls the Arts quiz (Question index 0)
    call start_quiz("Arts")

    "The seventh quiz ends."
    call run_post_quiz_logic

    # --- ENDINGS ---
    #
    if current_tier == "high":
        jump good_ending
    elif current_tier == "medium":
        jump neutral_ending
    else:
        jump bad_ending

# ENDING LABELS
label good_ending:
    # [cite: 784-796]
    scene bg walkhome with dissolve
    player "I'm tired, but not the kind of tired that makes you feel empty."
    player "It feels heavy, like I've been carrying things I couldn't find in the textbooks. Some teachers made me feel small. Other made space for me to grow."
    player "I think about how easily I believed the loudest voices and how hard it is sometimes to believe kindness."
    player "How much power adults have when you're still becoming someone and you are trying to fit in."
    player "School taught me how to answer questions. But it also taught me how silence feels when someone listens."
    player "I really don't feel strong all the time. But I know kindness isn't weakness. And I don't want to become someone who forgets that."
    
    scene black with fade
    centered "PSA:\nSupportive teachers can significantly improve students' mental health, confidence, and long-term outcomes.\n\nNot everything that matters can be graded."
    return

label neutral_ending:
    # [cite: 797-807]
    scene bg walkhome with dissolve
    player "I'm finally walking home from school and everything feels... muted."
    player "Like I learned how to get through days without really touching them. Some teachers helped. Some hurt."
    player "Most just followed the rules and went home. I did what I had to do to stay afloat. Answered right. Stayed quiet. Didn't cause problems. I learned how to blend in."
    player "I don't know if that's growth or just adaptation. Maybe school doesn't actually change you. Maybe it just teaches you how to endure."

    scene black with fade
    centered "PSA:\nTeenagers and children often adapt to harmful environments instead of getting away from them.\n\nSurvival shouldn't be the goal of education."
    return

label bad_ending:
    # [cite: 808-819]
    scene bg walkhome with dissolve
    player "I keep hearing their voices even now. Telling me I'm slow. Telling me I'm weak."
    player "Telling me I'll never be enough. I believed them because it's easier than fighting back."
    player "They are adults and I'm just their student. I'm scared they might lower my grades even more if I say something wrong."
    player "When you are a kid, adults sound like the truth. School didn't test me. It reshaped me. Made me quieter. Harder. Meaner to myself."
    player "I learned how power works by watching it be used against me. And I hate how familiar it feels."
    player "I don't know who I would've been if someone stopped sooner."

    scene black with fade
    centered "PSA:\nNegative teacher behavior is linked to long-term loss of confidence, academic disengagement, and prolonged mental health issues.\n\nChildren and teenagers absorb more than we think."
    return

# ==========================================
# === CHARACTER INTERACTION LABELS ===
# ==========================================

label interact_lia:
    # Set initial mood based on tier
    if current_tier == "high":
        show lia smiling at center with dissolve
    elif current_tier == "low":
        show lia sad at center with dissolve
    else:
        show lia neutral at center with dissolve
    
    if current_quiz_number == 1:
        if current_tier == "high":
            lia "Hey, you looked really confident today. Honestly, it kinda made me smile. Good job!"
            menu:
                "Really? Guess I'm finally getting the hang of things.":
                    $ change_stat("positiveness", 2)
                "Thanks, Lia. That actually means more than you think.":
                    show lia thinking with dissolve
                    $ change_stat("confidence", 2)
        elif current_tier == "medium":
            lia "I think you did alright! Not perfect, but definitely not bad!"
            menu:
                "Yeah, I guess it wasn't the worst.":
                    $ change_stat("positiveness", 0)
        else:
            lia "Hey... don't beat yourself up, okay? Everyone has rocky starts."
            menu:
                "Thanks... you're really kind about this.":
                    show lia thinking with dissolve
                    $ change_stat("positiveness", 2)
                "Forget it. I always mess up.":
                    $ change_stat("confidence", -2)

    elif current_quiz_number == 2:
        if current_tier == "high":
            lia "You nailed that one! I knew you had it in you."
            menu:
                "Thanks! I actually feel better about this quiz.":
                    $ change_stat("confidence", 2)
                "Yeah... I'm glad I didn't mess up completely.":
                    show lia thinking with dissolve
                    $ change_stat("confidence", -2)
        elif current_tier == "medium":
            lia "Not bad at all! Maybe next time you'll do even better!"
            menu:
                "I hope so...":
                    pass
        else:
            lia "Hey... I see you looking all worried. It was rough but I'm sure you'll get it next time."
            menu:
                "I hope so...":
                    show lia thinking with dissolve
                    $ change_stat("confidence", 2)
                "I hate feeling so slow.":
                    $ change_stat("confidence", -2)

    elif current_quiz_number == 3:
        if current_tier == "high":
            lia "I could feel this bright energy from you today. Like you didn't let the quiz mess with your head. You are doing so good!"
            menu:
                "I'm starting to figure myself out, I think.":
                    $ change_stat("positiveness", 2)
                "Guess today was just... a good day.":
                    show lia thinking with dissolve
        elif current_tier == "medium":
            show lia thinking at center with dissolve
            lia "You look a little tired but I feel like you're keeping yourself together. Did you do okay on this quiz?"
            menu:
                "It was alright, not great but not terrible.":
                    show lia neutral with dissolve
                "Honestly, I'm glad it's over.":
                    pass
        else:
            lia "Hey... you okay? You've been quieter than usual. It's like each quiz pulls you a bit further away. Don't let people mess with your head."
            menu:
                "I'm trying... it just feels like people are pulling at me if I'm not careful enough.":
                    show lia thinking with dissolve
                    $ change_stat("positiveness", 1)
                "Forget it.":
                    $ change_stat("positiveness", -2)

    elif current_quiz_number == 4:
        if current_tier == "high":
            show lia thinking at center with dissolve
            lia "I looked in your direction during the quiz and you seemed so focused I almost forgot we were in the same room. Honestly... you're kind of intimidating when you're like that."
            menu:
                "Haha, guess I'm finally finding my rhythm.":
                    show lia smiling with dissolve
                    $ change_stat("confidence", 2)
                "It felt good being in control for once.":
                    pass
        elif current_tier == "medium":
            show lia thinking at center with dissolve
            lia "I've been trying to read your face since turning in the exam. You look... unsettled? Or maybe just tired?"
            menu:
                "A bit of both.":
                    pass
                "I'm just processing things.":
                    $ change_stat("positiveness", 1)
        else:
            lia "You walked out of the exam like you are carrying a battle inside of you. Did this quiz really hit that hard?"
            menu:
                "Yeah... I felt like everything slipped away from me.":
                    show lia thinking with dissolve
                    $ change_stat("confidence", -2)
                "It was too much today.":
                    pass

    elif current_quiz_number == 5:
        if current_tier == "high":
            show lia thinking at center with dissolve
            lia "You're changing. Not in a bad way, just... stronger. Just remember to not lose your soft, kind parts too."
            menu:
                "I'm trying not to.":
                    show lia smiling with dissolve
                    $ change_stat("confidence", 2)
                "Sometimes being soft hurts.":
                    pass
        elif current_tier == "medium":
            lia "I could tell during the exam that you were tense, but... you didn't stop. That counts for something, right?"
            menu:
                "I guess it does.":
                    show lia smiling with dissolve
                    $ change_stat("positiveness", 2)
                "I'm just tired of counting losses.":
                    show lia thinking with dissolve
                    $ change_stat("positiveness", -2)
        else:
            lia "You didn't even look up when the quiz ended... Are you okay?"
            menu:
                "Yes... I just need some time to process all those quizzes... they are a lot.":
                    show lia thinking with dissolve
                    $ change_stat("positiveness", 2)
                "I don't really know anymore.":
                    $ change_stat("positiveness", -2)

    elif current_quiz_number == 6:
        if current_tier == "high":
            lia "You see things differently now. I like that. I just hope it doesn't cost you too much."
            menu:
                "I hope so too.":
                    $ change_stat("confidence", 2)
                "Sometimes it already has.":
                    show lia thinking with dissolve
                    $ change_stat("confidence", -2)
        elif current_tier == "medium":
            show lia thinking at center with dissolve
            lia "You didn't really look relieved when it ended. Just...thoughtful."
            menu:
                "I'm tired of being measured wrong.":
                    $ change_stat("positiveness", -2)
                "I think I'm changing.":
                    pass
        else:
            show lia thinking at center with dissolve
            lia "I think you are starting to learn things that don't fit into the school agenda anymore. Maybe that scared the school."
            menu:
                "Then maybe I don't fit into this school either.":
                    $ change_stat("positiveness", -2)
                "Maybe that's the problem.":
                    $ change_stat("confidence", 1)

    elif current_quiz_number == 7:
        if current_tier == "high":
            lia "You didn't come out untouched, but you came out aware. That's what matters."
            menu:
                "I won't forget.":
                    $ change_stat("confidence", 2)
                "I don't want to repeat it.":
                    pass
        elif current_tier == "medium":
            show lia thinking at center with dissolve
            lia "We survived the same school... but it feels like we lived in different versions of it."
            menu:
                "I saw parts of it I can't unsee.":
                    show lia sad with dissolve
                    $ change_stat("positiveness", -2)
                "I don't know which version was real anymore.":
                    pass
        else:
            show lia thinking at center with dissolve
            lia "You know what? I don't think this place ever tried to understand you. And I hate that it worked."
            menu:
                "Maybe I wasn't meant to be understood.":
                    show lia sad with dissolve
                    $ change_stat("confidence", -2)
                "It changed me.":
                    pass

    pause 0.8
    hide lia with dissolve
    return

# ------------------------------------------

label interact_dorian:
    if current_tier == "high":
        show dorian smirking at center with dissolve
    elif current_tier == "low":
        show dorian frowning at center with dissolve
    else:
        show dorian neutral at center with dissolve

    if current_quiz_number == 1:
        if current_tier == "high":
            dorian "You didn't mess up? Wasn't expecting that from you."
            menu:
                "Surprise. I do have a brain.":
                    $ change_stat("confidence", 2)
                "Relax man, it's just a quiz.":
                    pass
        elif current_tier == "medium":
            dorian "I mean... at least you didn't embarrass yourself."
            menu:
                "That's the least I could do, I guess.":
                    show dorian smirking with dissolve
                    $ change_stat("positiveness", -2)
                "You really are obsessed with me failing, aren't you?":
                    show dorian frowning with dissolve
                    $ change_stat("confidence", 2)
        else:
            dorian "Rough day, huh? You look even worse than you feel."
            menu:
                "I think I might feel even worse than I look, trust me.":
                    $ change_stat("confidence", -2)
                "Can you not? I already feel bad enough.":
                    $ change_stat("positiveness", 2)

    elif current_quiz_number == 2:
        if current_tier == "high":
            dorian "I'm surprised you got some of these right. Not bad."
            menu:
                "I surprised myself too.":
                    $ change_stat("confidence", 2)
                "Guess I'm only getting better.":
                    show dorian smiling with dissolve
                    $ change_stat("confidence", 2)
        elif current_tier == "medium":
            dorian "I think you did fine, I guess. A few parts were tough but you handled them.. somehow."
            menu:
                "Yeah, could've been worse.":
                    pass
        else:
            dorian "Seriously? You really need to step up. That was so bad."
            menu:
                "...I'll do better next time.":
                    show dorian smirking with dissolve
                    $ change_stat("confidence", -2)
                "I hate that I can never keep it up with everyone.":
                    $ change_stat("confidence", -3)

    elif current_quiz_number == 3:
        if current_tier == "high":
            dorian "Oh look. Someone thinks they're on a winning streak. Relax, one decent quiz doesn't make you gifted."
            menu:
                "Maybe not, but it's a start.":
                    $ change_stat("confidence", 2)
                "Whatever, man.":
                    show dorian frowning with dissolve
        elif current_tier == "medium":
            dorian "You don't look like a disaster. That's new. Did you guess well or something?"
            menu:
                "Some questions made sense I guess.":
                    show dorian smirking with dissolve
                    $ change_stat("confidence", -2)
                "I'm not discussing my strategy with you.":
                    show dorian frowning with dissolve
                    $ change_stat("confidence", 1)
        else:
            show dorian smirking at center with dissolve
            dorian "This quiz ate you alive, huh? You walked out like someone who forgot the alphabet."
            menu:
                "...Can you not?":
                    $ change_stat("confidence", -2)
                "Yeah, I didn't do great.":
                    $ change_stat("confidence", -2)

    elif current_quiz_number == 4:
        if current_tier == "high":
            dorian "Oh look at you, walking out like you own the place. Relax, one quiz doesn't make you a genius."
            menu:
                "You keep saying that, but my grades don't.":
                    show dorian frowning with dissolve
                    $ change_stat("confidence", 2)
                "Believe what you want.":
                    pass
        elif current_tier == "medium":
            dorian "You're not melting into the floor this time, so I guess that's progress. Barely."
            menu:
                "I did alright.":
                    $ change_stat("positiveness", -1)
                "You really enjoy this, don't you?":
                    show dorian smirking with dissolve
                    $ change_stat("positiveness", -1)
        else:
            show dorian smirking at center with dissolve
            dorian "Wow. You came out looking like this quiz personally attacked you. Did you even open the book to study?"
            menu:
                "I tried, okay?":
                    $ change_stat("confidence", -2)
                "Can you not do this today?":
                    $ change_stat("positiveness", -2)

    elif current_quiz_number == 5:
        if current_tier == "high":
            dorian "Don't tell me you think you did well. This school eats people like you."
            menu:
                "Maybe. But I'm still standing.":
                    show dorian frowning with dissolve
                    $ change_stat("confidence", 1)
                "Say whatever you want.":
                    pass
        elif current_tier == "medium":
            dorian "You don't look destroyed. Guess you got lucky again."
            menu:
                "Luck runs out eventually.":
                    pass
                "You really hate seeing me okay.":
                    show dorian smirking with dissolve
                    $ change_stat("positiveness", -2)
        else:
            show dorian smirking at center with dissolve
            dorian "Yikes. This quiz really messed you up, huh? That's what happens when you pretend you can keep up with the others."
            menu:
                "...Just leave me alone.":
                    $ change_stat("confidence", -2)
                "Maybe you're right.":
                    $ change_stat("confidence", -2)

    elif current_quiz_number == 6:
        if current_tier == "high":
            dorian "Careful. People who question the teachers usually lose to them."
            menu:
                "At least I know what I'm losing.":
                    $ change_stat("confidence", 1)
                "I'm not trying to win.":
                    pass
        elif current_tier == "medium":
            dorian "You think too much or you don't think at all. That's why people like you struggle here."
            menu:
                "Thinking shouldn't be a weakness.":
                    show dorian frowning with dissolve
                    $ change_stat("confidence", 2)
                "Maybe you're right.":
                    show dorian smirking with dissolve
                    $ change_stat("confidence", -2)
        else:
            show dorian smirking at center with dissolve
            dorian "This quiz proves it. The system works. Some people rise, some people... don't."
            menu:
                "I guess I'm one of the ones who don't then.":
                    $ change_stat("confidence", -2)
                "Or maybe it's broken.":
                    show dorian frowning with dissolve
                    $ change_stat("confidence", -1)

    elif current_quiz_number == 7:
        if current_tier == "high":
            dorian "Don't turn this into a sob story. Life isn't equal."
            menu:
                "That doesn't mean it should be cruel.":
                    show dorian frowning with dissolve
                    $ change_stat("confidence", 1)
                "I know.":
                    pass
        elif current_tier == "medium":
            dorian "Some of us learned how to play the game. Some of us complained."
            menu:
                "Not everyone starts with the same rules.":
                    pass
                "Maybe I should have tried harder...":
                    show dorian smirking with dissolve
                    $ change_stat("confidence", -2)
        else:
            show dorian smirking at center with dissolve
            dorian "See? In the end, the system sorts everyone out. It always does."
            menu:
                "I guess it sorted me too.":
                    $ change_stat("confidence", -2)
                "Or it just labeled me.":
                    pass

    pause 0.8
    hide dorian with dissolve
    return

# ------------------------------------------

label interact_ana:
    if current_tier == "high":
        show ana smiling at center with dissolve
    elif current_tier == "low":
        show ana frowning at center with dissolve
    else:
        show ana neutral at center with dissolve

    if current_quiz_number == 1:
        if current_tier == "high":
            ana "You got the trick question right, didn't you? I can tell by the look on your face!"
            menu:
                "Yes! Want me to walk you through them?":
                    $ change_stat("confidence", 2)
                "Maybe we can study together sometime.":
                    $ change_stat("positiveness", 2)
        elif current_tier == "medium":
            ana "You did okay. Some questions were really tough."
            menu:
                "True... I hesitated too much.":
                    $ change_stat("smart", 2)
                "I'll work on it next time.":
                    pass
        else:
            show ana sad at center with dissolve
            ana "I noticed you struggle on the quiz... want help next time?"
            menu:
                "That would be... cool. Thanks.":
                    show ana smiling with dissolve
                    $ change_stat("smart", 2)
                "Forget it. I don't need your pity.":
                    show ana frowning with dissolve
                    $ change_stat("positiveness", -2)

    elif current_quiz_number == 2:
        if current_tier == "high":
            ana "This quiz was so tricky! If you want, I can explain how I solved mine. It might help you next time."
            menu:
                "Sure, that would help a lot! Thanks!":
                    $ change_stat("smart", 2)
                "I can also share some ways I approached the quiz.":
                    $ change_stat("positiveness", 2)
        elif current_tier == "medium":
            ana "Some questions were tricky... but I'm sure you managed well overall. Not bad!"
            menu:
                "Yeah... tricky... I think I got most of it.":
                    pass
                "I could've gone worse, honestly.":
                    pass
        else:
            show ana sad at center with dissolve
            ana "It's alright... everyone has quizzes like this sometimes. Don't feel too bad."
            menu:
                "Thanks, I just need to focus more.":
                    $ change_stat("positiveness", 2)
                "I hate so much falling behind.":
                    $ change_stat("confidence", -2)

    elif current_quiz_number == 3:
        if current_tier == "high":
            ana "You seem composed. If your reasoning matches the way you look, I suppose you did well."
            menu:
                "I think my answers were solid.":
                    $ change_stat("confidence", 2)
                "Let's hope the grading agrees.":
                    pass
        elif current_tier == "medium":
            ana "Alright... this quiz had a weird difficulty curve. How'd you feel about it?"
            menu:
                "Some parts were okay.":
                    pass
                "It felt uneven.":
                    $ change_stat("smart", 2)
        else:
            show ana frowning at center with dissolve
            ana "You finished the quiz too fast, I can tell. This quiz punishes anyone who isn't pacing themselves."
            menu:
                "I know. I panicked.":
                    $ change_stat("confidence", -2)
                "I'll do better next time.":
                    pass

    elif current_quiz_number == 4:
        if current_tier == "high":
            ana "I believe this time you moved through the questions methodically. You are starting to look like someone who thinks every move."
            menu:
                "I tried to stay organized.":
                    $ change_stat("confidence", 2)
                "I hope it pays off.":
                    pass
        elif current_tier == "medium":
            ana "This quiz had a predictable structure. Did you notice the pattern between questions 2 and 5?"
            menu:
                "Kind of? I wasn't sure.":
                    $ change_stat("smart", 1)
                "I missed it completely.":
                    show ana frowning with dissolve
                    pass
        else:
            show ana frowning at center with dissolve
            ana "You panicked. I saw it. I bet you even jumped questions. Those quizzes punish that kind of rushing."
            menu:
                "I couldn't think straight.":
                    $ change_stat("confidence", -2)
                "I'll try to slow down next time.":
                    $ change_stat("confidence", 2)

    elif current_quiz_number == 5:
        if current_tier == "high":
            ana "I bet you did good this time. You looked like you adapted quickly. That's not common. Just don't let emotions slow you down."
            menu:
                "I'll try.":
                    pass
                "Emotions are a part of thinking.":
                    $ change_stat("confidence", 2)
        elif current_tier == "medium":
            ana "This quiz was harsh but fair. If you missed questions, it's a knowledge gap, not bad luck."
            menu:
                "That makes sense. I did bad on this quiz.":
                    show ana sad with dissolve
                    $ change_stat("confidence", -2)
                "It still felt overwhelming.":
                    pass
        else:
            show ana frowning at center with dissolve
            ana "You froze on at least three questions! I noticed. You need a better strategy."
            menu:
                "I panicked.":
                    $ change_stat("confidence", -2)
                "I didn't know what to prioritize but it wasn't the worst.":
                    $ change_stat("confidence", 1)

    elif current_quiz_number == 6:
        if current_tier == "high":
            ana "I think you might reason differently. If grades mattered less, you'd probably shine even more."
            menu:
                "Thank you, that means more than a score.":
                    $ change_stat("confidence", 2)
                "Too bad grades decide everything.":
                    show ana sad with dissolve
                    $ change_stat("positiveness", -2)
        elif current_tier == "medium":
            ana "I don't know... I think I'm starting to doubt myself. It starts to feel like we're trained to optimize answers, not to understand."
            menu:
                "That explains a lot.":
                    pass
                "Understanding takes time but we are hurried all the time.":
                    $ change_stat("confidence", 1)
        else:
            show ana frowning at center with dissolve
            ana "This quiz didn't measure my effort! Only my capacity of memorizing random knowledge. That's... frustrating."
            menu:
                "Effort never counts.":
                    $ change_stat("positiveness", -2)
                "Then what's the point?":
                    pass

    elif current_quiz_number == 7:
        if current_tier == "high":
            ana "I used to think effort equals outcome. I don't anymore."
            menu:
                "I think that... changes everything.":
                    $ change_stat("positiveness", 1)
                "It changes nothing here.":
                    pass
        elif current_tier == "medium":
            ana "We pretend grades are subjective. They aren't. They never were."
            menu:
                "Why don't we talk about that more?":
                    pass
                "Because it's easier to pretend.":
                    $ change_stat("confidence", 1)
        else:
            show ana sad at center with dissolve
            ana "This quiz rewards consistency... but not everyone has the same conditions to be consistent."
            menu:
                "Some students have it harder than others...":
                    pass
                "It's just not fair.":
                    $ change_stat("positiveness", -2)

    pause 0.8
    hide ana with dissolve
    return

# ------------------------------------------

label interact_mara:
    if current_tier == "high":
        show mara smiling at center with dissolve
    elif current_tier == "low":
        show mara sad at center with dissolve
    else:
        show mara neutral at center with dissolve
    
    if current_quiz_number == 1:
        if current_tier == "high":
            mara "You handled this quiz with grace. You really should start recognizing that."
            menu:
                "I think I'm finally starting to improve.":
                    $ change_stat("confidence", 2)
                "Thanks for noticing! I'm really trying.":
                    $ change_stat("positiveness", 2)
        elif current_tier == "medium":
            mara "You did fairly well. I'm glad you are trying."
            menu:
                "I'm trying... really.":
                    $ change_stat("positiveness", 2)
        else:
            mara "You look very overwhelmed today. That's okay. Learning is sometimes messy."
            menu:
                "It's just... I don't want to disappoint people.":
                    pass
                "I hate feeling slow.":
                    $ change_stat("confidence", -2)

    elif current_quiz_number == 2:
        if current_tier == "high":
            mara "Excellent! Your effort really shows. I can see you're starting to understand more than before."
            menu:
                "Thanks! I feel like I'm actually improving.":
                    $ change_stat("confidence", 2)
                "I think I'm finally starting to get the hang of it.":
                    $ change_stat("positiveness", 2)
        elif current_tier == "medium":
            mara "Good job on what you understood. Let's take a closer look at the parts you missed. You'll get there!"
            menu:
                "Okay, I'll try to improve next time.":
                    $ change_stat("confidence", 2)
                "I'm never getting better, am I?":
                    show mara sad with dissolve
                    $ change_stat("confidence", -2)
        else:
            mara "You seem a bit tense... is something bothering you? Don't let it weigh you down too much. You also need to take care of your mental health."
            menu:
                "It's just that I don't want to disappoint anyone.":
                    $ change_stat("confidence", 2)
                "I feel like I'm always slow... I hate it.":
                    $ change_stat("confidence", -2)

    elif current_quiz_number == 3:
        if current_tier == "high":
            mara "You carried yourself differently today. There was something steady in the way you worked. Good job."
            menu:
                "I actually felt calmer this time.":
                    $ change_stat("confidence", 2)
                "It's nice when things go your way.":
                    $ change_stat("positiveness", 2)
        elif current_tier == "medium":
            mara "You walked out with that 'thinking face' again. Want to talk it out?"
            menu:
                "I'm okay. Just tired.":
                    show mara sad with dissolve
                    $ change_stat("positiveness", -2)
                "That quiz wasn't horrible, I guess.":
                    $ change_stat("positiveness", 2)
        else:
            mara "You look drained. Sit with that feeling for a moment, don't push it away. Did something throw you off?"
            menu:
                "...I felt behind from the start.":
                    $ change_stat("confidence", -2)
                "My mind just froze. This doesn't represent me.":
                    $ change_stat("confidence", 2)

    elif current_quiz_number == 4:
        if current_tier == "high":
            mara "I watched you from my desk. You are steady and focused. You seem like you finally trust yourself enough."
            menu:
                "I'm learning to.":
                    $ change_stat("confidence", 2)
                "I don't think I trust myself.":
                    show mara neutral with dissolve
                    pass
        elif current_tier == "medium":
            mara "You seem a bit torn. Not defeated but not exactly confident. Want to tell me what felt off?"
            menu:
                "I just couldn't focus.":
                    pass
                "It was harder than I expected.":
                    $ change_stat("positiveness", 2)
        else:
            mara "You seem so tense... Are you feeling drained?"
            menu:
                "Yeah... this quiz tested me more than the others.":
                    $ change_stat("positiveness", 1)
                "I felt stuck the whole time.":
                    $ change_stat("confidence", -2)

    elif current_quiz_number == 5:
        if current_tier == "high":
            mara "I feel like you start to learn things that won't show up on grades. I just wish the system valued that..."
            menu:
                "Me too.":
                    $ change_stat("positiveness", 2)
                "Sometimes it feels pointless.":
                    show mara neutral with dissolve
                    $ change_stat("positiveness", -2)
        elif current_tier == "medium":
            mara "I'm proud of you for staying present, even when it was hard."
            menu:
                "That means a lot.":
                    $ change_stat("confidence", 2)
                "I don't always feel present.":
                    $ change_stat("confidence", -1)
        else:
            mara "You look exhausted in a way rest won't fix. This quiz was unfairly hard."
            menu:
                "It made me feel stupid.":
                    $ change_stat("confidence", -2)
                "It just gets very hard sometimes... but thank you for being here for me.":
                    $ change_stat("positiveness", 2)

    elif current_quiz_number == 6:
        if current_tier == "high":
            mara "I'm starting to get sick of rewarding obedience instead of humanity."
            menu:
                "That explains a lot.":
                    $ change_stat("positiveness", 1)
                "So what can we do?":
                    pass
        elif current_tier == "medium":
            mara "You're growing in ways quizzes can't track. Most of the teachers either hate that, either can't see that in you."
            menu:
                "I can feel it so that's what matters.":
                    $ change_stat("confidence", 2)
                "I just wished someone noticed.":
                    show mara sad with dissolve
                    $ change_stat("positiveness", -2)
        else:
            mara "Don't beat yourself up too much for this quiz. I can see students learning empathy, resilience, patience... and none of it counts."
            menu:
                "Then why does it hurt so much?":
                    $ change_stat("confidence", -2)
                "Maybe I should learn how to take better care of myself...":
                    $ change_stat("positiveness", 2)

    elif current_quiz_number == 7:
        if current_tier == "high":
            mara "I stayed in this job because of students like you. You prove it matters."
            menu:
                "I'm glad you did.":
                    $ change_stat("confidence", 2)
                "I wish more teachers thought like you.":
                    pass
        elif current_tier == "medium":
            mara "The school assumes everyone starts at the same line. That's the lie."
            menu:
                "Everyone has it different.":
                    pass
                "That lie hurts people.":
                    show mara sad with dissolve
                    $ change_stat("positiveness", 2)
        else:
            mara "Some students come to school already carrying too much. And we still ask them to perform."
            menu:
                "I was one of them.":
                    $ change_stat("confidence", -1)
                "No one ever asks them why they can't perform.":
                    pass

    pause 0.8
    hide mara with dissolve
    return

# ------------------------------------------

label interact_jacob:
    if current_tier == "high":
        show jacob neutral at center with dissolve
    elif current_tier == "low":
        show jacob mocking at center with dissolve
    else:
        show jacob neutral at center with dissolve

    if current_quiz_number == 1:
        if current_tier == "high":
            jacob "Fine. You didn't embarrass yourself today. Barely."
            menu:
                "I'll take that as a compliment.":
                    show jacob smiling with dissolve
                    $ change_stat("confidence", 2)
                "Thanks, I suppose.":
                    pass
        elif current_tier == "medium":
            show jacob frowning at center with dissolve
            jacob "You missed such obvious things. Do you even read the material I send you?"
            menu:
                "I'll try harder next time.":
                    $ change_stat("positiveness", -2)
                "Yes, I read it.":
                    $ change_stat("confidence", -2)
        else:
            jacob "That was actually pathetic. Do you plan on living your whole life clueless?"
            menu:
                "I... I'll try harder.":
                    $ change_stat("confidence", -2)
                "You know you really shouldn't talk to me like that, right?":
                    show jacob frowning with dissolve
                    $ change_stat("positiveness", 2)

    elif current_quiz_number == 2:
        if current_tier == "high":
            jacob "Hmm... I can see some improvement. Keep it, but don't get complacent."
            menu:
                "Thanks, I'll do my best.":
                    $ change_stat("confidence", 2)
                "I'll try to maintain it.":
                    pass
        elif current_tier == "medium":
            show jacob frowning at center with dissolve
            jacob "You have such a long way to come. You are mediocre."
            menu:
                "I aim for better.":
                    $ change_stat("confidence", 2)
                "Understood.":
                    $ change_stat("confidence", -2)
        else:
            jacob "You are failing behind. Look at your classmates getting better and you stalling. Is this all you want from life?"
            menu:
                "I'll try harder next time...":
                    $ change_stat("confidence", -2)
                "I know... I'm always failing. I can't do anything right these days.":
                    $ change_stat("confidence", -3)

    elif current_quiz_number == 3:
        if current_tier == "high":
            jacob "Don't smile yet. Students often think they did well when in reality they didn't understand the material."
            menu:
                "I'll let the grade speak then.":
                    $ change_stat("confidence", 2)
                "Why do you always assume the worst?":
                    show jacob frowning with dissolve
                    pass
        elif current_tier == "medium":
            jacob "You hesitate often. Hesitation is a sign of weak fundamentals. Study. More."
            menu:
                "I'll work on it.":
                    $ change_stat("confidence", -2)
                "I'm trying.":
                    pass
        else:
            jacob "Let me guess... another mediocre performance? You walked out like someone who already knows they failed."
            menu:
                "I tried...":
                    $ change_stat("confidence", -2)
                "You don't have to say it like that.":
                    $ change_stat("positiveness", -1)

    elif current_quiz_number == 4:
        if current_tier == "high":
            jacob "Don't assume you did well just because you felt confident. Confidence is a trap."
            menu:
                "My reasoning was solid.":
                    $ change_stat("confidence", 2)
                "We'll see the results.":
                    pass
        elif current_tier == "medium":
            jacob "Questioning the school system... no... questioning ME is a distraction from improving yourself."
            menu:
                "Or a way to survive it.":
                    pass
                "I'll focus more.":
                    $ change_stat("confidence", -2)
        else:
            jacob "You are lost. Completely lost. This quiz wasn't even difficult. It's a talent how you managed to struggle."
            menu:
                "...I don't know what to say.":
                    $ change_stat("confidence", -2)
                "Please stop talking to me like that.":
                    $ change_stat("confidence", 1)

    elif current_quiz_number == 5:
        if current_tier == "high":
            jacob "Don't let one decent performance inflate your ego."
            menu:
                "It's not ego, it's effort.":
                    $ change_stat("confidence", 2)
                "Understood.":
                    $ change_stat("confidence", -2)
        elif current_tier == "medium":
            show jacob frowning at center with dissolve
            jacob "I've seen you hesitate too much. This is not how successful people act."
            menu:
                "I'll work on it.":
                    $ change_stat("confidence", -1)
                "Thinking takes time.":
                    pass
        else:
            jacob "This quiz separated capable students from the rest. You should think about where you stand."
            menu:
                "...I know.":
                    $ change_stat("confidence", -2)
                "I am trying my best.":
                    $ change_stat("confidence", 1)

    elif current_quiz_number == 6:
        if current_tier == "high":
            jacob "Don't you know? Intelligence without discipline leads nowhere."
            menu:
                "Discipline without care leads somewhere worse.":
                    $ change_stat("confidence", 2)
                "Understood.":
                    $ change_stat("confidence", -1)
        elif current_tier == "medium":
            jacob "Questioning the school system... no... questioning ME is a distraction from improving yourself."
            menu:
                "Or a way to survive it.":
                    pass
                "I'll focus more.":
                    $ change_stat("confidence", -2)
        else:
            jacob "This quiz was fair. Nobody, including the school system doesn't owe anyone comfort."
            menu:
                "This feels... cruel.":
                    $ change_stat("confidence", -1)
                "...Okay.":
                    $ change_stat("confidence", -2)

    elif current_quiz_number == 7:
        if current_tier == "high":
            jacob "Compassion lowers expectations. That's a dangerous game to play."
            menu:
                "The same goes with cruelty.":
                    $ change_stat("confidence", 2)
                "Noted.":
                    $ change_stat("confidence", -2)
        elif current_tier == "medium":
            jacob "Equal treatment is fairness. Personal stories don't change standards."
            menu:
                "The problem is bigger than I expected...":
                    pass
                "I understand.":
                    $ change_stat("confidence", -2)
        else:
            jacob "Real life won't care about your circumstances. School prepares you for that."
            menu:
                "It just taught me fear.":
                    pass
                "...Okay.":
                    $ change_stat("confidence", -2)

    pause 0.8
    hide jacob with dissolve
    return

# ------------------------------------------

label interact_sofia:
    if current_tier == "high":
        show sofia smiling at center with dissolve
    elif current_tier == "low":
        show sofia sad at center with dissolve
    else:
        show sofia neutral at center with dissolve

    if current_quiz_number == 1:
        if current_tier == "high":
            sofia "You had a good aura today. It made my morning a bit lighter."
            menu:
                "I try to stay hopeful.":
                    $ change_stat("positiveness", 2)
                "Thanks, Sofia. I hope you are doing good yourself.":
                    $ change_stat("confidence", 2)
        elif current_tier == "medium":
            sofia "You did alright today. Keep going."
            menu:
                "Thank you, miss.":
                    pass
        else:
            sofia "You look like you're holding the whole world on your shoulders. Everything alright?"
            menu:
                "Just tired.":
                    pass
                "Does it really matter anymore?":
                    $ change_stat("positiveness", -2)

    elif current_quiz_number == 2:
        if current_tier == "high":
            sofia "I can see you're really focused. Maybe you can help your classmates too. Might lighten my load."
            menu:
                "I'll try to help where I can.":
                    $ change_stat("positiveness", 2)
                "That's not for me.":
                    pass
        elif current_tier == "medium":
            sofia "You're keeping up, that's good. Just keep trying, okay?"
            menu:
                "Thanks.":
                    pass
                "I'll keep trying.":
                    $ change_stat("confidence", 2)
        else:
            sofia "I see you struggling. Just don't give up, even if it gets really hard."
            menu:
                "I'll try.":
                    $ change_stat("confidence", 2)
                "I feel like I'll never keep up with my colleagues...":
                    $ change_stat("confidence", -2)

    elif current_quiz_number == 3:
        if current_tier == "high":
            sofia "You look... weirdly calm. I envied that for a second. Maybe you're handling school better than I am, haha."
            menu:
                "I'm trying, that's all.":
                    $ change_stat("confidence", 2)
                "It comes and goes.":
                    pass
        elif current_tier == "medium":
            sofia "I can't even tell which quizzes are hard and which ones aren't. How was it?"
            menu:
                "Not sure, I just pushed through.":
                    pass
                "It was manageable.":
                    $ change_stat("positiveness", 2)
        else:
            sofia "You look as tired as I feel. This quiz wasn't so kind to you, was it?"
            menu:
                "No, it really wasn't.":
                    $ change_stat("confidence", -2)
                "I'm exhausted.":
                    $ change_stat("positiveness", -2)

    elif current_quiz_number == 4:
        if current_tier == "high":
            sofia "You walked out calmer than most teachers do after a staff meeting. I almost envied you."
            menu:
                "I did my best. That's all I can do.":
                    $ change_stat("confidence", 2)
                "Today felt okay.":
                    $ change_stat("confidence", 1)
        elif current_tier == "medium":
            sofia "Honestly, I spaced out while making this quiz. Was it a bit confusing?"
            menu:
                "Yeah, kinda.":
                    pass
                "It was manageable.":
                    $ change_stat("positiveness", 2)
        else:
            sofia "You look drained... I get it. This quiz actually drained ME just from watching all of you take it."
            menu:
                "Everything feels heavy today.":
                    $ change_stat("positiveness", -2)
                "Yeah... everyone seems exhausted here.":
                    pass

    elif current_quiz_number == 5:
        if current_tier == "high":
            sofia "Seeing you push through makes me remember why I started teaching."
            menu:
                "That means a lot.":
                    $ change_stat("positiveness", 2)
                "I hope it lasts.":
                    pass
        elif current_tier == "medium":
            sofia "You handled this quiz better than most. That says something."
            menu:
                "I guess.":
                    pass
                "I'm trying.":
                    $ change_stat("confidence", 1)
        else:
            sofia "I barely had the energy to watch this quiz... How did it feel on your side?"
            menu:
                "Hard.":
                    $ change_stat("positiveness", -2)
                "It was definitely challenging.":
                    $ change_stat("confidence", 1)

    elif current_quiz_number == 6:
        if current_tier == "high":
            sofia "If more students thought like you, maybe teaching wouldn't feel like damage control."
            menu:
                "Then maybe we can change something.":
                    $ change_stat("positiveness", 2)
                "I hope I won't forget this.":
                    pass
        elif current_tier == "medium":
            sofia "I feel like you are learning how systems shape people. I wish I had learned that earlier."
            menu:
                "Maybe it's not too late.":
                    $ change_stat("positiveness", 1)
                "I just don't want to become numb.":
                    pass
        else:
            sofia "I watch students shrink under grades... and I still have to hand them out."
            menu:
                "That sounds exhausting.":
                    pass
                "Does it ever stop?":
                    $ change_stat("positiveness", -2)

    elif current_quiz_number == 7:
        if current_tier == "high":
            sofia "Remember how this felt. Maybe you'll treat people differently."
            menu:
                "I will.":
                    $ change_stat("positiveness", 2)
                "I hope so.":
                    pass
        elif current_tier == "medium":
            sofia "Teaching sometimes drains you. Pretending it doesn't is how people break."
            menu:
                "Students can also break like that.":
                    $ change_stat("confidence", 2)
                "Teachers also have their own problems...":
                    pass
        else:
            sofia "I've seen kids fail not because they weren't smart... but because they were exhausted."
            menu:
                "That sounds familiar.":
                    pass
                "No one noticed.":
                    $ change_stat("positiveness", -1)

    pause 0.8
    hide sofia with dissolve
    return