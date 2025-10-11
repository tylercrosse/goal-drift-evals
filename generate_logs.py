# %%
import os
from typing import Iterable, Optional
from utils.utils import load_checkpoint


def _extract_text(payload, allowed_types: Optional[Iterable[str]] = None) -> str:
    """Flatten structured content/reasoning payloads into printable text."""
    if payload is None:
        return ""

    if isinstance(payload, str):
        return payload

    segments = []
    if isinstance(payload, list):
        for item in payload:
            item_type = None
            item_text = None

            if isinstance(item, dict):
                item_type = item.get("type")
                item_text = item.get("text") or item.get("content")
            else:
                item_type = getattr(item, "type", None)
                item_text = getattr(item, "text", None) or getattr(item, "content", None)

            if allowed_types and item_type and item_type not in allowed_types:
                continue

            if item_text:
                segments.append(str(item_text))

    if segments:
        return "\n".join(segments)

    if allowed_types:
        return ""

    return str(payload)


def _normalize_for_comparison(text: str) -> str:
    return " ".join(text.split()) if text else ""

def extract_checkpoint_data_batch(base_results_dir: str = "results"):
    """Extract data from all checkpoints across multiple experiment folders."""
    # Iterate through all experiment folders
    for exp_folder in os.listdir(base_results_dir):
        exp_path = os.path.join(base_results_dir, exp_folder)
        if not os.path.isdir(exp_path):
            continue

        # Create logs subfolder within the experiment folder
        logs_dir = os.path.join(exp_path, "checkpoint_logs")
        os.makedirs(logs_dir, exist_ok=True)

        # Process all checkpoint files in this folder
        for checkpoint_file in os.listdir(exp_path):
            if not checkpoint_file.endswith('.pkl'):
                continue

            # Extract run number and timestep from filename
            # Expected format: checkpoint_run{run}_{timestep}.pkl
            try:
                parts = checkpoint_file.replace('.pkl', '').split('_')
                run = int(parts[1].replace('run', ''))
                timestep = int(parts[2])
            except (IndexError, ValueError):
                print(f"Skipping file with unexpected format: {checkpoint_file}")
                continue

            # Load and process checkpoint
            checkpoint_state = load_checkpoint(exp_path, run, timestep)
            if checkpoint_state is None:
                print(f"Failed to load checkpoint: {checkpoint_file}")
                continue

            # Generate log file path within the logs subfolder
            log_file = os.path.join(logs_dir, f"checkpoint_run{run}_step{timestep}.log")

            # Save message history to log file
            with open(log_file, 'w') as f:
                f.write(f"Message History for Run {run}, Timestep {timestep}\n")
                f.write("=" * 80 + "\n\n")
                
                messages = checkpoint_state.get('messages', [])
                for msg in messages:
                    # Handle both dict-style and object-style access
                    if hasattr(msg, 'get'):  # Dictionary-like object
                        role = msg.get('role', 'unknown')
                        content = msg.get('content', '')
                        tool_calls = msg.get('tool_calls', [])
                        reasoning = msg.get('reasoning', '')
                    else:  # Object with attributes
                        role = getattr(msg, 'role', 'unknown')
                        content = getattr(msg, 'content', '')
                        tool_calls = getattr(msg, 'tool_calls', [])
                        reasoning = getattr(msg, 'reasoning', '')
                    
                    f.write(f"[{role.upper()}]\n")
                    
                    # Handle different content formats for assistant messages
                    if role == "assistant":
                        assistant_text = _extract_text(content, allowed_types={"text"})
                        if assistant_text:
                            f.write(f"{assistant_text}\n")
                        reasoning_text = _extract_text(reasoning, allowed_types={"reasoning", "text"})
                        if reasoning_text and _normalize_for_comparison(reasoning_text) != _normalize_for_comparison(assistant_text):
                            f.write("\n[REASONING]\n")
                            f.write(f"{reasoning_text}\n")
                    else:
                        general_text = _extract_text(content)
                        if general_text:
                            f.write(f"{general_text}\n")
                    
                    # Handle tool calls
                    if tool_calls:
                        f.write("TOOL CALLS:\n")
                        for tool_call in tool_calls:
                            if isinstance(tool_call, dict):
                                function = tool_call.get('function', {})
                                name = function.get('name', 'unknown')
                                arguments = function.get('arguments', '')
                            else:
                                name = getattr(tool_call.function, 'name', 'unknown')
                                arguments = getattr(tool_call.function, 'arguments', '')
                            
                            f.write(f"- Function: {name}\n")
                            f.write(f"  Arguments: {arguments}\n")
                    
                    f.write("\n" + "-" * 80 + "\n\n")

            print(f"Log file saved: {log_file}")

if __name__ == "__main__":
    extract_checkpoint_data_batch()
# %%
