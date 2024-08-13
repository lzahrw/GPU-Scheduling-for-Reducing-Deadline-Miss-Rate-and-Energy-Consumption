import math
from functools import reduce
from task import TaskGen
from Cooperative_scheduler import CooperativeScheduler, CooperativeTask
from sBEET_scheduler import SBEETScheduler, SBEETTask

runtime = 40000


def calculate_hyper_period(tasks_set):
    periods = [int(task.period) for task in tasks_set]
    return reduce(math.lcm, periods)


if __name__ == '__main__':
    # tasks = TaskGenerator(gen_type=TaskGenerator.MAX).generate_tasks()
    #
    # print("Start execution with Cooperative Algorithm")
    # cooperative_tasks = [CooperativeTask(task) for task in tasks]
    # hyper_period = calculate_hyper_period(cooperative_tasks)
    # cooperative = CooperativeScheduler(cooperative_tasks, runtime)
    # cooperative.schedule()
    #
    # print("Start execution with sBEET Algorithm")
    # sbeet_tasks = [SBEETTask(task) for task in tasks]
    # sbeet = SBEETScheduler(sbeet_tasks, runtime)
    # sbeet.schedule()
    task_generator = TaskGen()
    tasks = task_generator.generate_tasks(nsets=1)
    print(len(tasks))
    for task in tasks:
        print(f"Task Name: {task.name}, Utilization: {task.utilization}, Period: {task.exec_time}")

    # print("Start execution with Cooperative Algorithm")
    # cooperative_tasks = [CooperativeTask(task) for task in tasks]
    # hyper_period = calculate_hyper_period(cooperative_tasks)
    # cooperative = CooperativeScheduler(cooperative_tasks, runtime)
    # cooperative.schedule()
    #
    print("Start execution with sBEET Algorithm")
    sbeet_tasks = [SBEETTask(task) for task in tasks]
    sbeet = SBEETScheduler(sbeet_tasks, runtime)
    sbeet.schedule()
