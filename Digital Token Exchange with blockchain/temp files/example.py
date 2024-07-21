class TokenExchange:
    def __init__(self, total_tokens, market_cap):
        self.total_tokens = total_tokens
        self.market_cap = market_cap
        self.current_price = market_cap / total_tokens
        self.available_tokens = total_tokens

    def buy_tokens(self, amount):
        if amount <= self.available_tokens:
            self.available_tokens -= amount
            self.current_price *= (1 + (amount / self.total_tokens))
            return f"Successfully bought {amount} tokens at {self.current_price} each."
        else:
            return "Insufficient tokens available for purchase."

    def sell_tokens(self, amount):
        if amount <= (self.total_tokens - self.available_tokens):
            self.available_tokens += amount
            self.current_price *= (1 - (amount / self.total_tokens))
            return f"Successfully sold {amount} tokens at {self.current_price} each."
        else:
            return "Insufficient tokens available for sale."

    def get_token_price(self):
        return f"Current token price: {self.current_price} each."


# Example usage:
exchange = TokenExchange(total_tokens=100000, market_cap=100000)

# Check the initial token price
print(f"Initial token price: {exchange.current_price} each")

# Buy 1000 tokens
print(exchange.buy_tokens(1000))

# Sell 500 tokens
print(exchange.sell_tokens(500))

# Check the current token price
print(exchange.get_token_price())
