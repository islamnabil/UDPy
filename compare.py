import matplotlib.pyplot as plt
from pprint import pprint


DELIMITER = '\'\'^||^\'\''  # 8

plp = [1, 2, 3, 4, 5, 10, 30]
throughput = []


def get(filename):
    cur = [0, 0, 0, 0, 0, 0, 0]

    with open(filename) as log:
        runs = [run.strip() for run in log.read().split(DELIMITER)]
        runs = [run.split('\n') for run in runs]
    pprint(runs)

    for i in range(0, len(runs), 5):
        samples = runs[i: i + 5]
        pprint(samples)
        for sample in samples:
            cur[i // 5] += float(sample[0].split('=')[1])
        cur[i // 5] /= 5
    throughput.append(cur)


get('go-back-n/GBNlog.txt')
get('stop-and-wait/log.txt')

plt.plot(plp, throughput[0], label='go-back-n')
plt.plot(plp, throughput[1], label='stop-and-wait')
plt.legend(['go-back-n', 'stop-and-wait'], ['s', 'g'])
plt.xlabel('Packet Loss Probability %')
plt.ylabel('Throughput (bps)')
plt.legend(loc='upper right')
plt.show()
