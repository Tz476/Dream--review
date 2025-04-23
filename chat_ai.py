import ollama

MODEL_NAME = 'llama2:7b'


def initialize():
    # Initialize the model
    try:
        for model in ollama.list().models:
            if MODEL_NAME == model.model:
                return
    except:
        return 'Please start ollama'

    return 'Miss %s in ollama' % MODEL_NAME


def rewrite(sentence):
    """
    Rewrite the sentence using llama2
    """
    response = ollama.chat(model=MODEL_NAME,
                           messages=[
                               {"role": "system",
                                "content": "Rewrite the following text to make it more dreamlike "
                                           "and suitable as input for a text-to-image model, "
                                           "with a word limit of 30 words.", },
                               {"role": "user", "content": sentence}])
    text_prompt = response["message"]["content"].strip()
    return text_prompt
