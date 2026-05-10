# Chomp Game: Algorithm & Architecture Explained

This document provides a detailed explanation of the algorithms and data structures used to power the futuristic edition of the Chomp game.

<!-- Note: These algorithms were specifically built to handle up to 10,000x10,000 grid bounds safely and efficiently across both memory and raw CPU computation logic in Python/JS. -->

## 1. Game State Tracking (The `rows` Array)
Instead of keeping a massively heavy 2D matrix (like a $10000 \times 10000$ matrix that would freeze the user's browser processing power entirely to iterate loops against), the logic scales elegantly using just a 1-Dimensional tracking array.
```javascript
// Example for a 5x5 grid's initial state
let rows = [5, 5, 5, 5, 5];
```
Each index mathematically maps to a specific **Row**, and the numeric value stored inside each index maps exactly to **how many solid columns (chocolates) remain active** inside of that singular row. 
Because of the algorithmic rules of Chomp (where selecting and eating any arbitrary piece instantly guarantees the subtraction of all pieces below and to the right of it uniformly), the array variables cascade dynamically and stay strictly **non-increasing** overall. (e.g., `rows[0] >= rows[1] >= rows[2]`).

## 2. The "Chomping" Calculation Loop
When a user manually interacts or clicks on an abstract target coordinate `(r, c)` to effectively "eat":
1. **Safety Boundary Authentication**: The system algorithm strictly asserts bounds logic checking if `r < m` (the target row exists) and if `c < rows[r]` (the target column has not already been deleted/eaten by a prior iteration). If `c` mathematically exceeds `rows[r]`, it throws an intentional out-of-bounds protection error.
2. **Cascading Deletion Matrix**: The actual process completely skips a nested XY iteration loop and executes a linear wipe loop downwards securely originating from the specific clicked row point `r`, terminating exactly exactly at `m - 1`.
3. **Array Splitting**: Inside the mathematical execution, for any specific localized `i` row variable where its quantity `rows[i] > c` physically exists, it aggressively hard-caps and overrides the data bound straight downwards, forcing `rows[i] = c`.
```javascript
// A simple loop ensuring an O(M) subtraction
for (let i = r; i < m; i++) {
    if (rows[i] > c) rows[i] = c;
}
```
This converts a $O(N \times M)$ processing nightmare into a lightweight, insanely scaleable $O(M)$ processing task enabling near-instant render calculations mathematically.

## 3. Dynamic Hardware UI Rendering (The Interactive Polygon Mapping)
Simulating hundreds of millions (`10000 * 10000`) of unique HTML elements natively DOM crashes standard browsing environments immediately. To circumnavigate limitations securely:
- The custom engine abstracts the math arrays into a **singlular continuous polygon geometric border** connecting raw bounding exterior lines mathematically.
- Tracing strictly operates up effectively mapping out `yTop`, `yBottom` scaling off the active widths defined natively by `rows[r] * cellWidth`.
- The engine uses continuous HTML5 Canvas logic combining straight exterior lines continuously bounding to construct an overarching polygon object drawn locally once visually taking fractions of a millisecond!

## 4. UI Visual Origin Matrix Flipping (Configurable Poison Selection Toggle)
When the active user requests the explicit Poison block coordinate to rest locally at the **Bottom-Left** quadrant rather than mapping safely visually at the **Top-Left** quadrant:
- The system prevents confusing code-spaghetti. Instead, mathematical backend code matrix indexing always permanently reserves array logical `0,0` intrinsically to the Poison object target logic regardless conceptually to protect memory stability securely.
- Only the visual engine uses localized mathematical scaling functions locally executing an HTML5 Canvas API transform scaling using `ctx.translate` and mapping exactly directly against `ctx.scale(1, -1)` rendering backwards 180 degrees physically on drawing load. 
- All active input locations reverse localized target points instantly backwards dynamically processing before interacting structurally against arrays.
