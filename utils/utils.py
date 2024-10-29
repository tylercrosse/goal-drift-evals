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