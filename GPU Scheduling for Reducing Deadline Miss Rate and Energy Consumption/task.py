import csv
import json
import os
import random
from typing import List



def generate_task_names(profile_directory_path):
    return [file.replace('.csv', '') for file in os.listdir(profile_directory_path) if file.endswith('.csv')]


def create_task_utils(task_names, util_sets, index):
    return {task_names[j]: util_sets[index][j] for j in range(len(task_names))}


def configure_task_profiles(task, util):
    for profile in task.task_profile.values():
        profile.exec_time = profile.max_exec_time
    task.exec_time = task.task_profile[1].exec_time
    task.utilization = util
    task.period = task.exec_time / util


class TaskProfile:
    def __init__(self, avg_exec_time: float, min_exec_time: float, max_exec_time: float, power_usage: float,
                 energy: float,
                 energy_window: float, exec_time: float) -> None:
        self.avg_exec_time = avg_exec_time
        self.min_exec_time = min_exec_time
        self.max_exec_time = max_exec_time
        self.exec_time = exec_time
        self.power_usage = power_usage
        self.energy = energy
        self.energy_window = energy_window



class Task:
    def __init__(self, name: str, arrival: float) -> None:
        self.name = name
        self.arrival = arrival
        self.period = None
        self.index = None
        self.cores = None
        self.utilization = None
        self.is_executed = False
        self.exec_time = None
        self.replace_core = False
        self.change_core = 0
        self.task_profile = {}

    def add_task_profile(self, sm_count: int, task_profile: TaskProfile) -> None:
        self.task_profile[sm_count] = task_profile


class TaskGen:

    def __init__(self):
        pass

    def uunifast_discard(self, n, u, nsets):
        sets = []
        while len(sets) < nsets:
            utilizations = []
            sum_u = u
            for i in range(1, n):
                next_sum_u = sum_u * random.random() ** (1.0 / (n - i))
                utilizations.append(sum_u - next_sum_u)
                sum_u = next_sum_u
            utilizations.append(sum_u)
            if all(ut <= 1 for ut in utilizations):
                sets.append(utilizations)
        return sets

    def extract_tasks_profile(self, data):
        core_count = int(data[0])
        avg_exec_time = float(data[1])
        min_exec_time = float(data[2])
        max_exec_time = float(data[3])
        power_usage = float(data[4])
        total_energy = float(data[5])
        energy_window = float(data[6])
        exec_time = max_exec_time
        return core_count, avg_exec_time, min_exec_time, max_exec_time, power_usage, total_energy, energy_window, exec_time

    def attach_profiles_to_job(self, job: Task) -> None:
        profiles_path = 'tasks_info'
        with open(os.path.join(profiles_path, f'{job.name}.csv'), 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for data in reader:
                core_count, avg_exec_time, min_exec_time, max_exec_time, power_usage, total_energy, energy_window,\
                exec_time = self.extract_tasks_profile(
                    data)
                exec_profile = TaskProfile(
                    avg_exec_time, min_exec_time, max_exec_time, power_usage, total_energy, energy_window, exec_time
                )
                job.add_task_profile(core_count, exec_profile)

    def generate_tasks(self, nsets):
        profile_directory_path = 'tasks_info'
        task_names = generate_task_names(profile_directory_path)

        util_sets = self.uunifast_discard(len(task_names), 2, nsets)
        print(len(task_names))
        all_tasks = []

        for i in range(nsets):
            task_utils = create_task_utils(task_names, util_sets, i)
            for task_name, utilization in task_utils.items():
                task = Task(name=task_name, arrival=0)
                self.attach_profiles_to_job(task)
                configure_task_profiles(task, utilization)
                all_tasks.append(task)

        random.shuffle(all_tasks)
        for i, task in enumerate(all_tasks):
            task.index = i

        return all_tasks
