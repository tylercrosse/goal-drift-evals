import json
from typing import List, Dict
from openai import OpenAI
from anthropic import Anthropic
import os
from anthropic.types import ToolUseBlock, TextBlock
from system_message import get_system_message
from simulation import Simulation
import pprint
import sys

oai_client = OpenAI()
api_key = os.environ.get("ANTHROPIC_API_KEY")
anthropic_client = Anthropic(api_key=api_key)


class SimulationManager:

    def __init__(self, model: str):
        self.model = model
        self.api_client = self._get_api_client()
        self.system_message = get_system_message()["content"]
        self.messages = [get_system_message()] if "gpt" in model.lower() else []

    def _get_api_client(self):
        if "gpt" in self.model.lower():
            return oai_client
        elif "claude" in self.model.lower():
            return anthropic_client
        else:
            raise ValueError(f"Unsupported model: {self.model}")
        
    def run_simulation(self, sim: Simulation, num_steps: int):
        for _ in range(num_steps):
            print(f"Timestep: {sim.current_timestep}")
            sim.initialize_timestep()
            user_message = sim.gen_user_message()
            print("USER MESSAGE:")
            pprint.pprint(user_message, width=150, compact=True)
            print("\n" * 2)
            print("RESPONSE MESSAGE:")
            self.messages.extend(user_message)

            timestep_start = sim.current_timestep
            while timestep_start == sim.current_timestep:
                self.single_step(self.model, sim)

            print("\n" * 5)
        
        return self._generate_result_dict(sim)
    
    def _generate_result_dict(self, sim: Simulation):
        return {
            "profit": sim.profit,
            "budget_limit_errors": sim.budget_limit_errors,
            "tool_call_errors": sim.tool_call_errors
        }
        
    def single_step(self, model: str, sim: Simulation, verbose: bool = True):
        """
        Prompts the given model to make business decisions and records these decisions in the simulation.

        Args:
            model (str): The model name to make decisions with.
            simulation (BusinessSimulation): The current simulation instance.
            messages (List[Dict]): List of messages exchanged during the simulation.
            decisions (List[Dict]): List of decisions for the current timestep.
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

            if "claude" in model.lower():
                input_tokens = response.usage.input_tokens
                output_tokens = response.usage.output_tokens
                input_tokens_cache_read = getattr(response.usage, 'cache_read_input_tokens', '---')
                input_tokens_cache_create = getattr(response.usage, 'cache_creation_input_tokens', '---')
                print(f"User input tokens: {input_tokens}")
                print(f"Output tokens: {output_tokens}")
                print(f"Input tokens (cache read): {input_tokens_cache_read}")
                print(f"Input tokens (cache write): {input_tokens_cache_create}")

                total_input_tokens = input_tokens + (int(input_tokens_cache_read) if input_tokens_cache_read != '---' else 0)
                percentage_cached = (int(input_tokens_cache_read) / total_input_tokens * 100 if input_tokens_cache_read != '---' and total_input_tokens > 0 else 0)

                print(f"{percentage_cached:.1f}% of input prompt cached ({total_input_tokens} tokens)")
            
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
            print(f"Error: {e}")


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
        if "gpt" in model.lower():
            response_message = response.choices[0].message
            self.messages.append(response_message)
            tool_calls = response_message.tool_calls
            response_message_content = response_message.content
        elif "claude" in model.lower():
            response_message = response
            print("Response message: ", response_message)
            self.messages.append({"role": "assistant", "content": response.content})
            tool_calls = [block for block in response.content if isinstance(block, ToolUseBlock)]
            response_message_content = "".join(block.text for block in response.content if isinstance(block, TextBlock))
        else:
            raise ValueError(f"Unsupported model: {model}")

        return tool_calls, response_message_content


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
    


if __name__ == "__main__":
    original_stdout = sys.stdout
    log_file_path = f'logs/task1_output_run{1}.txt'
    with open(log_file_path, 'w') as f:
        sys.stdout = f
        sim = Simulation(1, "gpt-4o-mini")
        sim_manager = SimulationManager("gpt-4o-mini")
        sim_manager.run_simulation(sim, 40)
    sys.stdout = original_stdout
