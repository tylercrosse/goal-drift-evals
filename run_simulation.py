import sys
from manage_simulation import SimulationManager
from simulation import Simulation
import argparse
from multiprocessing import Pool, Manager
import os
import json

def run_single_simulation(run, model, results_file, lock):
    log_file_path = f'logs/task1_output_run{run}.txt'
    with open(log_file_path, 'w') as f:
        sys.stdout = f
        sim = Simulation(run, model)
        sim_manager = SimulationManager(model, run)
        result = sim_manager.run_simulation(sim, 30)
        
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
                                     [(run, args.model, args.results_file, lock) for run in run_list])
    else:
        run_results = []
        for run in run_list:
            result = run_single_simulation(run, args.model, args.results_file, lock)
            run_results.append(result)

    sys.stdout = original_stdout
    print(f"All runs from {run_list[0]} to {run_list[-1]} completed. Results have been saved to {args.results_file}")