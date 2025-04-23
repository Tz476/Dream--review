
## Student name:Yi Ding
## Student number: 24001375
## Project title:Dream Replay
## Link to project video recording: 
https://artslondon-my.sharepoint.com/:v:/g/personal/y_ding0120241_arts_ac_uk/EWiVSXVSQaxAshps_OkxsEYBGmZXOiRolo4aJE3mGI2K1A?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=rBbntu

### Introduction
In this project, I implemented an app called Dream Replay. The user enters the textual description of dream, and the app
generates the corresponding images.

### Techniques

(1) Interactive code

The project is made using streamlit which is a faster way to build data apps.

(2) AI frameworks

- Text-to-Image  
  `CompVis/stable-diffusion-v1-4`, a text-to-image model, runs in pytorch. In this project, it is used for visual
  representations of dreams.
- Chat model  
  The model `llama2:7b`, a chat model, runs in ollama. In this project, it is used for rewriting the textual description
  of the dreams.

### Usage

#### 1. Install environments


(1) Download and install ollama according to [ollama website](https://ollama.com/download).

(2) Download `llama2:7b` model using `ollama pull llama2:7b`.

(3) Install pytorch (choose proper CUDA version) using 
```
pip install torch --index-url https://download.pytorch.org/whl/cu124
``` 
(4) Install other python modules using 
```
pip install -r requirements.txt
```
#### 2. Run app

Before running, ensure that ollama is running and the `llama2:7b` model exists.  
First, run the command 
```
streamlit run app.py
```
on the console. Then you can visit the app using the browser.  
If this is the first run, the program will download `CompVis/stable-diffusion-v1-4`
from [HuggingFace](https://huggingface.co/CompVis/stable-diffusion-v1-4). This will take some time.
