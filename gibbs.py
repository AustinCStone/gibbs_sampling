import bayesian_network as b
import random as r
import functional as f


class Sample_table_container:
	def __init__(self, gibbs_sample_table, ancestral_sample_table):
		self.gibbs_sample_table = gibbs_sample_table
		self.ancestral_sample_table = ancestral_sample_table

	def compare_pdfs(self):
		#why doesn't iterkeys give an array? it would be nice to be able to do iterkeys().sum()
		total_gibbs_samples = float(sum(map(lambda value: value, self.gibbs_sample_table.itervalues())))
		total_ancestral_samples = float(sum(map(lambda value: value, self.ancestral_sample_table.itervalues())))
		frequency_table_gibbs = []
		frequency_table_ancestral = []
		for key, value in self.ancestral_sample_table.iteritems():
			frequency_table_ancestral.append([key, float(value)/total_ancestral_samples])

		for key, value in self.gibbs_sample_table.iteritems():
			frequency_table_gibbs.append([key, float(value)/total_gibbs_samples])

		sorted(frequency_table_gibbs, key=lambda entry: entry[0])
		sorted(frequency_table_ancestral, key=lambda entry: entry[0])
		print frequency_table_ancestral
		print '\n\n\n\n\n\n'
		print frequency_table_gibbs

		

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


