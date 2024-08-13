import heapq
from plotting import plot_tasks


class CooperativeScheduler:

    def __init__(self, tasks, hyper_period):
        self.hyper_period = hyper_period
        self.tasks = tasks
        self.queue = []
        # initialize the queue
        for task in self.tasks:
            heapq.heappush(self.queue, task)

    def initialize_plot_info(self):
        plot_info = {}
        for task in self.tasks:
            plot_info[task.name] = []
        return plot_info

    def execute_task(self, current_task, current_t, plot_info):
        print("Starting execution of task ", current_task.name)
        plot_info[current_task.name].append((current_t, current_t + current_task.exec_time))
        current_t += current_task.exec_time

        if current_task.arrival + current_task.period < current_t:
            print("Deadline missed by task ", current_task.name)
        else:
            print("Execution of task ", current_task.name, " is finished")

        current_task.task.arrival += current_task.period
        heapq.heappush(self.queue, current_task)
        return current_t

    def schedule(self):
        current_t = 0
        plot_info = self.initialize_plot_info()
        while current_t <= self.hyper_period:
            current_task = heapq.heappop(self.queue)
            if current_t < current_task.arrival:
                current_t = current_task.arrival
            current_t = self.execute_task(current_task, current_t, plot_info)
        plot_tasks(plot_info, 'Cooperative')


class CooperativeTask:
    def __init__(self, task):
        self.task = task

    def __getattr__(self, attribute):
        return getattr(self.task, attribute)

    def __lt__(self, other):
        if self.task.arrival == other.task.arrival:
            return self.task.index < other.task.index
        return self.task.arrival < other.task.arrival
