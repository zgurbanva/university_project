import sys
import os

# ANSI Colors
PURPLE = '\033[95m'
DARK_PURPLE = '\033[35m'
CYAN = '\033[96m'
RED_BG = '\033[41m'
WHITE = '\033[97m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_board(rows, m, poison_loc):
    """
    Renders the board if it's small enough. For massive grids, simplifies the output.
    """
    n = max([cols for cols in rows if cols > 0], default=0)
    
    if m > 50 or n > 50:
        print(f"{DARK_PURPLE}[Grid too large to display visually. System is tracking bounds.]")
        print(f"Remaining active rows: {sum(1 for r in rows if r > 0)}")
        print(f"Max remaining width: {n}{RESET}")
        return

    # Print column headers
    header = f"   "
    for c in range(n):
        header += f"{CYAN}{c:2}{RESET} "
    print(header)
    
    for visual_r in range(m):
        row_str = f"{CYAN}{visual_r:2}{RESET} "
        
        # Determine the underlying backend row based on visual row
        backend_r = visual_r
        if poison_loc == 'bottom-left':
           # If poison is bottom-left, the visual bottom row (m-1) is the backend row (0)
           backend_r = (m - 1) - visual_r
           
        for visual_c in range(rows[backend_r]):
            if backend_r == 0 and visual_c == 0:
                row_str += f"{RED_BG}{WHITE} P {RESET}" # Poisoned square
            else:
                row_str += f"{PURPLE} O {RESET}" # Chocolate square
        print(row_str)

def play_chomp():
    print(f"\n{BOLD}{PURPLE}=== NEON CHOMP PROTOCOL (LARGE GRID SUPPORT) ==={RESET}\n")
    
    # Setup dimensions
    while True:
        try:
            m = int(input(f"{DARK_PURPLE}Enter number of rows (m): {RESET}"))
            n = int(input(f"{DARK_PURPLE}Enter number of columns (n): {RESET}"))
            if m > 0 and n > 0:
                break
            print(f"{RED_BG}m and n must be positive integers.{RESET}")
        except ValueError:
            print(f"{RED_BG}Invalid input.{RESET} Enter positive integers.")

    # Setup poison location
    print(f"\n{CYAN}Select Poison Location:{RESET}")
    print("1. Top-Left")
    print("2. Bottom-Left")
    loc_choice = input(f"{DARK_PURPLE}Enter choice (1 or 2): {RESET}")
    poison_loc = 'bottom-left' if loc_choice.strip() == '2' else 'top-left'

    # Backend tracking array (1D for massive efficiency)
    rows = [n] * m
    player = 1

    while True:
        print(f"\n{DARK_PURPLE}--- Current Grid ---{RESET}")
        print_board(rows, m, poison_loc)
        
        print(f"\n{BOLD}{CYAN}Player {player}'s turn.{RESET}")
        move = input(f"{PURPLE}Target position [row col] (or 'quit'): {RESET}")
        
        if move.strip().lower() in ['exit', 'quit']:
            break
            
        try:
            r_str, c_str = move.split()
            visual_r, visual_c = int(r_str), int(c_str)
        except ValueError:
            print(f"{RED_BG}Error:{RESET} Please enter two integers separated by a space (e.g. '1 2').")
            continue
            
        # Map visual coordinates to backend logic
        backend_r = visual_r
        backend_c = visual_c
        
        if poison_loc == 'bottom-left':
            # Visual row maps to inverted backend row
            # e.g., if visual_r is m-1, backend_r is 0
            backend_r = (m - 1) - visual_r
            
        if backend_r < 0 or backend_r >= m or backend_c < 0 or backend_c >= rows[backend_r]:
            print(f"{RED_BG}Error:{RESET} Invalid move. Coordinate is out of bounds or already bypassed.")
            continue
            
        if backend_r == 0 and backend_c == 0:
            print(f"\n{RED_BG}{WHITE} ALERT! {RESET} Player {player} consumed the poisoned block!")
            print(f"\n{BOLD}{PURPLE}>>> PLAYER {3 - player} WINS! <<<{RESET}\n")
            break
            
        # Perform the "Chomp" perfectly at O(M) time cost handling millions of blocks seamlessly
        for i in range(backend_r, m):
            if rows[i] > backend_c:
                rows[i] = backend_c
                
        player = 3 - player

if __name__ == "__main__":
    try:
        play_chomp()
    except KeyboardInterrupt:
        print(f"\n{RED_BG}Game aborted.{RESET}")
        sys.exit(0)
