import json
import numpy as np
import collections
import argparse
import matplotlib.pyplot as plt
import analysis.utils

args = argparse.ArgumentParser()
args.add_argument("--uid-linear", default="ailr_linear_simple_t3_10n15_s0")
args.add_argument("--uid-random", default="ailr_random_t3_10n15_s0")
args = args.parse_args()

data_all = analysis.utils.data_to_users("computed/collected.jsonl", flat=True)
data_linear = [line for line in data_all if line["uid"] == args.uid_linear]
data_random = [line for line in data_all if line["uid"] == args.uid_random]

plt.figure(figsize=(4, 2))

def plot_trajectory(data, name, color):
    data_local = collections.defaultdict(list)
    accuracy_acc = []
    for line in data:
        data_local[line["data_i"]].append(line["reward"])
        # add only test for accuracy computation
        if line["data_i"] >= 10:
            accuracy_acc.append(line["question"]["correct"] == line["response"])
    data_local = [(k, np.average(v)) for k,v in data_local.items()]
    data_local.sort(key=lambda x: x[0])
    plt.plot(
        [i for i, reward in data_local],
        [reward for i, reward in data_local],
        label=name,
        color=color,
        linewidth=4,
        zorder=10,
    )

    plt.text(
        len(data_local)-0.5, data_local[-1][1],
        ha="left", va="center",
        s=f"{np.average(accuracy_acc):.0%}",
        color=color
    )
    print(name, f"{np.average(accuracy_acc):.1%}")

    # plot individual users
    data_local = collections.defaultdict(list)
    for line in data:
        data_local[line["user"]["prolific_pid"]].append(line)
    data_local = list(data_local.values())
    for data_local_user in data_local:
        # solution to multiple runs?
        data_local_user_multi = collections.defaultdict(list)
        for line in data_local_user:
            data_local_user_multi[line["data_i"]].append(line)

        data_local_user_multi = [(k,np.average([x["reward"] for x in v])) for k,v in data_local_user_multi.items()]
        data_local_user_multi.sort(key=lambda x: x[0])
        plt.plot(
            [x[0] for x in data_local_user_multi],
            [x[1] for x in data_local_user_multi],
            color=color, alpha=0.3,
            linewidth=1,
            zorder=5,
        )

plot_trajectory(data_linear, "Linear", color="#190")
plot_trajectory(data_random, "Balanced random", color="#910")
plt.vlines(
    x=10, ymin=0, ymax=plt.ylim()[1]/2,
    color="black"
)

ax = plt.gca()
ax.spines[["top", "right"]].set_visible(False)

plt.legend(frameon=False)
plt.ylabel("Reward (p)")
plt.xlabel("Interaction")
plt.tight_layout(pad=0.1)
plt.show()