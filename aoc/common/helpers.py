def find_limiting_label(mapping):
    '''find the label in the mapping with the fewest options'''
    min_seats = 200
    label_choice = ''
    for label, poss_idx in mapping.items():
        if len(poss_idx) < min_seats:
            min_seats = len(poss_idx)
            label_choice = label
    return label_choice


def organize_idx_map(mapping):
    '''given a mapping that has label --> to all options,
    return a mapping that has label --> 1 option'''
    # now we have all the possible ones...so we have to sift thru
    organized = False
    final_mapping = {}
    num_labels = len(mapping.keys())
    while not organized:
        # find the label with the least options...
        limiting_label = find_limiting_label(mapping)
        assert len(mapping[limiting_label]) == 1
        final_seat = mapping[limiting_label][0]
        final_mapping[final_seat] = limiting_label
        del mapping[limiting_label]
        for _, poss_idx in mapping.items():
            if final_seat in poss_idx:
                poss_idx.remove(final_seat)
        if len(final_mapping.keys()) == num_labels:
            organized = True
    return final_mapping