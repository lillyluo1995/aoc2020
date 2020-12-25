from typing import IO
import re
from aoc.common import helpers

def read_file(input_file):
    '''read file'''
    labels = []
    for line in input_file.readlines():
        groups = re.findall('[a-z]+', line)
        contains_idx = groups.index('contains')
        labels.append([groups[:contains_idx], groups[contains_idx+1:]])
    return labels


def parse_labels(labels):
    '''return mapping of: allergen --> idx in label in which used
    and mapping of ingredient use --> # of times ingredient used'''
    allergen_idx = {}
    all_ingredients = set()
    ingredient_use = {}
    for idx, label in enumerate(labels):
        for ingredient in label[0]:
            all_ingredients.add(ingredient)
            if ingredient in ingredient_use:
                ingredient_use[ingredient] += 1
            else:
                ingredient_use[ingredient] = 1
        for allergen in label[1]:
            if allergen in allergen_idx:
                allergen_idx[allergen].append(idx)
            else:
                allergen_idx[allergen] = [idx]
    return ingredient_use, allergen_idx, all_ingredients


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''find ingredients w no allergens and count # of times used'''
    labels = read_file(input_file)
    ingredient_use, allergen_idx, all_ingredients \
        = parse_labels(labels)

    possible_ingredients = set()
    for _, idxes in allergen_idx.items():
        relevant_ingredients = [set(labels[idx][0]) for idx in idxes]
        ingredient_inter = set.intersection(*relevant_ingredients)
        for ingredient in ingredient_inter:
            possible_ingredients.add(ingredient)
    unused = all_ingredients.difference(possible_ingredients)
    return sum([ingredient_use[ingredient] for ingredient in unused])

def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''get mapping of ingredient to allergen'''
    labels = read_file(input_file)
    _, allergen_idx, _ = parse_labels(labels)
    ingredient_map = {}
    for allergen, idxes in allergen_idx.items():
        relevant_ingredients = [set(labels[idx][0]) for idx in idxes]
        ingredient_inter = set.intersection(*relevant_ingredients)
        for ingredient in ingredient_inter:
            if ingredient in ingredient_map:
                ingredient_map[ingredient].append(allergen)
            else:
                ingredient_map[ingredient] = [allergen]
    final_mapping = helpers.organize_idx_map(ingredient_map)
    sorted_mapping = sorted(final_mapping.items(), key=lambda x: x[0])
    return ','.join([item[1] for item in sorted_mapping])
