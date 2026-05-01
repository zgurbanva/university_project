# Chomp Game: Algorithm & Architecture Explained

This document provides a detailed explanation of the algorithms and data structures used to power the futuristic edition of the Chomp game.

## 1. Game State Tracking (The `rows` Array)
Instead of keeping a massively heavy 2D array (like a $10000 \times 10000$ matrix that would freeze the browser), the algorithm uses a 1-Dimensional tracking array.
```javascript
// Example for a 5x5 grid
let rows = [5, 5, 5, 5, 5];
```
Each index represents a **Row**, and the value at that index represents **how many columns (chocolates) remain** in that specific row. 
Because of the nature of Chomp (where eating a piece removes everything below and to its right), the values in this array are always mathematically non-increasing (e.g., `rows[0] >= rows[1] >= rows[2]`).

## 2. The "Chomping" Algorithm
When a player selects a coordinate `(r, c)` to eat:
1. **Boundary Validation**: The algorithm first checks if `r < m` and `c < rows[r]`. If `c` is greater than `rows[r]`, the chocolate is already eaten.
2. **Deletion Loop**: It iterates exclusively from the targeted row `r` down to the final row `m - 1`.
3. **Slicing**: For any row `i` where `rows[i] > c`, the algorithm truncates it so `rows[i] = c`.
```javascript
for (let i = r; i < m; i++) {
    if (rows[i] > c) rows[i] = c;
}
```
This is an incredibly efficient $O(M)$ operation. Even for 10,000 rows, it calculates instantly.

## 3. Dynamic Rendering (The Bounding Polygon)
Drawing 100,000,000 individual squares for a $10000 \times 10000$ grid destroys browser memory. Instead, the drawing algorithm traces the **outer boundary** of the `rows` array.
- It starts at the bottom-left `(0, Height)`.
- It loops through `rows`, plotting the right-edge `(rows[r] * cellWidth)` for each row's top and bottom.
- It connects the lines into a single, beautiful glowing polygon that the browser renders in just 1 millisecond.

## 4. Visual Orientation Flipping (Poison Selection)
When the player chooses to place the Poison at the **Bottom-Right** instead of the **Top-Left**:
- The algorithm keeps the backend exactly the same (meaning index `0,0` is still the computational poison).
- It applies an HTML5 Canvas transform (`ctx.translate` and `ctx.scale(-1, -1)`) to physically flip the drawing 180 degrees.
- When the user's mouse clicks a pixel `(x, y)`, the algorithm reverses the visual row/col coordinates before feeding them into the unchanged backend.
