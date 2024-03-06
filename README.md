<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <!--<a href="https://github.com/derekn4/CurfewBot?tab=readme-ov-file">
    <img src="curfew.png" alt="Logo" width="300" height="300">
  </a>-->

<h3 align="center">Towards Precise Detection of Toxic Pharmaceutical Drugs using Vision Transformers</h3>

  <p align="center">
    Utilizing Vision Transformers for multiclassification of Pharmaceutical drugs
    <br />
    <a href="https://github.com/derekn4/PillClassification"><strong>Explore the docs »</strong></a>
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#libaries-used">Libraries Used</a></li>
      </ul>
    </li>
    <li>
      <a href="#data-collection-and-preprocessing">Data Collection and Preprocessing</a>
      <ul>
        <li><a href="#subset-reason">Data Collection</a></li>
        <li><a href="#data-processing">Data Preprocessing</a></li>
      </ul>
    </li>
    <li>
      <a href="#vision-transformer">Vision Transformer</a>
      <ul>
        <li><a href="#initialization">Initialization</a></li>
        <li><a href="#dataset-building">Dataset Building</a></li>
        <li><a href="#validation-function">Validation Function</a></li>
        <li><a href="#fit-function">Fit Function</a></li>
        <li><a href="#early-stopping">Early Stopping</a></li>
        <li><a href="#training-loop">Training Loop</a></li>
      </ul>
    </li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
As modern health research continues to produce more complex pharmacological treatments, the public receives an ever-growing list of prospective tablets that can aid in treating various ailments and symptoms. While there are several benefits to these medical advancements, it is critical to realize the hazards associated with medications and their chemical combinations, one of them being the risk of medication errors by patients.

