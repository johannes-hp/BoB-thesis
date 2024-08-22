import os
import matplotlib.pyplot as plt
import seaborn as sns

path = os.path.join( os.path.dirname ( __file__), os.path.pardir, 'epitomes')
chars = []
tokens = []

for file in os.listdir(path):
    with open(os.path.join(path, file), 'r', encoding='utf-8') as f:
        text = f.read()
        chars.append(len(text))
        text_tokens = text.split()
        tokens.append(len(text_tokens))

total_chars = sum(chars)
avg_chars = total_chars/len(chars)
total_tokens = sum(tokens)
avg_tokens = total_tokens/len(tokens)

window_size = 10
i = 0
moving_avg_tokens = []

while i < len(tokens) - window_size + 1:
    
    window = tokens[i: i + window_size]
    window_avg = sum(window)/window_size
    moving_avg_tokens.append(window_avg)
    i += 1

print('CHARACTERS')
print(f'Total characters in BoB: {total_chars:.2f}')
print(f'Mean characters per epitome: {avg_chars:.2f}')
print('TOKENS')
print(f'Total tokens in BoB: {total_tokens}')
print(f'Mean tokens per epitome: {avg_tokens:.2f}')

# fig, axes = plt.subplots(1,2)
# sns.lineplot(tokens, ax=axes[0])
# axes[0].set_title('Tokens in each epitome')
# sns.lineplot(moving_avg_tokens, ax=axes[1])
# axes[1].set_title('Rolling mean of tokens per epitome (window=10)')
# plt.show()