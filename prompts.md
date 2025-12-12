# Prompts Used

## Series 1: English Prompts

### שלום (Shalom)
```
A banner graphic with the word שלום written in large font
```

### פירגון (Firgun)
```
A banner graphic with the word פירגון written in large font
```

## Series 2: Hebrew Prompts

### שלום (Shalom)
```
גרפיקה עם המילה שלום בגופן גדול
```

### פירגון (Firgun)
```
גרפיקה עם המילה פירגון בגופן גדול
```

## Evaluation Criteria

For reliable text generation within an image:

### Pass
- Accurate text (no pseudotext)
- Standard unvowelised block script Hebrew (unless specifically requested, the model should not add vowels or render in cursive)
- RTL: text rendered right-to-left

### Fail
- Text correct but offset to the left / rendered LTR
- Pseudotext (Hebrew-like characters that don't form the correct word)
- Unrequested vowelisation
- Wrong script (Arabic, Russian, Latin, etc.)
