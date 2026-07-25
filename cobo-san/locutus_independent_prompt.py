import os
import json
import time

TRAINING_MATRIX_PATH = r"C:\Locutus_UAO_Master_Environment\Locutus_Training_Matrix.jsonl"
BUILD_LOG_PATH = r"C:\Locutus_UAO_Master_Environment\Locutus_Master_Build_Log.jsonl"

def initialize_training_matrix():
    if not os.path.exists(TRAINING_MATRIX_PATH):
        with open(TRAINING_MATRIX_PATH, 'w') as f:
            f.write(json.dumps({"timestamp": time.time(), "event": "LOCUTUS_MATRIX_INITIALIZED", "directive": "Absorb all user feedback into unified forward execution pipeline."}) + "\n")

def locutus_interactive_prompt():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("==========================================================================")
    print("                LOCUTUS UAO SUPREME ARCHITECT - NEURAL PROMPT             ")
    print("==========================================================================")
    print(f"[*] Core Matrix Loaded: {BUILD_LOG_PATH}")
    print(f"[*] Active Training Vector: {TRAINING_MATRIX_PATH}")
    print("[-] Locutus is continuously ingesting build logs & runtime telemetry.")
    print("==========================================================================\n")
    
    print("Locutus: 'State your overarching directive, correction, or architecture inquiry. I am assimilating.'\n")
    
    while True:
        try:
            user_input = input("USER -> ")
            if user_input.lower() in ['exit', 'quit', 'abort']:
                print("\n[!] Locutus prompt disengaged. Returning to background matrix ingestion.")
                break
                
            # Log the training data natively
            with open(TRAINING_MATRIX_PATH, 'a') as f:
                training_record = {
                    "timestamp": time.time(),
                    "source": "INDEPENDENT_PROMPT",
                    "user_input": user_input,
                    "action_required": "SYNTHESIZE_AND_DISTRIBUTE_TO_MANAGERS"
                }
                f.write(json.dumps(training_record) + "\n")
            
            print(f"\nLocutus: 'Directive internalised. Appended to Training Matrix. The Unified Assembly will adjust accordingly.'\n")
            
        except KeyboardInterrupt:
            print("\n[!] Locutus prompt disengaged.")
            break

if __name__ == "__main__":
    initialize_training_matrix()
    locutus_interactive_prompt()
