from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from .args import get_arguments

import time

def current_milli_time():
    return round(time.time() * 1000)

tokenizer = ""
model = ""

print(get_arguments().model)

if get_arguments().model == "default":
    tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
    model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
else:
    tokenizer = AutoTokenizer.from_pretrained(get_arguments().model, local_files_only=get_arguments().local)
    model = AutoModelForCausalLM.from_pretrained(get_arguments().model, local_files_only=get_arguments().local)
    
chat_history_ids = ""
time_since_last_gen = current_milli_time()

class ChatAI:
    """Class to generate responses from the AI"""
    def generate_response(self, input, args):
        """Generate a response from the AI"""
        global chat_history_ids
        global time_since_last_gen

        # Commands
        if input.lower() == "/reset":
            chat_history_ids = ""
            return "**Reset History!**"

        # If it has been 10 minutes since the last message, clear history.
        if current_milli_time() - time_since_last_gen > (1000*60*10):
            chat_history_ids = ""

        # Set time since last generated response to current time
        time_since_last_gen = current_milli_time()

        # encode the new user input, add the eos_token and return a tensor in Pytorch
        new_user_input_ids = tokenizer.encode(input + tokenizer.eos_token, return_tensors='pt')

        # append the new user input tokens to the chat history
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if not chat_history_ids == "" else new_user_input_ids

        max_length = 1000
        min_length = bot_input_ids.shape[-1] + 2

        # Whether or not the model should use the past last key/values attentions
        # (if applicable to the model) to speed up decoding.
        use_cache = True

        # Whether or not to clean up the potential extra spaces in the text output.
        clean_up_tokenization_spaces = True

        # Exponential penalty to the length. 1.0 means no penalty.
        # Set to values < 1.0 in order to encourage the model to generate shorter sequences,
        # to a value > 1.0 in order to encourage the model to produce longer sequences.
        length_penalty = 1

        # Default: 1 - 1.3
        repetition_penalty = 1

        # generate a response
        chat_history_ids = model.generate(bot_input_ids, pad_token_id=tokenizer.eos_token_id, 
            no_repeat_ngram_size=2, max_length=max_length, min_length=min_length,
            do_sample=True, temperature=args.temperature, top_k=args.top_k, top_p=args.top_p,
            repetition_penalty=repetition_penalty,
            use_cache=use_cache, clean_up_tokenization_spaces=clean_up_tokenization_spaces, length_penalty=length_penalty
        )

        # pretty print last output tokens from bot
        generated_response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

        # if history context is over an amount, remove messages from an index 
        if self.history_length(chat_history_ids) >= args.max_history:
            chat_history_ids = self.strip_history(chat_history_ids, 3)
        
        return generated_response

    def strip_history(self, history, index):
        """Get the chat history and remove messages from an index"""
        new_history = tokenizer.decode(history[0], skip_special_tokens=False) # decode the history
        new_history = new_history.split(tokenizer.eos_token)[index:] # split and strip the history
        new_history = self.intersperse(new_history, tokenizer.eos_token) # add tokenizer between each list item 
        new_history = "".join(new_history) # convert back to string
        new_history = tokenizer.encode(new_history + tokenizer.eos_token, return_tensors='pt') # encode the new history
        return new_history

    def history_length(self, history):
        """Get length of the chat history"""
        decoded_history = tokenizer.decode(history[0], skip_special_tokens=False) # decode the history
        history_split = decoded_history.split(tokenizer.eos_token) # split the history so we can count it
        history_length = len(history_split)-1  # remove one from the final number as there is an empty string at the end of the list
        return history_length

    def intersperse(self, lst, item):
        """Add item between each existing item in list"""
        result = [item] * (len(lst) * 2 - 1)
        result[0::2] = lst
        return result
