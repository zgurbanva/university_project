def greedy_change(coins, amount):
    """
    Computes the change using the Greedy Algorithm.
    The Greedy Algorithm makes the locally optimal choice at each step.
    In this case, it continuously takes the largest possible coin denomination 
    that is less than or equal to the remaining amount.
    """
    # Sort coins in descending order to always try the largest coin first
    coins_sorted = sorted(coins, reverse=True)
    result = []
    current_amount = amount
    
    # Iterate through the available coin denominations
    for coin in coins_sorted:
        # While the current accumulated amount is large enough to use this coin
        while current_amount >= coin:
            result.append(coin)       # Add the coin to our result list
            current_amount -= coin    # Subtract the coin's value from the remaining amount
            
    # If after checking all coins the remaining amount is not exactly zero,
    # it means the given denominations cannot make the exact change greedily.
    if current_amount > 0:
        return None 
    return result

def optimal_change(coins, amount):
    """
    Computes the exact smallest number of coins using Dynamic Programming (DP).
    Unlike the Greedy approach, DP guarantees finding the true mathematical minimum
    by solving subproblems and building up globally optimal solutions.
    """
    # dp[i] stores the minimum number of coins needed to make the amount i.
    # Initialize all values to infinity, meaning "unreachable mathematically so far".
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0 # Base case: 0 coins are needed to make an amount of 0.
    
    # Store the first coin added at each step to allow reconstructing the final answer.
    coin_used = [-1] * (amount + 1)
    
    # Iterate through every amount from 1 up to the target budget
    for i in range(1, amount + 1):
        # Try every available coin denomination
        for coin in coins:
            # If the coin can contribute to the current amount 'i', 
            # and using it results in fewer total coins than the previously known best:
            if i >= coin and dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1 # Update the minimum coins needed
                coin_used[i] = coin      # Record which coin was used to achieve this minimum
                
    # If the target amount remains infinity, there is no mathematical way to make exact change.
    if dp[amount] == float('inf'):
        return None
        
    # Reconstruct the list of optimal coins used by tracing back through the coin_used array
    result = []
    curr = amount
    while curr > 0:
        result.append(coin_used[curr]) # Add the coin used to reach current amount
        curr -= coin_used[curr]        # Step backwards by the coin's value
        
    # Sort in descending order to make the output format consistent with the greedy output
    return sorted(result, reverse=True)

def analyze_system(coins, amount):
    """
    Compares the Greedy approach versus the Optimal (DP) approach.
    This function effectively tests whether the given coin system is "canonical"
    for the specific budget provided.
    """
    print(f"--- Analyzing Change for {amount} with Denominations: {coins} ---")
    greedy = greedy_change(coins, amount)
    optimal = optimal_change(coins, amount)
    
    if greedy is None or optimal is None:
        print("Cannot make exact change with these coins.\n")
        return
        
    print(f"Optimal Solution (DP): Used {len(optimal)} coins -> {optimal}")
    print(f"Greedy Result        : Used {len(greedy)} coins -> {greedy}")
    
    print("\n--- Conclusion: Which is better? ---")
    if len(greedy) == len(optimal):
        print("Both algorithms perform equally well! ")
        print("Result: GREEDY IS OPTIMAL (Smallest possible number of coins used).")
    else:
        print("The Optimal Solution (DP) is better!")
        print(f"Result:  GREEDY FAILED (It used {len(greedy)} coins, but the minimum possible is {len(optimal)}).")
    print()

if __name__ == "__main__":
    print("--- Coin Change Analyzer ---")
    try:
        amount_input = input("Enter the target amount (budget): ")
        amount = int(amount_input.strip())
        
        coins_input = input("Enter the coin denominations separated by commas (e.g., 1, 5, 10, 25): ")
        # Parse the comma-separated string into a list of integers
        coins = [int(c.strip()) for c in coins_input.split(',')]
        
        print("\n")
        analyze_system(coins, amount)
        
    except ValueError:
        print("\nError: Invalid input. Please make sure you only enter numbers.")
