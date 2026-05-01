# Conditions for the Greedy Algorithm to be Optimal

When the greedy coin change algorithm is guaranteed to use the mathematically absolute fewest coins possible, the coin system is known as a **Canonical Coin System**.

If a coin system is *non-canonical*, there will always exist certain values of $N$ where the greedy algorithm fails to find the smallest number of coins (e.g., using `[1, 3, 4]` to make essentially any even multiple of $3$ like $6$).

## When is a Coin System Guaranteed to be Canonical?

There is no simple, universal formula that works for *all* integer groupings to immediately determine if they are canonical without running a structural check (like Pearson's algorithm in $O(N^3)$), but there are **sufficient conditions** where the greedy algorithm is strictly guaranteed to work perfectly every single time:

### Condition 1: Strict Multiples (The Divisibility Condition)
The most common condition under which a greedy approach works is when **every coin denomination is an integer multiple of the next smaller denomination**.

**Example:**
* Coins: `{1, 5, 10, 50, 100}`
* 100 is a multiple of 50. 50 is a multiple of 10. 10 is a multiple of 5. 5 is a multiple of 1.
* Because of perfect divisibility, a larger coin can intrinsically always perfectly substitute identical sums of smaller coins, guaranteeing no "overlap" inefficiency. 
* This is why metric/base-10 currency bounds generally work great.

### Condition 2: The "Standard US Coin" exception (M > 2C)
Not all canonical systems follow perfect multiples. The standard US Coin system `{1, 5, 10, 25}` is undeniably canonical, but 25 is *not* a multiple of 10!

Researchers have found that a broader sufficient condition for the greedy algorithm to be optimal is if the denominations satisfy certain bounds. Specifically, if for any consecutive coins $c_1, c_2, c_3$ where $c_3 > c_2 > c_1$:
* $c_3 < c_1 + c_2 < c_4$
*(Note: the actual mathematical theorem requires checking representations up to $c_n + c_{n-1}$, formulated independently by Kozen, Zaks, and Pearson.)*

### Why the Greedy Algorithm Fails on `{1, 15, 25}`
The greedy algorithm looks only at the *largest immediate bite* it can take.
When calculating change for $N=30$:
* **Greedy** grabs $25$. It then needs to make $5$, which requires five $1$s. Result: `[25, 1, 1, 1, 1, 1]` (6 coins).
* **Optimal** looks at the global picture. It ignores the $25$ because $15 + 15 = 30$. Result: `[15, 15]` (2 coins).

Greedy fails here because the gap between $15$ and $25$ is too small relative to the global sum. The "greedy" bite trap prevents it from combining smaller efficient pairs!