This project aims to employ Vision Transformers, a deep learning model, to identify pharmaceutical pills.
It employs fast data-preprocessing, data-augmentation techniques, and attention mechanisms to reliably recognize the kind of medicine given a picture of a pill.
The model performance evaluation metric focused on the most toxic drugs, using LD50 values.
  - LD50 value: LD50 is the amount of a material, given all at once, which causes the death of 50% (one half) of a group of test animals.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][Python.org]][Python-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Libraries Used
* HuggingFace
* Transformers
* Pytorch
* Pandas
* Sklearn
* numpy

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Data Collection and Preprocessing
- Install all necessary libraries to run pillImageDownload.py
- NOTE: the  National Library of Medicine consisted of 4,000 high-quality reference pills and 133,000 pictures captured by digital cameras on mobile phones.
  - ~2-3TB of data which we could not store or processes in GoogleColab

### Data Collection
- Makes requests from "https://data.lhncbc.nlm.nih.gov/public/Pills/index.html"
- Can only process 10 folders at a time before ConnectionTimeout (~5000 images)
- Searched for only .jpg images (usually smaller size) and calls download function
- Loops through the number of download links in the folder (ending with .jpg)
  - downloads each image and writes to a folder

- In ToxicityExctraction.ipynb, we use the official drug names to search for LD50 values on the "go.drugbank.com"
- We store the values in a CSV file to eventually add to our final dataset
- NOTE: Any drug that was unable to be collected from go.drugbank.com, manual searching would be done.


### Data Processing
- CSV Column Names: NDC11, Part, Image, Layout, Name, rat toxicity
- Add image paths to .csv file with ld50 values obtained from the toxicity .csv file
- Since images had to be collected in subsets, multiple folders were created
  - in order to accurately access during training, the column "Part" was added to help identify which folder the image would be found

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Vision Transformer
Early on in the development of our model, we tried various other ML models for Vision Classification. 
Most of these typical methods, including Convolution Neural Networks (CNNs), did not output great results.
Furthermore, they required too many parameters and even more training time that we did not have access to in order to potentially get any improvements.

Fortunately, the Vision Transformer was developed soon after the Transformer model.
The idea behind Vision Transformers is to treat images as sequences of patches, which are then processed by a transformer model. 
This approach showed promising results, demonstrating competitive performance compared to traditional CNNs on various image classification benchmarks.

### Initialization
- The "ViTForImageClassification.from_pretrained" method comes from the Hugging Face Transformers library
- It loads "google/vit-base-patch16-224", a base version of the ViT model trained on ImageNet
- "num_labels" is set to 230 because our dataset contained 230 unique pharmaceutical drugs
- The "id2label" and "label2id" dictionaries are used to map class indices to labels and vice versa
- The "ignore_mismatched_sizes" parameter is set to True to handle images with different sizes during training.

- Optimizer Initialization: The AdamW optimizer is used for training the model. It's initialized with the model's parameters and the specified learning rate (lr).

- Training Configuration: Several hyperparameters are defined for training:
  - num_epochs: The number of training epochs (set to 10).
  - eval_steps: Number of steps after which to perform evaluation during training.
  - record_steps: Number of steps after which to record training statistics.
  - save_checkpoint: Number of epochs after which to save model checkpoints.

- Loss Function Initialization: The nn.CrossEntropyLoss() function is used to define the loss criterion for multi-class classification. 


### Dataset Building
- Define a custom dataset class NaturalImageDataset for handling image data
- "init" function initializes the dataset object with:
  - the provided paths to images (path) and their corresponding labels (labels)
  - optional argument "tfms" which determines whether data augmentation should be applied during training (tfms=1) or validation/testing (tfms=0).

### Validation Function
- This function evaluates the model on a validation dataset (test_dataloader).
- It sets the model to evaluation mode (model.eval()) to disable dropout and batch normalization.
- For each batch in the validation dataset, it computes the loss and accuracy.
- The loss and accuracy metrics are then averaged over all batches and returned.

### Fit Function
- This function trains the model using a training dataset (train_dataloader).
- It sets the model to training mode (model.train()).
- For each batch in the training dataset, it performs the forward pass, computes the loss, and updates the model's weights using backpropagation.
- It computes and returns the average training loss and accuracy.

### Early Stopping
- This class implements early stopping based on the change in validation loss.
- It tracks the number of consecutive times the validation loss exceeds the training loss by a certain minimum delta (min_delta).
- If the tolerance threshold (tolerance) is reached, indicating that the validation loss consistently exceeds the training loss, it sets the early_stop flag to True, indicating that training should be stopped early.

### Training Loop
- A "StratifiedKFold" cross-validation loop is used to split the dataset into train and test sets for each fold
  - Within each fold, the model is trained and validated
  - various performance metrics are computed and stored for evaluation
    - precision
    - recall
    - F1-score
    - Matthews correlation coefficient (MCC)

- Steps inside the loop:
  - \textbf{Data Splitting}: The dataset is split into training and testing sets using StratifiedKFold.
  - Model Training and Validation: For each fold, the model is trained and validated for a maximum of 10 epochs. 
    - The "fit" function trains the model using the training data, while the validate function evaluates the model on the validation data.
  - Early Stopping: Early stopping is applied to prevent overfitting. 
    - If the validation loss decreases, the model's state is saved. 
    - If the validation loss does not improve for a certain number of epochs (as determined by the EarlyStopping class), training is stopped early
  - Performance Evaluation: 
    - After training and validation, various performance metrics (precision, recall, F1-score, MCC) are computed using the predicted labels (y_pred) and true labels (y_test) 
    - These metrics are then stored for each fold.
  - Visualization: Accuracy and loss plots are generated to visualize the model's performance during training and validation for each fold.


<!-- CONTACT -->
## Contact

Derek Nguyen 
- [LinkedIn](https://www.linkedin.com/in/derekhuynguyen/) 
- [Email](derek.nguyen99@gmail.com)
<br></br>
Project Link: [https://github.com/derekn4/PillClassification](https://github.com/derekn4/PillClassification)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Python.org]: https://www.python.org/static/img/python-logo.png
[Python-url]: https://www.python.org/about/website/