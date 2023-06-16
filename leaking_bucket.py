import time
from collections import deque

class LeakyBucket:
    def __init__(self, capacity, consume_rate, consume_time):
        self.capacity = capacity
        self.consume_rate = consume_rate
        self.consume_time = consume_time
        self.tokens = 0
        self.last_leak_time = time.time()
        #self.queue = deque(max_len = capacity)

    def add_token(self, token):
        if self.tokens+token <= self.capacity:
            self.tokens += token
            #self.queue.append(token)
            return True
        else:
            return False

    #assume consume_tokens is called at a constant rate
    def consume_tokens(self):
        now = time.time()
        time_elapsed = now - self.last_leak_time
        if time_elapsed >= self.consume_time:
            self.tokens = max(self.tokens - self.consume_rate, 0)
            return True
        else:
            return False
        


# Example usage:
bucket = LeakyBucket(capacity=10, consume_rate=2, consume_time=1)  # Set the capacity and refill rate

# Consume tokens
tokens_to_consume = 5
if bucket.consume_tokens(tokens_to_consume):
    print(f"Successfully consumed {tokens_to_consume} tokens.")
else:
    print("Failed to consume tokens. Bucket is empty.")

# Wait for a while
time.sleep(2)

# Consume tokens again
tokens_to_consume = 8
if bucket.consume_tokens(tokens_to_consume):
    print(f"Successfully consumed {tokens_to_consume} tokens.")
else:
    print("Failed to consume tokens. Bucket is empty.")

