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
    combined_string = f"{task_id}_{timestep}_{run}"
    return hash(combined_string)