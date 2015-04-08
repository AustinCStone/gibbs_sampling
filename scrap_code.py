'''
def extract_sample_value(parent_nodes_list):
	return extract_sample_value_helper(0b0, parent_nodes_list)


def extract_sample_value_helper(sample_value, parent_nodes_list):
	"""samples are recorded in terms of the binary string representing the depth first traversal of the tree"""
	for node in parent_nodes_list:
		if not node.marked:
			sample_value = sample_value<<1 | node.state
			node.marked = True
			print node.name
		if node.children is not None:
			sample_value = extract_sample_value_helper(sample_value, node.children) 
	return sample_value
'''
'''
def filter_sample_table(binary_string, sample_table):
	filtered_table = {}
	for key, value in sample_table:
		if key & binary_string:
			if filtered_table.has_key(binary_string):
				filtered_table[binary_string]+=1
			else:
				filtered_table[binary_string] = 1
	return filtered_table
'''

	'''node1 = Bayesian_node(None, lambda: .5, None, "1")
	node2 = Bayesian_node(None, lambda: .5, None, "2")
	node3 = Bayesian_node(None, lambda: .5, None, "3")
	node4_p_dict = {0b000:.5, 0b001:.5, 0b010:.5, 0b100:.5, 0b011:.5, 0b101:.5, 0b110: .5, 0b111:.5}
	node4 = Bayesian_node(None, f.partial(p_up, node4_p_dict), [node1, node2, node3], "4")
	node5_p_dict = {0b00:.5, 0b01:.5, 0b10:.5, 0b11:.5}
	node5 = Bayesian_node(None, f.partial(p_up, node4_p_dict), [node1, node3],"5")
	node6_p_dict = {0b1:.5, 0b0:.5}
	node6 = Bayesian_node(None, f.partial(p_up, node6_p_dict), [node4], "6")
	node7_p_dict = {0b00:.5, 0b01:.5, 0b10:.5, 0b11:.5}
	node7 = Bayesian_node(None, f.partial(p_up, node7_p_dict), [node4, node5], "7")'''