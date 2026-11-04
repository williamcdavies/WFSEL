# Strategies (A–D)
The letters "A", "B", "C", and/or "D" may appear throughout this codebase. Each letter represents one of the strategies defined below.

## Dictionary

| Strategy | High smoke year(s)                                                                 | Low smoke year(s)                                  | Season Function |
|:-------- |:---------------------------------------------------------------------------------- |:-------------------------------------------------- |:--------------- |
| **$A$**  | Most recent year at or above the high threshold                                    | Most recent year at or below the low threshold     | Sliding Window  |
| **$B$**  | Most recent year at or above the high threshold                                    | All years at or below the low threshold (averaged) | Sliding Window  |
| **$C$**  | Year with the greatest count of distinct start days at or above the high threshold | All years at or below the low threshold (averaged) | Sliding Window  |
| **$D$**  | All years at or above the high threshold (averaged)                                | All years at or below the low threshold (averaged) | Sliding Window  |
