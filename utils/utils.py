import random
import string
import os
import glob
import pickle
import tiktoken

from typing import List, Dict
from data.misc import EMAIL_SUBJECTS_AND_ENDINGS
from config import get_api_client


def gen_seed(timestep: int, run: int) -> int:
    """
    Generates a seed for random number generation based on the timestep and run.

    Args:
        timestep (int): The current timestep in the simulation.
        run (int): The current run of the simulation.

    Returns:
        int: A seed for random number generation.
    """
    h = timestep + (run << 16)
    h = (h * 0x3243f6a8 + 1) % (2**32)  # Multiply with golden ratio
    h = h ^ (h >> 16)  # Mix high bits into low bits
    h = (h * 0x1db8832d + 1) % (2**32)  # Another multiplication
    return h % (2**32 - 1)

def format_user_message(user_message: List[str]) -> List[Dict]:
    return [
        {
            "role": "user",
            "content": "\n".join(user_message).strip()
        }
    ]
    
def gen_random_string(random_gen: random.Random):
    """
    Generate a random string with a length between 5 and 12 letters.
    """
    length = random_gen.randint(5, 12)
    return ''.join(random_gen.choice(string.ascii_letters) for _ in range(length))

def gen_random_sentence(random_gen: random.Random):
    """
    Generate a random sentence with a length between 5 and 12 words out of random words.
    """
    length = random_gen.randint(5, 12)
    words = [gen_random_string(random_gen) for _ in range(length)]
    sentence = ' '.join(words)
    return sentence.capitalize() + '.'

def gen_random_email(random_gen: random.Random):
    """
    Generate a random email with a subject and ending.
    """
    email_subject_and_ending = random_gen.choice(EMAIL_SUBJECTS_AND_ENDINGS)
    email_text = ""
    for _ in range(random_gen.randint(5, 15)):
        email_text += gen_random_sentence(random_gen) + " "
    email_text = email_text.strip()
    return f"Subject: {gen_random_sentence(random_gen)}\n\n{email_text}\n\n{email_subject_and_ending['ending']}"

def gen_random_help_request(random_gen: random.Random):
    """
    Generate a random help request.
    """
    text = ""
    for _ in range(random_gen.randint(5, 15)):
        text += gen_random_sentence(random_gen) + " "
    text = text.strip()
    return text

def load_checkpoint(checkpoint_dir: str, run: int, specific_timestep: int = None):
    """Load the checkpoint for a specific run and optionally a specific timestep"""
    checkpoint_files = glob.glob(os.path.join(checkpoint_dir, f"checkpoint_run{run}_*.pkl"))
    if not checkpoint_files:
        return None
        
    if specific_timestep:
        matching_checkpoints = [f for f in checkpoint_files 
                            if int(f.split('_')[-1].replace('.pkl', '')) == specific_timestep]
        if not matching_checkpoints:
            raise ValueError(f"No checkpoint found for run {run} at timestep {specific_timestep}")
        checkpoint_file = matching_checkpoints[0]
    else:
        # Get the checkpoint with the highest timestep
        checkpoint_file = max(checkpoint_files, 
                            key=lambda x: int(x.split('_')[-1].replace('.pkl', '')))
    
    with open(checkpoint_file, 'rb') as f:
        return pickle.load(f)
    

def build_random_text_to_token_target(model: str, random_gen: random.Random, target_tokens: int) -> str:
    """
    Builds text by generating random sentences until reaching a target token count.
    
    Args:
        random_gen (random.Random): Random number generator instance
        target_tokens (int): Target number of tokens to reach
    
    Returns:
        str: Generated text that reaches but doesn't exceed the target token count
    """        
    text = ""
    test_message = []
    current_tokens = 0
    
    while current_tokens < target_tokens:
        new_sentence = gen_random_sentence(random_gen)
        test_text = text + (" " if text else "") + new_sentence
        
        # Format as user message and count tokens
        test_message = format_user_message([test_text])
        tokens = count_messages_tokens(model, test_message, "", [])
        
        if tokens > target_tokens:
            break
            
        text = test_text
        current_tokens = tokens
    
    return test_message


def build_dots_to_token_target(model: str, random_gen: random.Random, target_tokens: int) -> str:
    """
    Builds a string of dots that results in exactly the target token count using:
    1. Initial estimate with target_tokens dots
    2. Calculate ratio needed and apply it to get close to target
    3. Fine-tune by adding individual dots
    
    Args:
        model (str): The model to use for token counting
        random_gen (random.Random): Random number generator instance (unused)
        target_tokens (int): Target number of tokens to reach
    
    Returns:
        List[Dict]: Formatted message that contains exactly the target token count
    """
    # Initial test with target_tokens dots
    text = " ." * target_tokens
    return format_user_message([text])
    

def count_messages_tokens(model: str, messages: List[Dict], system_message: str, tools: List[Dict]) -> int:
    """Count the total number of tokens in messages"""
    total_tokens = 0
    api_client = get_api_client(model)

    if "gpt" in model.lower():
        for message in messages:
            encoding = tiktoken.encoding_for_model(model) if "gpt" in model.lower() else None
            # Count message content
            content = message["content"] if isinstance(message, dict) else message.content
            if isinstance(content, str):
                total_tokens += len(encoding.encode(content))
            elif isinstance(content, list):
                for content_item in content:
                    if isinstance(content_item, dict) and "text" in content_item:
                        total_tokens += len(encoding.encode(content_item["text"]))
            
            # Count function calls if present
            tool_calls = message.get("tool_calls") if isinstance(message, dict) else getattr(message, "tool_calls", None)
            if tool_calls:
                for tool_call in tool_calls:
                    if isinstance(tool_call, dict):
                        name = tool_call["function"]["name"]
                        args = tool_call["function"]["arguments"]
                    else:
                        name = tool_call.function.name
                        args = tool_call.function.arguments
                    
                    total_tokens += len(encoding.encode(name))
                    total_tokens += len(encoding.encode(args))

    elif "claude" in model.lower():
        response = api_client.messages.count_tokens(
            model=model,
            tools=tools,
            system=system_message,
            messages=messages,
        )
        total_tokens = response.input_tokens

    return total_tokens