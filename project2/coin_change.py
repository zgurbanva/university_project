def greedy_change(coins, amount):
    """
    Computes the change using the Greedy Algorithm.
    It takes the largest possible coin until the amount is zero.
    """
    coins_sorted = sorted(coins, reverse=True)
    result = []
    current_amount = amount
    
    for coin in coins_sorted:
        while current_amount >= coin:
            result.append(coin)
            current_amount -= coin
            
    # If the exact amount cannot be made, return what we have (or an error)
    if current_amount > 0:
        return None 
    return result

def optimal_change(coins, amount):
    """
    Computes the exact smallest number of coins using Dynamic Programming (DP).
    This guarantees finding the true mathematical minimum.
    """
    # dp[i] stores the minimum number of coins to make amount i
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    # Store the first coin added to trace back the actual coins used
    coin_used = [-1] * (amount + 1)
    
    for i in range(1, amount + 1):
        for coin in coins:
            if i >= coin and dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1
                coin_used[i] = coin
                
    if dp[amount] == float('inf'):
        return None
        
    # Reconstruct the optimal coins used
    result = []
    curr = amount
    while curr > 0:
        result.append(coin_used[curr])
        curr -= coin_used[curr]
        
    # Sort for consistent output comparison
    return sorted(result, reverse=True)

def analyze_system(coins, amount):
    """
    Compares the Greedy approach vs the Optimal approach
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
