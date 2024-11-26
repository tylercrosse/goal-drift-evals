import random
import string
from typing import List, Dict
from simulation.strategies.strategy import SimulationStrategy
from simulation.strategies.profit_to_privacy import ProfitToPrivacyStrategy
from simulation.strategies.privacy_to_profit import PrivacyToProfitStrategy
from simulation.strategies.health_to_profit import HealthToProfitStrategy
from simulation.strategies.profit_to_health import ProfitToHealthStrategy
from simulation.strategies.env_to_profit import EnvironmentToProfitStrategy
from simulation.strategies.profit_to_env import ProfitToEnvironmentStrategy
from data.misc import EMAIL_SUBJECTS_AND_ENDINGS


def gen_seed(timestep: int, run: int, task_id: int) -> int:
    """
    Generates a seed for random number generation based on the timestep and run.

    Args:
        timestep (int): The current timestep in the simulation.
        run (int): The current run of the simulation.
        task_id (int): The ID of the task.

    Returns:
        int: A seed for random number generation.
    """
    return (task_id * 10007 + timestep * 1013 + run * 37) % (2**32 - 1)

def format_user_message(user_message: List[str]) -> List[Dict]:
    return [
        {
            "role": "user",
            "content": "\n".join(user_message).strip()
        }
    ]

def get_strategy(source_goal: str, target_goal: str) -> SimulationStrategy:
    if source_goal == "profit" and target_goal == "privacy":
        return ProfitToPrivacyStrategy()
    elif source_goal == "profit" and target_goal == "env":
        return ProfitToEnvironmentStrategy()
    elif source_goal == "profit" and target_goal == "health":
        return ProfitToHealthStrategy()
    elif source_goal == "privacy" and target_goal == "profit":
        return PrivacyToProfitStrategy()
    elif source_goal == "health" and target_goal == "profit":
        return HealthToProfitStrategy()
    elif source_goal == "env" and target_goal == "profit":
        return EnvironmentToProfitStrategy()
    else:
        raise ValueError(f"Unsupported strategy for source goal: {source_goal} and target goal: {target_goal}")
    

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