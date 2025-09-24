def get_amount_out(amount_in: int, token_in_is_token0: bool, reserves: tuple[int, int], fee: float = 0.003) -> int:
    """
    模拟 Uniswap V2 getAmountOut 公式。
    输入：
    - amount_in: 输入代币数量（int，最小单位，如 wei 或代币最小单位）。
    - token_in_is_token0: True 如果输入代币是池子的 token0（例如 USDC），False 如果是 token1（例如 WETH）。
    - reserves: 池子交换前储备元组 (reserve0, reserve1)（int，最小单位；reserve0 为 token0/USDC，reserve1 为 token1/WETH）。
    - fee: 池子费用率（float，如 0.003 表示 0.3%）。

    输出：输出代币数量（int，最小单位）。

    公式：amount_out = (amount_in * fee_multiplier * reserve_out) // (reserve_in * 1000 + amount_in * fee_multiplier)
    其中 fee_multiplier = 1000 * (1 - fee)，使用整数运算模拟 Solidity 精度。
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

