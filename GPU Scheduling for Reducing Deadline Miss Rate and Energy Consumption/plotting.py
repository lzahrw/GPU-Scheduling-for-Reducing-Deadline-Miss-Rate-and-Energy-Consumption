import matplotlib.pyplot as plt
import matplotlib.patches as patches


def plot_tasks(tasks, schedule_type):
    runtime = 40000
    color_map = {
        'Cooperative': 'skyblue',
        'sBEET': 'lightcoral'
    }
    for task in tasks:
        values = tasks[task]

        fig, ax = plt.subplots(figsize=(10, 5))
        y_value = 0.5

        if schedule_type == 'Cooperative':
            for segment in values:
                width = segment[1] - segment[0]
                rect = patches.Rectangle((segment[0], y_value - 0.5), width, 1, edgecolor='black',
                                         facecolor=color_map[schedule_type], alpha=0.7)
                ax.add_patch(rect)
        elif schedule_type == 'sBEET':
            executed_slots = []
            for i in range(0, len(values) - 1, 2):
                executed_slots.append((values[i], values[i + 1]))
            for segment in executed_slots:
                width = segment[1] - segment[0]
                rect = patches.Rectangle((segment[0], y_value - 0.5), width, 1, edgecolor='black',
                                         facecolor=color_map[schedule_type], alpha=0.7)
                ax.add_patch(rect)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_position(('outward', 10))
        ax.spines['bottom'].set_position(('outward', 10))

        ax.set_xlim(0, runtime)
        ax.set_ylim(0, 2)
        ax.set_xlabel('Time')
        ax.set_ylabel('Task Execution')
        ax.set_title(f'{schedule_type} Schedule')

        ax.grid(True, linestyle='--', alpha=0.5)

        plt.show()
        # fig.savefig(f'{schedule_type}_result_{task}.png')
