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
      <a href="#dialogpt-code-how-it-works">DioloGPT Code: How it works</a>
      <ul>
        <li><a href="#data-processing">Data Processing</a></li>
        <li><a href="#args-class">Args Class</a></li>
        <li><a href="#conv-funct">Construct Conversations Function</a></li>
        <li><a href="#conv-class">ConversationDataset Class</a></li>
        <li><a href="#train">Train Function</a></li>
        <li><a href="#evalute">Evaluate Function</a></li>
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

Dataset Curation using Few-shot learning for Empathetic Conversational Agents.
In this project, we aimed to build a conversational agent for mental health applications that is more “human-like” in its  approach and has the following characteristics:
- Is empathetic 
- Has a sense of morality 
- Is self-aware (Knows when to not respond)
- Doesn’t generate triggering responses

Specifically, we graded the final model on these categories through Human Evaluations:
- Natural Flow
- Context Dependence
- Topic Consistency
- Speaker Consistency
- Specificity
- Interestingness

Our primary objective is to develop an empathetic conversational agent that is specifically tailored for self-care and emotional support settings.


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


## DioloGPT Code: How it works
- Install all necessary libraries to run DialoGPT.ipynb

### Data Processing
- Dataset is pulled from local storage "FB_Multi_Train.csv"
- Preprocessing of Data required:
 - Tokenization
 - End-of-Sentence Token addition
 - Flattening Conversations
 - Padding
 - Caching Features

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