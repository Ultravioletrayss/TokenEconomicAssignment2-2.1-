
---

### 2.3: Uniswap V2 Swap Simulation Function

#### Overview

This function simulates the **Uniswap V2 `getAmountOut`** logic. It calculates how many output tokens you would receive from the pool given a specific input token amount. It is based on the **constant product formula** (`x * y = k`) and accounts for the default **0.3% fee**. Integer arithmetic is used to match Solidity precision exactly.

#### Input Parameters

* `amount_in` (int): Amount of input tokens (in the smallest unit, e.g., wei or token’s smallest unit).
* `token_in_is_token0` (bool): Whether the input token is **token0** of the pool (`True` if yes, e.g., USDC; `False` if token1, e.g., WETH).
* `reserves` (tuple\[int, int]): Pool reserves **before the swap** `(reserve0, reserve1)`, where `reserve0` is token0 reserve and `reserve1` is token1 reserve (in the smallest unit).
* `fee` (float, default `0.003`): Pool fee rate (0.3% by default).

#### Output

* `int`: Amount of output tokens (in the smallest unit).

#### Formula

```
amount_out = (amount_in * fee_multiplier * reserve_out) // (reserve_in * 1000 + amount_in * fee_multiplier)
```

Where:
`fee_multiplier = 1000 * (1 - fee)` (e.g., 997 for 0.3% fee).
Floor division `//` is used to simulate Solidity integer arithmetic.

#### Function Code

```python
def get_amount_out(amount_in: int, token_in_is_token0: bool, reserves: tuple[int, int], fee: float = 0.003) -> int:
    """
    Simulate the Uniswap V2 getAmountOut formula.
    
    Parameters:
    - amount_in: Input token amount (int, smallest unit, e.g., wei).
    - token_in_is_token0: True if input token is pool's token0 (e.g., USDC), False if token1 (e.g., WETH).
    - reserves: Tuple of pool reserves before swap (reserve0, reserve1), in smallest unit.
    - fee: Pool fee rate (float, e.g., 0.003 for 0.3%).
    
    Returns:
    - Output token amount (int, smallest unit).
    
    Formula:
    amount_out = (amount_in * fee_multiplier * reserve_out) // (reserve_in * 1000 + amount_in * fee_multiplier)
    where fee_multiplier = 1000 * (1 - fee). Integer arithmetic is used to match Solidity precision.
    """
    reserve0, reserve1 = reserves
    if token_in_is_token0:
        reserve_in = reserve0
        reserve_out = reserve1
    else:
        reserve_in = reserve1
        reserve_out = reserve0
    
    if amount_in == 0:
        return 0
    
    fee_multiplier = int(1000 * (1 - fee))  # e.g., 0.003 -> 997
    amount_in_with_fee = amount_in * fee_multiplier
    numerator = amount_in_with_fee * reserve_out
    denominator = reserve_in * 1000 + amount_in_with_fee
    return numerator // denominator
```

#### Usage Example

```python
# Example: Swap 1 ETH (1e18 wei), WETH is token1, assume reserves
result = get_amount_out(
    1_000_000_000_000_000_000,  # 1 ETH in wei
    token_in_is_token0=False,    # WETH is token1
    reserves=(1_000_000_000_000, 1_000_000_000_000_000_000_000),  # example reserves (token0, token1)
    fee=0.003
)
print(result)  # Outputs corresponding USDC amount
```

---
