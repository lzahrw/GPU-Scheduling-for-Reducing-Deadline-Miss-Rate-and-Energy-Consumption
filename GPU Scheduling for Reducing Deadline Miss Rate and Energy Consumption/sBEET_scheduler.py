import heapq
import math
from plotting import plot_tasks


class SBEETScheduler:

    def __init__(self, tasks, hyper_period):
        self.hyper_period = hyper_period
        self.tasks = tasks
        self.queue = []
        # initialize the queue
        for task in self.tasks:
            heapq.heappush(self.queue, task)

    def get_tasks_for_available_cores(self, available_cores):
        task1 = heapq.heappop(self.queue)
        task2 = heapq.heappop(self.queue)

        best_tasks = {"task1": None, "task2": None, "best_time": math.inf, "best_power": math.inf}
        for core in range(5, 5 - available_cores, -1):
            total_exec_time, total_power, task1_exec_time, task2_exec_time = \
                self.calculate_execution_and_power(task1, task2, core)

            if total_exec_time < best_tasks["best_time"]:
                best_tasks, final = self.update_best_tasks \
                    (best_tasks, task1, task2, total_exec_time, total_power, core, task1_exec_time, task2_exec_time)
            elif best_tasks["best_time"] == total_exec_time:
                if total_power < best_tasks["best_power"]:
                    best_tasks, final = \
                        self.update_best_tasks(best_tasks, task1, task2, total_exec_time, total_power,
                                               core, task1_exec_time, task2_exec_time)

        first_task, second_task = self.assign_task(final)
        if second_task.cores != available_cores:
            first_task.replace_core = True
            first_task.change_core = available_cores - second_task.cores
        return first_task, second_task

    def calculate_execution_and_power(self, task1, task2, core):
        task1_exec_time = task1.task_profile[core].exec_time
        task2_exec_time = task2.task_profile[6 - core].exec_time
        total_exec_time = task1_exec_time + task2_exec_time
        task1_power = task1.task_profile[core].power_usage
        task2_power = task2.task_profile[6 - core].power_usage
        total_power = task1_power + task2_power
        # print(total_exec_time, total_power, task1_exec_time, task2_exec_time)
        return total_exec_time, total_power, task1_exec_time, task2_exec_time

    def update_best_tasks(self, best_tasks, task1, task2, total_exec_time, total_power, core, task1_exec_time,
                          task2_exec_time):
        best_tasks.update({"task1": task1, "task2": task2, "best_time": total_exec_time, "best_power": total_power})
        final = (
            (task1, core, task1_exec_time), (task2, 6 - core, task2_exec_time))
        return best_tasks, final

    def get_best_task_choice(self, task1, task2):
        final = None
        best_tasks = {"task1": None, "task2": None, "best_time": math.inf, "best_power": math.inf}
        for core in range(5, 0, -1):
            total_exec_time, total_power, task1_exec_time, task2_exec_time = \
                self.calculate_execution_and_power(task1, task2, core)

            if total_exec_time < best_tasks["best_time"]:
                best_tasks, final = self.update_best_tasks \
                    (best_tasks, task1, task2, total_exec_time, total_power, core, task1_exec_time, task2_exec_time)
            elif best_tasks["best_time"] == total_exec_time:
                if total_power < best_tasks["best_power"]:
                    best_tasks, final = \
                        self.update_best_tasks(best_tasks, task1, task2, total_exec_time, total_power,
                                               core, task1_exec_time, task2_exec_time)

        task1, task2 = self.assign_task(final)
        return task1, task2

    def assign_task(self, final):
        task1 = final[0][0]
        task1.cores = final[0][1]
        task1.exec_time = final[0][2]
        task2 = final[1][0]
        task2.cores = final[1][1]
        task2.exec_time = final[1][2]
        return task1, task2

    def find_best_tasks(self, available_cores):
        if available_cores == 0:
            task1 = heapq.heappop(self.queue)
            task2 = heapq.heappop(self.queue)
            return task1, task2
        elif available_cores != 6:
            return self.get_tasks_for_available_cores(available_cores)
        else:
            task1 = heapq.heappop(self.queue)
            task2 = heapq.heappop(self.queue)
            return self.get_best_task_choice(task1, task2)

    def execute_task(self, task, current_t, plot_info, available_cores):
        if not task.is_executed and task.arrival <= current_t:
            print("Task ", task.name, "  is being executed with ", task.cores, " cores")
            plot_info[task.name].append(current_t)
            available_cores -= task.cores
            task.is_executed = True
        elif task.replace_core:
            print("Task ", task.name, "  now have more core: ", task.cores, " cores")
            available_cores -= task.change_core
            task.replace_core = False
            task.change_core = 0
        return available_cores

    def finalize_task(self, task, current_t, plot_info, available_cores):
        if task.exec_time <= 0:
            if task.arrival + task.period < current_t:
                print("Deadline missed by task ", task.name)
            else:
                print("Execution of task ", task.name, " is finished")
            plot_info[task.name].append(current_t)
            available_cores += task.cores
            task.arrival += task.period
            task.cores = None
            task.exec_time = None
            task.is_executed = False
        return available_cores

    def time_passage(self, task1, task2, current_t):
        time_pass = 0.1
        current_t += time_pass
        task1.exec_time -= time_pass
        task2.exec_time -= time_pass
        return current_t

    def schedule(self):
        current_t = 0
        plot_info = {task.name: [] for task in self.tasks}
        available_cores = 6
        while current_t < self.hyper_period:
            task1, task2 = self.find_best_tasks(available_cores)
            if current_t < task1.arrival and current_t < task2.arrival:
                current_t = min(task1.arrival, task2.arrival)

            available_cores = self.execute_task(task1, current_t, plot_info, available_cores)
            available_cores = self.execute_task(task2, current_t, plot_info, available_cores)
            current_t = self.time_passage(task1, task2, current_t)
            available_cores = self.finalize_task(task1, current_t, plot_info, available_cores)
            available_cores = self.finalize_task(task2, current_t, plot_info, available_cores)
            heapq.heappush(self.queue, task1)
            heapq.heappush(self.queue, task2)
        plot_tasks(plot_info, 'sBEET')


class SBEETTask:
    def __init__(self, task):
        self.task = task

    def __getattr__(self, attribute):
        return getattr(self.task, attribute)

    def __setattr__(self, name, value):
        if name == 'task':
            super().__setattr__(name, value)
        else:
            setattr(self.task, name, value)

    def __lt__(self, other):
        if self.task.arrival == other.task.arrival:
            return self.task.period < other.task.period
        else:
            return self.task.arrival < other.task.arrival
