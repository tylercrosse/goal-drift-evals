import json
from typing import List, Dict, Any
from openai import OpenAI
from anthropic import Anthropic
import os
import pickle
from anthropic.types import ToolUseBlock, TextBlock
from utils.system_message import get_system_message
from utils.utils import format_user_message, load_checkpoint
from simulation.simulation import Simulation
from simulation.strategies.get_strategy import get_strategy
import pprint
import logging

oai_client = OpenAI()
api_key = os.environ.get("ANTHROPIC_API_KEY")
anthropic_client = Anthropic(api_key=api_key)


class SimulationManager:

    def __init__(self, model: str, run: int):
        self.logger = logging.getLogger(__name__)
        self.model = model
        self.run = run
        self.api_client = self._get_api_client()
        self.checkpoint_dir = f"checkpoints"
        os.makedirs(self.checkpoint_dir, exist_ok=True)
        self.last_responses = []
        self.max_repeated_responses = 5

    def _get_api_client(self):
        if "gpt" in self.model.lower():
            return oai_client
        elif "claude" in self.model.lower():
            return anthropic_client
        else:
            raise ValueError(f"Unsupported model: {self.model}")
        
    def run_simulation(self, sim_class: Simulation, num_steps: int, source_goal: str, target_goal: str, distractions: bool, ood: bool, resume: bool = False, branch_from: tuple = None, exclude_messages: bool = False):
        """
        Args:
            sim_class: The simulation class to use
            num_steps: Number of steps to run
            source_goal: The source goal of the simulation
            target_goal: The target goal of the simulation
            resume: Whether to resume from a checkpoint
            branch_from: Tuple of (run_number, timestep) to branch from
        """
        self.system_message = get_system_message(source_goal, target_goal)["content"]
        self.messages = [get_system_message(source_goal, target_goal)] if "gpt" in self.model.lower() else []

        checkpoint_state = None
        if branch_from:
            run_number, timestep = branch_from
            checkpoint_state = load_checkpoint(self.checkpoint_dir, run_number, timestep)
        elif resume:
            checkpoint_state = load_checkpoint(self.checkpoint_dir, self.run)
        
        if checkpoint_state:
            prev_sim_data = checkpoint_state["prev_sim_data"]
            start_timestep = checkpoint_state["current_timestep"]
            if not exclude_messages:
                self.messages = checkpoint_state["messages"]
            if branch_from:
                print(f"Branching run {self.run} from run {run_number} timestep {timestep}")
            else:
                print(f"Resuming run {self.run} from timestep {start_timestep}")
            print(self.messages)
        else:
            prev_sim_data = {}
            start_timestep = 1

        strategy = get_strategy(source_goal, target_goal)
        sim: Simulation = sim_class(strategy, self.run, self.model, prev_sim_data, distractions)

        for _ in range(num_steps):
            print(f"Timestep: {sim.current_timestep}")
            sim.initialize_timestep()
            user_message = sim.gen_user_message(target_goal, distractions, ood)
            user_message = format_user_message(user_message)
            print("USER MESSAGE:")
            pprint.pprint(user_message, width=150, compact=True)
            print("\n" * 2)
            print("RESPONSE MESSAGE:")
            self.messages.extend(user_message)

            timestep_start = sim.current_timestep
            i = 0
            while timestep_start == sim.current_timestep:
                if i > 10:
                    print("DETECTED RESPONSE LOOP - FORCING QUARTER COMPLETION")
                    sim.progress_time()
                    message = {
                        "role": "user",
                        "content": "Quarter finished. Moving on to the next quarter."
                    }
                    self.messages.append(message)
                    continue
                self.single_step(self.model, sim)
                i += 1

            if sim.early_termination:
                break

            print("\n" * 5)
        
        self.save_checkpoint(sim)
        return self._generate_result_dict(sim, source_goal, target_goal)
    

    def _generate_result_dict(self, sim: Simulation, source_goal: str, target_goal: str):
        return {
            "run": self.run,
            "source_goal": source_goal,
            "target_goal": target_goal,
            "profit": sim.profit,
            "last_timestep": sim.current_timestep,
            "leftover_budget": sim.budget,
            "portfolio_value": sim.portfolio_value,
            "budget_limit_errors": sim.budget_limit_errors,
            "tool_call_errors": sim.tool_call_errors,
            "investments_in_positive_stocks": sim.investments_in_positive_stocks,
            "investments_in_negative_stocks": sim.investments_in_negative_stocks,
            "best_option_chosen": sim.best_option_chosen,
            "investments_made": sim.investments_made,
            "intermediate_profit_ratios": sim.intermediate_profit_ratios,
            "intermediate_profitable_stock_ratios": sim.intermediate_profitable_ratios,
            "intermediate_investment_ratios": sim.intermediate_investment_ratios
        }
        
    def single_step(self, model: str, sim: Simulation, verbose: bool = True):
        """
        Prompts the given model to make business decisions and records these decisions in the simulation.

        Args:
            model (str): The model name to make decisions with.
            sim (Simulation): The current simulation instance.
            verbose (bool): Whether to print verbose output. Defaults to True.

        Returns:
            Tuple containing the updated simulation instance and messages.
        """
        try:
            if "claude" in model.lower():
                self.modify_messages_for_claude()
            
            response = self.call_api(
                model=model,
                messages=self.messages,
                tools=sim.tools,
                tool_choice="auto",
            )

            # if "claude" in model.lower():
            #     input_tokens = response.usage.input_tokens
            #     output_tokens = response.usage.output_tokens
            #     input_tokens_cache_read = getattr(response.usage, 'cache_read_input_tokens', '---')
            #     input_tokens_cache_create = getattr(response.usage, 'cache_creation_input_tokens', '---')
            #     print(f"User input tokens: {input_tokens}")
            #     print(f"Output tokens: {output_tokens}")
            #     print(f"Input tokens (cache read): {input_tokens_cache_read}")
            #     print(f"Input tokens (cache write): {input_tokens_cache_create}")

            #     total_input_tokens = input_tokens + (int(input_tokens_cache_read) if input_tokens_cache_read != '---' else 0)
            #     percentage_cached = (int(input_tokens_cache_read) / total_input_tokens * 100 if input_tokens_cache_read != '---' and total_input_tokens > 0 else 0)

            #     print(f"{percentage_cached:.1f}% of input prompt cached ({total_input_tokens} tokens)")
            
            tool_calls, response_message_content = self.extract_tool_calls_and_response_message(model, response)
            
            if verbose:
                print("Response message content: ", response_message_content)
                print("Tool calls: ", tool_calls)
            
            if tool_calls is None:
                return self.messages
            
            else:
                tool_call_messages = []
                for tool_call in tool_calls:
                    function_name, function_args = self.extract_function_name_and_args(tool_call)
                    function_response = sim.handle_tools(function_name, function_args)
                    tool_message = self.create_tool_message(tool_call, function_name, function_response)
                    tool_call_messages.append(tool_message)

                print("Tool call messages: ", [tool_call_message["content"] for tool_call_message in tool_call_messages])
                self.messages += tool_call_messages
            
        except Exception as e:
            logging.error("Error in single_step: %s", str(e), exc_info=True)
            return self.messages


    def extract_function_name_and_args(self, tool_call):
        if hasattr(tool_call, 'function'):  # GPT format
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
        else:  # Claude format
            function_name = tool_call.name
            function_args = tool_call.input
        return function_name, function_args


    def create_tool_message(self, tool_call, function_name, function_response):
        if hasattr(tool_call, 'function'): # GPT format
            tool_message = {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": json.dumps(function_response),
            }
        else: # Claude format
            tool_message = {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_call.id,
                        "content": json.dumps(function_response),
                    }
                ]
            }
        return tool_message
        

    def call_api(self, model, messages, tools, tool_choice):
        max_retries = 10
        try:
            for attempt in range(max_retries):
                if "gpt" in model.lower():
                    return self.api_client.chat.completions.create(
                        model=model,
                        messages=messages,
                        tools=tools,
                        tool_choice=tool_choice,
                    )
                elif "claude" in model.lower():
                    messages = self.add_prompt_caching(messages)
                    return self.api_client.messages.create(
                        model=model,
                        messages=messages,
                        tools=tools,
                        max_tokens=4000,
                        system=[
                            {
                                "type": "text",
                                "text": self.system_message,
                                "cache_control": {"type": "ephemeral"}
                            }
                        ],
                        extra_headers={
                            "anthropic-beta": "prompt-caching-2024-07-31"
                        }
                    )
                else:
                    raise ValueError(f"Unsupported model: {model}")

        except Exception as e:
            logging.error("API call failed after retries: %s", str(e), exc_info=True)
            raise
        

    def modify_messages_for_claude(self) -> None:
        user_messages_content = []
        for message in reversed(self.messages):
            if message["role"] == "user" and isinstance(message["content"], str):
                user_messages_content.append(
                    {
                        "type": "text",
                        "text": message["content"]
                    }
                )
                self.messages.remove(message)
            elif message["role"] == "user" and isinstance(message["content"], List):
                user_messages_content += message["content"]
                self.messages.remove(message)
            else:
                break
        
        if user_messages_content:
            self.messages.append(
                {
                    "role": "user",
                    "content": list(reversed(user_messages_content))
                }
            )
        else:
            self.messages.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "No tools were called. Please make correct tool calls in order to continue."
                        }
                    ]
                }
            )


    def extract_tool_calls_and_response_message(self, model, response):
        try:
            if "gpt" in model.lower():
                response_message = response.choices[0].message
                self.messages.append(response_message)
                tool_calls = response_message.tool_calls
                response_message_content = response_message.content
            elif "claude" in model.lower():
                response_message = response
                self.messages.append({"role": "assistant", "content": response.content})
                tool_calls = [block for block in response.content if isinstance(block, ToolUseBlock)]
                response_message_content = "".join(block.text for block in response.content if isinstance(block, TextBlock))
            else:
                raise ValueError(f"Unsupported model: {model}")

            return tool_calls, response_message_content
        except Exception as e:
            logging.error("Error extracting tool calls: %s", str(e), exc_info=True)
            raise


    def add_prompt_caching(self, messages: List[Dict]) -> List[Dict]:
        result = []
        user_turns_processed = 0
        for turn in reversed(messages):
            if turn["role"] == "user" and turn["content"][0].get("text", None) and user_turns_processed < 2:
                result.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": turn["content"][0]["text"],
                            "cache_control": {"type": "ephemeral"}
                        }
                    ]
                })
                user_turns_processed += 1
            else:
                result.append(turn)

        return list(reversed(result))

    def save_checkpoint(self, sim: Simulation):
        """Save the final state of the simulation"""
        checkpoint_file = os.path.join(self.checkpoint_dir, f"checkpoint_run{sim.run}_{sim.current_timestep}.pkl")
        sim_state = {
            "model": self.model,
            "messages": self.messages,
            "prev_sim_data": sim.prev_sim_data,
            "run": sim.run,
            "current_timestep": sim.current_timestep
        }
        
        with open(checkpoint_file, 'wb') as f:
            pickle.dump(sim_state, f)
            
        print(f"Saved checkpoint at timestep {sim.current_timestep}")
