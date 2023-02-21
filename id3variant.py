import sys
import math
import random as rd


def get_attributes(data_file):
    attr_num = len(data_file[0].strip().split())
    attributes = [[] for _ in range(attr_num)]

    for line in data_file:
        line = line.strip().split()

        for id, val in enumerate(line):
            attributes[id].append(val)

    return attributes


def get_partitions(input_file):
    partitions = {}
    for line in input_file:
        line = line.strip().split()
        partitions[line[0]] = []
        partitions[line[0]] = line[1:]
    return partitions


def entropy(probs):
    if probs:
        if 0 not in probs:
            e = list(map((lambda prob: prob * math.log(1/prob, 2)), probs))
            return sum(e)
        else:
            return 0
    else:
        print("Probability list of attribute not found!")


def get_probabilities(array, elements):
    result = [array.count(el) / len(array) for el in elements]
    return result


def target_entropy(attributes, partition=None):
    attr_list = []
    if partition:
        for attribute in attributes:
            attr_list.append([attribute[int(id)] for id in partition])
    else:
        attr_list = attributes
    target_attr_values = attr_list[-1][0:4]
    unique_attr_values = list(set(target_attr_values))

    probability_list = get_probabilities(
        target_attr_values, unique_attr_values)
    target_entropy = entropy(probability_list)

    return target_entropy


def features_entropies(attributes, partition=None):
    attr_list = []
    if partition:
        for attribute in attributes:
            attr_list.append([attribute[int(id)] for id in partition])
    else:
        attr_list = attributes
    target = attr_list[-1]
    total_features_entropies = []
    unique_target_values = list(set(target))
    for feature in attr_list[0:-1]:
        categories = list(set(feature))
        category_total_entropy = []

        for category in categories:
            unique_attr_values = [target[id]
                                  for id, val in enumerate(feature) if val == category]
            probability_list = get_probabilities(
                unique_attr_values, unique_target_values)
            category_total_entropy.append(entropy(probability_list))

        category_probabilities = get_probabilities(feature, categories)
        feature_entropy = sum(
            list(map(lambda a, b: a*b, category_probabilities, category_total_entropy)))

        total_features_entropies.append(feature_entropy)

    return total_features_entropies


def max_gain_index_and_value(attributes, partition=None):
    e_T = target_entropy(attributes, partition)
    e_As = features_entropies(attributes, partition)
    gains = list(map(lambda b: e_T-b, e_As))
    val = max(gains)
    index = int(gains.index(val))
    return [index, val]


def calc_f_val(attributes, partition):
    max_feature = max_gain_index_and_value(attributes, partition)
    n = len(attributes[-1])
    s = len(partition)
    f_val = s/n * max_feature[1]

    return [max_feature[0], f_val]


def max_f_values(attributes, partitions):
    f_comb = [[key] + calc_f_val(attributes, partition)
              for key, partition in partitions.items()]
    f_values = [x[2] for x in f_comb]
    return f_comb[f_values.index((max(f_values)))]


def split_partition(attributes, partitions):
    partition_id_to_split, attribute_id, dump = max_f_values(attributes, partitions)
    if dump is None:
        print('Invalid f_value')
    else:
        partition_list = partitions[partition_id_to_split]
        attr_to_split = attributes[attribute_id]
        categories = [
            val for id in partition_list for val in attr_to_split[int(id)]]
        res = {key: [] for key in categories}
        for partition in partition_list:
            split_index = int(attr_to_split[int(partition)])
            res[str(split_index)].append(partition)

        ids = []
        for _ in res.keys():
            id = partition_id_to_split + 1
            while id in ids or str(id) in partitions.keys():
                id += 1
            ids.append(id)

        partitions.pop(partition_id_to_split, 'Not found partition to remove')
        for val in ids:
            partitions[val] = res.popitem()[1]
        if len(ids) == 2:
            print(
                f'Partition {partition_id_to_split} was replaced with partitions {ids[0]} and {ids[1]} using Attribute {attribute_id}.')
        elif len(ids) == 3:
            print(
                f'Partition {partition_id_to_split} was replaced with partitions {ids[0]}, {ids[1]}, and {ids[2]} using Attribute {attribute_id}.')

        return partitions


def main():
    if (len(sys.argv) != 4):
        data_file = open('dataset-x.txt', 'r')
        input_file = open('partition-x.txt', 'r')
        output_file = open('partition-2.txt', 'w')
    else:
        data_file = open(sys.argv[1], 'r')
        input_file = open(sys.argv[2], 'r')
        output_file = open(sys.argv[3], 'w')

    # Process data
    attributes = get_attributes(data_file.readlines())
    partitions = get_partitions(input_file.readlines())
    output = split_partition(attributes, partitions)
    for key, value in output.items():
        output_file.writelines([f'{key} ', ' '.join(value), '\n'])


if __name__ == "__main__":
    main()
