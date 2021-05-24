import math


def create_sequence_data(sequence, shannon_range=6):
    retval = []
    for i in range(len(sequence)):
        retval.append(compute_entropy(sequence[int(max(0, i-(shannon_range/2))):int(min(len(sequence)-1, i+(shannon_range/2)))]))

    return retval


def compute_entropy(sequence):
    L = len(sequence)
    complexity_vector = []
    while sequence != '':
        c = sequence[0]
        complexity_vector.append(sequence.count(c))
        sequence = sequence.replace(c, '')

    assert(len(complexity_vector) <= 20)

    while len(complexity_vector) < 20:
        complexity_vector.append(0)

    result = 0
    for cv in complexity_vector:
        if cv > 0:
            result += (cv / L) * math.log(cv / L, 2)

    return -1 * result


if __name__ == '__main__':
    # print(compute_entropy("QWERTYUIOPASDFGHJKLZ"))
    print(compute_entropy("AAAAAAAAAABBBBBBBBBB"))



