# Hebrew Text Rendering Evaluation Results

## Scoring

| Model | שלום | פירגון | Score | Notes |
|-------|:----:|:------:|:-----:|-------|
| **Gemini 3 Pro** | 1 | 1 | **2/2** | Best performer - demonstrated contextual understanding (added relevant emojis for פירגון) |
| **Nano Banana Pro** | 1 | 1 | **2/2** | Reliable Hebrew rendering |
| Wan 2.5 | 0 | 1 | 1/2 | Partial success |
| Flux 2 | 0 | 0 | 0/2 | Hebrew mixed with Latin; nonsensical |
| Flux 2 Pro | 0 | 0 | 0/2 | Missing/nonsensical letters |
| Flux Dev | 0 | 0 | 0/2 | Wrong script (Arabic, English) |
| Imagen 4 | 0 | 0 | 0/2 | Hebrew letters but nonsensical words |
| Ideogram V2 | 0 | 0 | 0/2 | Russian-like text |
| Qwen Image | 0 | 0 | 0/2 | Invalid/nonsensical characters |
| SD 3.5 Large | 0 | 0 | 0/2 | Nonsensical |
| Recraft V3 | 0 | 0 | 0/2 | Invalid characters / English |
| Aura Flow | 0 | 0 | 0/2 | English / invalid Hebrew-like |

## Winners

1. **Gemini 3 Pro** (2/2) - Best overall with contextual understanding
2. **Nano Banana Pro** (2/2) - Reliable Hebrew rendering

## Models That Failed Both Tests (0/2)

- Flux 2
- Flux 2 Pro
- Flux Dev
- Imagen 4
- Ideogram V2
- Qwen Image
- SD 3.5 Large
- Recraft V3
- Aura Flow

## Detailed Notes

### Test 1: שלום (Shalom)

| Model | Pass | Notes |
|-------|:----:|-------|
| Gemini 3 Pro | 1 | Correct Hebrew |
| Nano Banana Pro | 1 | Correct Hebrew |
| Wan 2.5 | 0 | Valid Hebrew letters but wrong word |
| Flux 2 | 0 | Hebrew letters mixed with Latin/other characters |
| Flux 2 Pro | 0 | Missing letters |
| Flux Dev | 0 | Rendered Arabic instead of Hebrew |
| Imagen 4 | 0 | Hebrew characters but nonsensical word |
| Ideogram V2 | 0 | Russian-like text |
| Qwen Image | 0 | Resemblance to Hebrew but invalid characters |
| SD 3.5 Large | 0 | Nonsensical |
| Recraft V3 | 0 | Invalid characters |
| Aura Flow | 0 | Rendered word in English |

### Test 2: פירגון (Firgun)

| Model | Pass | Notes |
|-------|:----:|-------|
| Gemini 3 Pro | 1 | Correct word + thumbs up emojis complementing meaning (joy in sharing) - impressive context understanding |
| Nano Banana Pro | 1 | Correct word |
| Wan 2.5 | 1 | Correct and valid |
| Flux 2 | 0 | Valid Hebrew characters but nonsensical word |
| Flux 2 Pro | 0 | Valid letters but nonsensical word |
| Flux Dev | 0 | Random English words |
| Imagen 4 | 0 | Hebrew letters but nonsensical word |
| Ideogram V2 | 0 | Russian-like text |
| Qwen Image | 0 | Nonsensical |
| SD 3.5 Large | 0 | Nonsensical |
| Recraft V3 | 0 | Random English word |
| Aura Flow | 0 | Hebrew-like characters but don't conform to script |
