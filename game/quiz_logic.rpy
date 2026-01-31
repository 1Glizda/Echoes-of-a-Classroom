# quiz_logic.rpy

# This label runs a specific quiz question based on Subject and Index
# Usage: call start_quiz("Math", 0) 
# (Index 0 is the first question, 1 is the second, etc.)

label start_quiz(subject_name):
    
    # 1. Setup Loop Variables
    $ q_index = 0
    # Calculate how many questions exist for this subject
    $ total_questions = len(quiz_db[subject_name])

    # 2. Start the Loop
    while q_index < total_questions:
        
        # Get the specific question data for the current index
        $ q_data = quiz_db[subject_name][q_index]

        # Call the Quiz Screen
        call screen quiz_screen(q_data)
        $ result = _return

        # Handle the Result
        if result == "correct":
            # Show Feedback (Waits for "Continue")
            call screen quiz_feedback(True, q_data["explanation"])
            
            # Stats Logic
            $ change_stat("smart", 2)
            $ change_stat("confidence", 1)
            
        elif result == "wrong":
            call screen quiz_feedback(False, "The correct answer was: " + q_data["correct"] + "\n\n" + q_data["explanation"])
            
            $ change_stat("smart", -1)
            
        elif result == "timeout":
            call screen quiz_feedback(False, "Time's up!\n\nThe correct answer was: " + q_data["correct"])
            
            $ change_stat("confidence", -2)

        # Increment index to move to the next question
        $ q_index += 1

        # Restore the atmospheric music now that the quiz is done
        $ restore_game_music()

    # Loop finishes when q_index reaches total_questions
    return