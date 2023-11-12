I have a dataset of diseases followed by their respective symptoms.
All data is standarized accordingly to their ICD code. Both the disease and the symptom.
I want to create a ML model that predicts the correct disease given the input list of symptoms.

Each disease has between 10 to 25 different symptoms.
Furthermore, I want the structure and ICD code hierarchy to be encompassed in the decision making. This is, a symptom with a ICD code A100 is closer to A103 then it is to B100

I have 300 diseases in the dataset.

Answer these three question:
- Which type of model should I aim to?
- Which type of classification should I approach?
- Do I do it with my original dataset or with and augmented dataset variation?




Given the description of your problem, here are the answers to your questions:

    Which type of model should I aim for?

    You should aim for models that can handle hierarchical structures in the data, given that you're interested in considering the ICD code hierarchy.

        Hierarchical Models: These are designed to handle data that has some form of hierarchy or tree structure. A popular method within this category is Hierarchical Multi-Label Classification (HMLC) where classes (in your case, diseases) are organized in a hierarchical manner.

        Embedding-based Models: Another approach is to convert ICD codes into dense vectors (embeddings) that capture the similarity between different codes. For example, you can use techniques like word embeddings (Word2Vec, FastText) tailored for ICD codes, so that A100 is closer to A103 than B100 in the embedding space. Once converted, you can use classical models like Random Forests, Gradient Boosted Trees, or even deep learning models.

        Deep Learning Models: If you have a large amount of data, deep learning models like Neural Networks can also be considered, as they can potentially learn the intricate relationships between symptoms and diseases. Especially, architectures like attention mechanisms can weigh the importance of each symptom differently when predicting diseases.

    Which type of classification should I approach?

    Given that you want to predict a single disease based on a set of symptoms, you're essentially looking at a multiclass classification problem, where each disease is a separate class.

    Do I do it with my original dataset or with an augmented dataset variation?

    This largely depends on the size and quality of your dataset:

        Size: If you feel the dataset might not be large enough to capture the nuances of each disease, data augmentation can be beneficial. Techniques specific to your case might include creating synthetic symptom combinations or using bootstrapping.

        Class Imbalance: If some diseases are underrepresented in your dataset, data augmentation or resampling techniques can help balance the distribution.

        Noise and Errors: If the dataset contains noise (e.g., wrongly coded symptoms or diseases), data cleaning and preprocessing should be the priority before augmentation.

        Augmentation with Embeddings: If you use embedding-based models, you might indirectly augment the data by translating discrete ICD codes into continuous embedding vectors. These embeddings might capture similarities and nuances which the raw codes may not represent explicitly.

In summary, given the hierarchical nature of ICD codes and the need to predict diseases based on symptoms, a combination of hierarchical models and embedding-based models could be beneficial. Starting with the original dataset is a good idea, but depending on its size and quality, data augmentation might be useful. As with most ML problems, iterative experimentation will be crucial to find the best model and data handling strategy.
