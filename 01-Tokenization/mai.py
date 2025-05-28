import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hello, I'm Utkarsh"

tokens= enc.encode(text);

print("Tokens", tokens);
tokens = [13225, 11, 5477, 21952, 10428, 1116]
decoded = enc.decode(tokens);

print("Decoded", decoded)
