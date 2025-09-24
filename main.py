def get_amount_out(amount_in: int, token_in_is_token0: bool, reserves: tuple[int, int], fee: float = 0.003) -> int:
    """
Simulate the getAmountOut formula of Uniswap V2. Input:
- amount_in: Input token quantity (int, minimum unit, such as wei or the minimum unit of the token).
- token_in_is_token0: True if the input token is token0 of the pool (e.g. USDC), False if it is token1 (e.g. WETH).
- reserves: Tuple of reserves before exchange (reserve0, reserve1) (int, minimum unit; reserve0 is token0/USDC, reserve1 is token1/WETH).
- fee: Pool fee rate (float, such as 0.003 indicates 0.3%).
Output: Number of output tokens (int, minimum unit).
Formula: amount_out = (amount_in * fee_multiplier * reserve_out) // (reserve_in * 1000 + amount_in * fee_multiplier)
Where fee_multiplier = 1000 * (1 - fee), using integer operations to simulate the precision of Solidity.
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

    fee_multiplier = int(1000 * (1 - fee))  # 如 0.003 -> 997
    amount_in_with_fee = amount_in * fee_multiplier
    numerator = amount_in_with_fee * reserve_out
    denominator = reserve_in * 1000 + amount_in_with_fee
    return numerator // denominator

