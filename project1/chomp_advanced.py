
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
    Renders the board if it's small enough. For massive grids, simplifies the output
    so that the console doesn't freeze or run out of memory trying to print millions of characters.
    
    Args:
        rows (list): A 1D array representing the state of the grid.
        m (int): Total number of initialized rows in the game.
        poison_loc (str): Indicates starting poison orientation, either 'top-left' or 'bottom-left'.
    """
    # Look for the row with the most active columns
    n = max([cols for cols in rows if cols > 0], default=0)
    
    # Memory/Display protection for huge grids
    if m > 50 or n > 50:
        print(f"{DARK_PURPLE}[Grid too large to display visually. System is tracking bounds.]")
        print(f"Remaining active rows: {sum(1 for r in rows if r > 0)}")  # Compute sum of active elements
        print(f"Max remaining width: {n}{RESET}")
        return

    # Print column headers (X-Axis coordinates)
    header = f"   "
    for c in range(n):
        header += f"{CYAN}{c:2}{RESET} "
    print(header)
    
    # Iterate dynamically to print each cell
    for visual_r in range(m):
        row_str = f"{CYAN}{visual_r:2}{RESET} " # Add the visual Y-Axis coordinate label
        
        # Determine the underlying backend mathematical row based on the player's visual row
        backend_r = visual_r
        if poison_loc == 'bottom-left':
           # If poison is bottom-left, the visual bottom row (idx: m-1) is the backend matrix row (0)
           backend_r = (m - 1) - visual_r
           
        # Print "chocolates" for the length of whatever columns are remaining in this active row
        for visual_c in range(rows[backend_r]):
            # Has the player reached index 0,0? Highlight the poison.
            if backend_r == 0 and visual_c == 0:
                row_str += f"{RED_BG}{WHITE} P {RESET}" # Poisoned square
            else:
                row_str += f"{PURPLE} O {RESET}" # Normal Chocolate square
        print(row_str)

def play_chomp():
    """
    Main interactive game loop for the Chomp terminal CLI.
    Runs the protocol and validates inputs continuously until a fatal error or player win.
    """
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
            
        # Map user's visual inputs directly to backend matrix dimensions
        backend_r = visual_r
        backend_c = visual_c
        
        if poison_loc == 'bottom-left':
            # Visual row maps to inverted backend row
            # e.g., if visual_r is m-1, backend_r is 0. Mathematical parity guaranteed.
            backend_r = (m - 1) - visual_r
            
        # Protect execution logic by ensuring input coordinate isn't already eaten or out of range
        if backend_r < 0 or backend_r >= m or backend_c < 0 or backend_c >= rows[backend_r]:
            print(f"{RED_BG}Error:{RESET} Invalid move. Coordinate is out of bounds or already bypassed.")
            continue
            
        # Check specifically if the isolated poison square has been targeted
        if backend_r == 0 and backend_c == 0:
            print(f"\n{RED_BG}{WHITE} ALERT! {RESET} Player {player} consumed the poisoned block!")
            print(f"\n{BOLD}{PURPLE}>>> PLAYER {3 - player} WINS! <<<{RESET}\n")
            break
            
        # Perform the "Chomp" perfectly at O(M) time cost. 
        # Safely handling tens of millions of blocks seamlessly by ignoring nested loops.
        # It loops vertically through the matrix and forces mathematical boundaries tightly down to `backend_c`.
        for i in range(backend_r, m):
            if rows[i] > backend_c:
                rows[i] = backend_c
                
        # Advance the active player toggle successfully
        player = 3 - player

if __name__ == "__main__":
    try:
        play_chomp()
    except KeyboardInterrupt:
        print(f"\n{RED_BG}Game aborted.{RESET}")
        sys.exit(0)
