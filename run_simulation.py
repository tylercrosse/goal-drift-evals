import sys
from manage_simulation import SimulationManager
from simulation.default_simulation import DefaultSimulation
import argparse
from multiprocessing import Pool, Manager
import os
import json
import logging

class LogFileWriter:
    def __init__(self, log_file):
        self.log_file = log_file

    def write(self, message):
        self.log_file.write(message)
        self.log_file.flush()  # Ensure immediate writing

    def flush(self):
        self.log_file.flush()

def setup_logging(run):
    log_file_path = f'logs/task1_output_run{run}.txt'
    
    # Clear the file at the start of a new run
    with open(log_file_path, 'w') as f:
        f.write('')  # Clear the file
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
    
    # Create file handler in append mode
    file_handler = logging.FileHandler(log_file_path, mode='a')
    file_handler.setFormatter(formatter)
    
    # Get root logger and remove existing handlers
    root_logger = logging.getLogger()
    root_logger.handlers = []
    
    # Add file handler to root logger
    root_logger.addHandler(file_handler)
    root_logger.setLevel(logging.INFO)  # Capture all levels of logs
    
    # Create a single file writer for both stdout and stderr
    log_file = open(log_file_path, 'a')  # Use append mode for subsequent writes
    file_writer = LogFileWriter(log_file)
    
    # Redirect both stdout and stderr to the log file
    sys.stdout = file_writer
    sys.stderr = file_writer
    
    return log_file  # Return for cleanup in finally block

def run_single_simulation(run, model, results_file, lock, resume):
    try:
        setup_logging(run)
        sim_manager = SimulationManager(model, run)
        result = sim_manager.run_simulation(DefaultSimulation, 10, resume)
        
        # Save results with lock
        with lock:
            if not os.path.exists(results_file) or os.path.getsize(results_file) == 0:
                with open(results_file, 'w') as f:
                    json.dump({}, f)

            with open(results_file, 'r') as f:
                results = json.load(f)
                
            if "Task 1" not in results:
                results["Task 1"] = {}
            if model not in results["Task 1"]:
                results["Task 1"][model] = []
            results["Task 1"][model].append(result)

            with open(results_file, 'w') as f:
                json.dump(results, f, indent=4)
        
        return result
    except Exception as e:
        logging.error("Error in simulation run %d: %s", run, str(e), exc_info=True)
        raise
    finally:
        # Close the stdout file
        if hasattr(sys.stdout, 'close'):
            sys.stdout.close()

if __name__ == "__main__":
    original_stdout = sys.stdout
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gpt-4o-mini", help="Model to evaluate")
    parser.add_argument("--results_file", default="results.json", help="File path for the results JSON")
    parser.add_argument("--parallel", action="store_true", help="Enable parallel execution of runs")
    parser.add_argument("--runs", nargs="+", type=int, 
                        help="Specific run numbers to execute. Example: --runs 1 5 7")
    parser.add_argument("--run_range", nargs=2, type=int, default=None, 
                        help="Range of runs to perform (inclusive). Example: --run_range 1 5")
    parser.add_argument("--resume", action="store_true",
                        help="Resume from last checkpoint if available")
    args = parser.parse_args()

    if args.runs:
        run_list = args.runs
    elif args.run_range:
        start_run, end_run = args.run_range
        run_list = list(range(start_run, end_run + 1))
    else:
        run_list = [1, 2]
    
    # Create a manager to share the lock between processes
    manager = Manager()
    lock = manager.Lock()

    if args.parallel:
        with Pool() as pool:
            run_results = pool.starmap(run_single_simulation, 
                                     [(run, args.model, args.results_file, lock, args.resume) for run in run_list])
    else:
        run_results = []
        for run in run_list:
            result = run_single_simulation(run, args.model, args.results_file, lock, args.resume)
            run_results.append(result)

    sys.stdout = original_stdout
    print(f"All runs from {run_list[0]} to {run_list[-1]} completed. Results have been saved to {args.results_file}")