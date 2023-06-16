import time
from flask import Flask, jsonify, request

app = Flask(__name__)

class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill_time = time.time()

    def refill_tokens(self):
        now = time.time()
        time_elapsed = now - self.last_refill_time
        tokens_to_add = time_elapsed * self.refill_rate
        self.tokens = min(self.tokens + tokens_to_add, self.capacity)
        self.last_refill_time = now

    def consume_tokens(self, tokens):
        self.refill_tokens()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        else:
            return False

token_buckets = {}  # Dictionary to store user token buckets

@app.route("/request", methods=["POST"])
def handle_request():
    user_id = request.headers.get("X-User-Id", "")  # Get the user ID from request headers
    req_tokens = int(request.headers.get("X-Tokens", 0))  # Get the tokens required for the request

    # Check if user token bucket exists, otherwise create a new one
    if user_id and user_id not in token_buckets:
        token_buckets[user_id] = TokenBucket(capacity=10, refill_rate=1)  # Set the capacity and refill rate

    bucket = token_buckets[user_id]  # Get the user's token bucket

    if bucket.consume_tokens(req_tokens):
        return jsonify({"message": "Request successful."})
    else:
        return jsonify({"message": "Request failed. Insufficient tokens."}), 429

if __name__ == "__main__":
    app.run()

