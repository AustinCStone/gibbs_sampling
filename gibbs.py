import bayesian_network as b
import random as r


class Sample_table_container:
	def __init__(self, gibbs_sample_table, ancestral_sample_table):
		self.gibbs_sample_table = gibbs_sample_table
		self.ancestral_sample_table = ancestral_sample_table


def gibbs(name_to_node_map, name_to_clamped_map, num_burnin_samples, num_gibbs_samples):
	"""Performs gibbs sampling"""
	sample_table = {}
	#initialize with random and clamped values
	for name, node in name_to_node_map.iteritems():
		node.state = 0b1 if r.random() > .5 else 0b0
	for name, clamped_value in name_to_clamped_map.iteritems():
		name_to_node_map[name].state = clamped_value

	#start the iteration process
	for sample_num in range(num_gibbs_samples+num_burnin_samples):
		#iterate through all the variables
		for name, node in name_to_node_map.iteritems():
			if not name_to_clamped_map.has_key(name): #don't touch clamped values
				#sample this new variable in terms of all other variables
				#this node's sample depends only on its parents 
				p_up = node.p_up(node.parents) if node.parents is not None else node.p_up()
				node.state = 0b0 if r.random() > p_up else 0b1
		if sample_num > num_burnin_samples:
			b.put_sample_in_table(name_to_node_map, sample_table)

	return sample_table


def driver(num_burnin_samples, num_gibbs_samples, num_ancestral_samples, name_to_clamped_map):
	network = b.generate_network()
	ancestral_sample_table = b.build_ancestral_sample_table(network, num_ancestral_samples, name_to_clamped_map)
	gibbs_sample_table = gibbs(network.name_to_node_map, name_to_clamped_map, num_burnin_samples, num_gibbs_samples)
	return Sample_table_container(gibbs_sample_table, ancestral_sample_table)


