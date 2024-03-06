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
      <a href="#trltoxic-code-how-it-works">trltoxic Code: How it works</a>
      <ul>
        <li><a href="#trl-args">Script Arguments and Configuration</a></li>
        <li><a href="#trl-dataset">Dataset Building</a></li>
        <li><a href="#trl-init">Model Initialization</a></li>
        <li><a href="#ppo-init">PPO Trainer Initialization</a></li>
        <li><a href="#reward">Reward Pipeline Setup</a></li>
        <li><a href="#ppo-train">PPO Training Loop and Model saving</a></li>
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
 

### Args Class
- After importing the Transformers Library and various Pytorch imports, the Args() class is initialized
  - This class defines a set of parameters for configuring the training process.
  - Parameters include: 
    - paths to model, tokenizer, and output directories
    - batch sizes
    - learning rates
    - gradient accumulation steps
    - number of epochs
    - and various other training hyperparameters.


### Construct Conversations Function
- "construct_conv" function: 
  - This function takes a conversation row, a tokenizer, and an optional argument eos (end-of-sentence)
  - Encodes each utterance in the conversation using the tokenizer and appends an end-of-sentence token if "eos" is True.
  - Conversation is flattened into a single list of token IDs
  - Function returns the flattened list of token IDs representing the conversation.

### ConversationDataset Class
- This class inherits from "Dataset", which is a PyTorch class for representing datasets in PyTorch.
- The "init" method initializes the dataset.
  - Takes parameters including a tokenizer, args (training arguments), df (Dataframe containing conversation data), and an optional "block_size" (sets the maximum length of the sequence)
  - Checks if cached features exist and loads them if overwrite_cache parameter is set to False
    - Otherwise, it creates features from the dataset and saves them.
  - Constructs examples from the dataset by iterating over each row in the DataFrame.
  - Encodes the conversation using the "construct_conv" function and adds it to the examples list if its length is less than block_size.

  - __len__ method returns the total number of examples in the dataset.
  - __getitem__ method retrieves an item from the dataset. It returns a PyTorch tensor containing the token IDs of the conversation at index item.

### Train Function
- This function is responsible for training the model.
- Initializes a TensorBoard writer for logging
- Sets up training batch size and collation function for the DataLoader
- Calculates total number of optimization steps based on the number of training examples, gradient accumulation steps, and number of epochs.
- Initializes optimizer and scheduler for learning rate scheduling
  - loads optimizer and scheduler states if they already exist
- Initializes mixed precision training if "args.fp16" is enabled.
- Sets up multi-GPU and distributed training if multiple GPUs are available.
- Iterates through epochs and batches, calculates loss, performs backpropagation, and updates model parameters.
- Logs training progress, evaluates the model periodically, and saves checkpoints.
- Manages the maximum number of steps for training.
- Closes the TensorBoard writer.

### Evalute Function
- This function evaluates the model performance on a validation dataset.
- Sets up the evaluation batch size and collation function for the DataLoader.
- Initializes a DataLoader for the evaluation dataset.
- Performs evaluation by iterating through batches, calculating loss, and accumulating evaluation metrics.
- Computes the perplexity metric based on the evaluation loss.
- Logs evaluation results and writes them to an output file.
- Returns the evaluation results as a dictionary.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## trltoxic Code: How it works
This script performs fine-tuning of a language model using the Proximal Policy Optimization (PPO) algorithm to generate less toxic text.
Hence, "trl" for Transformer Reinforcement Learning.

Below are some key steps and components of the script:

### Script Arguments and Configuration
- The script uses dataclass to define script arguments such as the model name, learning rate, mini-batch size, etc.
- It uses HfArgumentParser to parse the arguments and configure the PPO training.

### Dataset Building
- The build_dataset function is defined to prepare the dataset for training. 
- It loads the data from a CSV file, tokenizes it, filters out short samples, and splits it into training and validation sets.

### Model Initialization
- The script loads a pretrained language model for causal language modeling (LM). 
- It then creates a value head for the LM using AutoModelForCausalLMWithValueHead.

### PPO Trainer Initialization
- It initializes a PPOTrainer object, which orchestrates the PPO training process. 
- This includes setting up the model, reference model, tokenizer, optimizer, and dataset.

### Reward Pipeline Setup
- The script loads a toxicity detection model (RoBERTa) and tokenizer. 
- It defines the generation arguments and output length sampler.

### PPO Training Loop and Model saving
- Inside the training loop, it iterates over the dataset and generates responses using the policy model.
- Sentiment scores (toxicity labels) are computed for the generated responses using the toxicity model.
- PPO steps are performed to optimize the policy based on the generated responses and rewards.
- Training statistics are logged, and the model is periodically saved during training.
- After training, the script saves the trained PPO model.


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