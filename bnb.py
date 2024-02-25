import numpy as np

class Node:
    def __init__(self, level, assigned_tasks, task_assignment, machine_load):
        self.level = level
        self.assigned_tasks = assigned_tasks
        self.task_assignment = task_assignment
        self.machine_load = machine_load

def calculate_upper_bound(processing_times, task_assignment, machine_load):
    max_load = max(machine_load)
    return max_load + max(processing_times[task_assignment])

def calculate_lower_bound(processing_times, task_assignment, machine_load):
    lower_bound = sum(machine_load)
    for i in range(len(processing_times)):
        if i not in task_assignment:
            lower_bound += min(processing_times[i])
    return lower_bound

def branch_and_bound(processing_times):
    num_jobs = len(processing_times)
    num_machines = len(processing_times[0])
    
    initial_node = Node(0, [], [-1] * num_jobs, [0] * num_machines)
    active_nodes = [initial_node]
    upper_bound = float('inf')
    
    while active_nodes:
        current_node = active_nodes.pop(0)
        if current_node.level == num_jobs:
            upper_bound = min(upper_bound, max(current_node.machine_load))
        else:
            for i in range(num_machines):
                next_load = current_node.machine_load[i] + processing_times[current_node.level][i]
                if next_load < upper_bound:
                    next_task_assignment = current_node.task_assignment.copy()
                    next_task_assignment[current_node.level] = i
                    next_machine_load = current_node.machine_load.copy()
                    next_machine_load[i] = next_load
                    next_node = Node(current_node.level + 1, 
                                     current_node.assigned_tasks + [current_node.level], 
                                     next_task_assignment, 
                                     next_machine_load)
                    active_nodes.append(next_node)
    
    return upper_bound

if __name__ == "__main__":
    # Example processing times for 20 jobs and 5 machines
    np.random.seed(379008056)
    processing_times = np.random.randint(1, 20, size=(5, 20))
    print("Processing times:\n")
    print(processing_times)

    upper_bound = branch_and_bound(processing_times)
    print("Upper Bound:", upper_bound)
    lower_bound = calculate_lower_bound(processing_times, [], [0] * 5)
    print("Lower Bound:", lower_bound)
