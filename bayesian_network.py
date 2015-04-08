import random as r
import functional as f

class Network: 
	"""Class to represent a network of bayesian nodes"""
	def __init__(self, parent_nodes_list, name_to_node_map):
		self.parent_nodes_list = parent_nodes_list
		self.name_to_node_map = name_to_node_map


class Bayesian_node:
    """Directed, binary bayesian network"""
    def __init__(self, children, p_up, parents, name=None):
    	#list of this node's children Bayesian_nodes
        self.children = children
        #function that takes the list of the node's parents (self.parents) and returns the probability 
        #this node is a 'one' or 'up'
        self.p_up = p_up
        #list of this node's parent bayesian_nodes
        self.parents = parents
        #name for printing purposes
        self.name = name
       	#useful for generating samples
       	self.state = 0b0
       	#useful for generating samples
       	self.marked = False


def generate_network():#num_parents, num_leaves, approx_num_total_nodes, approx_connectivity):
	"""Generates the network on page 362 on bishop... Too much work to generate random networks for now"""
	#lambda to collapse the list of parent's states into a binary string
	get_parents_binary_string = lambda parents: f.foldl(lambda acc, element: acc<<1 | element.state, 0b0, parents)
	#simply looks up the binary string formed from the parents in the p_map
	p_up = lambda p_map, parents: p_map[get_parents_binary_string(parents)]
	node1 = Bayesian_node(None, lambda: .4, None, 0)
	node2 = Bayesian_node(None, lambda: .7, None, 1)
	node3 = Bayesian_node(None, lambda: .3, None, 2)

	node4_p_dict = {0b000:.2, 0b001:.5, 0b010:.7, 0b100:.43, 0b011:.15, 0b101:.35, 0b110: .6, 0b111:.25}
	node4 = Bayesian_node(None, f.partial(p_up, node4_p_dict), [node1, node2, node3], 3)
	node5_p_dict = {0b00:.9, 0b01:.5, 0b10:.2, 0b11:.1}
	node5 = Bayesian_node(None, f.partial(p_up, node5_p_dict), [node1, node3],4)
	node6_p_dict = {0b1:.85, 0b0:.374}
	node6 = Bayesian_node(None, f.partial(p_up, node6_p_dict), [node4], 5)
	node7_p_dict = {0b00:.19, 0b01:.27, 0b10:.5, 0b11:.333}
	node7 = Bayesian_node(None, f.partial(p_up, node7_p_dict), [node4, node5], 6)

	node1.children = [node4, node5]
	node2.children = [node4]
	node3.children = [node4, node5]
	node4.children = [node6, node7]
	node5.children = [node7]

	return Network([node1,node2,node3], {0: node1, 1: node2, 2: node3, 3:node4, 4:node5, 5:node6, 6:node7})


def assign_value(node):
	"""assigns a value to a node via the ancestral sampling method"""
	if node.marked == True: #check if already assigned a value to this node
		return
	if node.parents is None: #this is a root node
		node.state = 0b0 if (r.random() > node.p_up()) else 0b1
	else:
		for parent in node.parents:
			if not parent.marked: #if the parent has no value, we need to fill it in
				assign_value(parent)
		node.state = 0b0 if (r.random() > node.p_up(node.parents)) else 0b1
	node.marked = True


def sample(parent_nodes_list):
	"""generates one sample from the network"""
	for node in parent_nodes_list:
		assign_value(node)
		if node.children is not None:
			sample(node.children)


def clear_marks(name_to_node_map):
	"""sets all marks in the network to false"""
	for key, value in name_to_node_map.iteritems():
		name_to_node_map[key].marked = False


def is_valid_sample(name_to_node_map, name_to_clamped_map):
	"""checks if the sample meets the criteria in the name_to_clamped_map.. this allows 
	a very inefficient form of rejection sampling"""
	for key, value in name_to_clamped_map:
		if name_to_node_map[key] is not value:
			return False
	return True


def put_sample_in_table(name_to_node_map, sample_table):
	"""samples are recorded as a binary string where the first place 
	represents node 1's value and place n represents node n's value"""
	get_bin = lambda x, n: x >= 0 and str(bin(x))[2:].zfill(n) or "-" + str(bin(x))[3:].zfill(n)
	sample_value = 0b0
	for key, node in name_to_node_map.iteritems():
		binary_string_temp = node.state << (len(name_to_node_map)-1) - node.name
		sample_value = sample_value | binary_string_temp
	if sample_table.has_key(sample_value):
		sample_table[sample_value]+=1
	else:
		sample_table[sample_value]=1
	print get_bin(sample_value, len(name_to_node_map))
	return sample_table

	

def build_ancestral_sample_table(network, num_samples, name_to_clamped_map):
	sample_table = {}
	network = generate_network()
	parent_nodes_list = network.parent_nodes_list
	name_to_node_map = network.name_to_node_map
	for i in range(num_samples):
		sample(parent_nodes_list)
		if (is_valid_sample(parent_nodes_list, name_to_clamped_map)):
			put_sample_in_table(network.name_to_node_map, sample_table)
		clear_marks(name_to_node_map)
	return sample_table


def pretty_print(parent_nodes_list):
	for node in parent_nodes_list:
		print node.name + ' '
		print 'is assigned ' + str(node.marked) + ' '
		print 'value is ' + str(node.state) + ' \n'
		if node.children is not None:
			pretty_print(node.children)
