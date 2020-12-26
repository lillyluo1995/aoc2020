from typing import IO


class Node():
    '''a doubly linked node'''

    def __init__(self, data=None, prev_node=None, next_node=None):
        self.data = data
        self.prev = prev_node
        self.next = next_node

    def set_prev(self, new_prev):
        '''set the previous node this node links to'''
        self.prev = new_prev

    def set_next(self, new_next):
        '''set the next node this node links to'''
        self.next = new_next


class DoublyCircularLinkedList():
    '''doubly linked list circular....'''

    def __init__(self, head=None, tail=None):
        self.head = head
        self.tail = tail

    def add(self, new_data):
        '''add a new node to the end of the list'''
        new_node = Node(new_data)
        if self.head is None:
            self.head = new_node
        if self.tail is None:
            self.tail = new_node

        # wire in the new node as the tail
        new_node.set_prev(self.tail)
        new_node.set_next(self.head)

        # rewire the tail
        self.tail.set_next(new_node)

        # rewire the head
        self.head.set_prev(new_node)

        # set as the tail
        self.tail = new_node

    def search(self, target):
        '''return the node in this list that has the target'''
        found = False
        node = self.head
        counter = 0
        while not found and counter < 10000000:
            if node.data == target:
                found = True
            else:
                node = node.next
                counter += 1
        if counter == 10000000:
            print('stuck trying to find {target} on {node}'.format(
                target=target, node=node.data))
        return node

    def print(self, start=None):
        '''print as a list for debuggin'''
        if start is None:
            node = self.head
        else:
            node = self.search(start)
        list_values = []
        finished = False
        while not finished:
            list_values.append(node.data)
            node = node.next
            if node.data in list_values:
                finished = True
        return list_values

    def print_tail(self, start=None):
        '''print backwards for debuggin'''
        if start is None:
            node = self.tail
        list_values = []
        finished = False
        while not finished:
            list_values.append(node.data)
            node = node.prev
            if node.data in list_values:
                finished = True
        list_values.reverse()
        print(list_values)


def parse_input(input_line):
    '''parse in input and return doubly circular linked list'''
    input_list = [int(num) for num in input_line]
    cups = DoublyCircularLinkedList()
    mapping = {}
    for num in input_list:
        cups.add(num)
        mapping[num] = cups.tail
    return cups, mapping, max(input_list), min(input_list)


def get_pickup_labels(current_node):
    '''get the cups we'll be picking up'''
    pickup_node = current_node
    pickup_labels = []
    for num in range(3):
        pickup_node = pickup_node.next
        pickup_labels.append(pickup_node.data)
        if num == 0:
            first_pickup = pickup_node
        if num == 2:
            last_pickup = pickup_node
    return pickup_labels, first_pickup, last_pickup


def rewire_cups(cups, current_node, mapping, min_cup, max_cup):
    '''rewire the cups as described'''
    current_data = current_node.data
    pickup_labels, first_pickup, last_pickup = get_pickup_labels(current_node)
    dest_label = current_data - 1
    while dest_label in pickup_labels or dest_label < min_cup:
        dest_label -= 1
        if dest_label < min_cup:
            dest_label = max_cup
    dest_node = mapping[dest_label]
    # set the previous of the destination node...
    dest_node_prev = dest_node.prev
    while dest_node_prev.data in pickup_labels:
        dest_node_prev = dest_node_prev.prev
    dest_node.set_prev(dest_node_prev)

    first_pickup_prev = first_pickup.prev
    first_pickup.set_prev(dest_node)
    first_pickup_prev.set_next(last_pickup.next)

    dest_node_next = dest_node.next
    dest_node.set_next(first_pickup)

    dest_node_next.set_prev(last_pickup)
    last_pickup_next = last_pickup.next
    last_pickup_next.set_prev(first_pickup_prev)
    last_pickup.set_next(dest_node_next)

    return cups, current_node.next


def p_1(input_file: IO, debug=False):  # pylint: disable=unused-argument
    '''use the input to determine output after 100 rounds'''
    input_line = '467528193'
    cups, mapping, max_cup, min_cup = parse_input(input_line)
    current_node = cups.head
    for _ in range(100):
        cups, current_node = rewire_cups(
            cups, current_node, mapping, min_cup, max_cup)
    return ''.join([str(num) for num in cups.print(1)[1:]])


def p_2(input_file: IO, debug=False):  # pylint: disable=unused-argument
    '''more cups...more rounds'''
    input_line = '467528193'
    cups, mapping, max_cup, min_cup = parse_input(input_line)

    total_cups = 1000000
    for num in range(max_cup+1, total_cups+1):
        cups.add(num)
        mapping[num] = cups.tail
    max_cup = total_cups

    current_node = cups.head
    for num_round in range(total_cups*10):
        if num_round % total_cups == 0:
            print(num_round)
        cups, current_node = rewire_cups(
            cups, current_node, mapping, min_cup, max_cup)

    node_1 = cups.search(1)
    next_1 = node_1.next
    next_2 = next_1.next
    return next_1.data*next_2.data
