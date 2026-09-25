"""
blocklist.py

This file just contains the blocklist of the JWT tokens. It will be imported by app and the logout resource so that tokens can be added to the blocklist when the user logs out.
"""

BLOCKLIST = set()            # The BLOCKLIST variable is defined as a set, which is a built-in data structure in Python that stores unique elements. In this case, it will be used to store the JWT tokens that have been invalidated or revoked, preventing them from being used for authentication in the future.

# Ideally, the blocklist should be stored in a database or a persistent storage mechanism (e.g., Redis) to ensure that it persists across application restarts. However, for simplicity, this implementation uses an in-memory set to store the blocklisted tokens.