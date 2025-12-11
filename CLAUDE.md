I created this repository to run a quick evaluation to see which of the major text image models could accurately render Hebrew text in a image. 

I'd like to evaluate two "words". The prompts are deliberately simple. 

In all cases, the aspect ratio should be 16:9. 

Each model should be tested for each word. 

Additionally:

After the images are generated, they should be saved into the repository but rendered with the model name beneath the image in a white row.

The model name to be rendered should not include the vendor and should be normalised.

For instance, the model id for seedream-4 is bytedance/seedream-4

That can be written as Seedream 4

The purpose of the annotation beneath the generated image is to identify which model generated it visually. Therefore, use large text. 