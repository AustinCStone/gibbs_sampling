import bayesian_network as b
import random as r
import functional as f
import numpy as np
import matplotlib.pyplot as plt


class Sample_table_container:
	def __init__(self, gibbs_sample_table, ancestral_sample_table):
		self.gibbs_sample_table = gibbs_sample_table
		self.ancestral_sample_table = ancestral_sample_table

	def compare_pdfs(self):
		#why doesn't iterkeys give an array? it would be nice to be able to do iterkeys().sum()
		total_gibbs_samples = float(sum(map(lambda value: value, self.gibbs_sample_table.itervalues())))
		print 'total gibbs samples: ' + str(total_gibbs_samples) + '\n'
		total_ancestral_samples = float(sum(map(lambda value: value, self.ancestral_sample_table.itervalues())))
		print 'total ancestral samples: ' + str(total_ancestral_samples) + '\n'
		frequency_table_gibbs = []
		frequency_table_ancestral = []
		for key, value in self.ancestral_sample_table.iteritems():
			frequency_table_ancestral.append([key, float(value)/total_ancestral_samples])

		for key, value in self.gibbs_sample_table.iteritems():
			frequency_table_gibbs.append([key, float(value)/total_gibbs_samples])

		#stupid way of graphing results
		sorted(frequency_table_gibbs, key=lambda entry: entry[0])
		sorted(frequency_table_ancestral, key=lambda entry: entry[0])
		i = 0
		while(i<len(frequency_table_ancestral)):
			end = min(len(frequency_table_ancestral), i+18)
			graph(frequency_table_ancestral[i:end], frequency_table_gibbs[i:end])
			i+=18

def graph(frequency_table_ancestral, frequency_table_gibbs):
	print frequency_table_gibbs
	print frequency_table_ancestral
	N = max(len(frequency_table_gibbs), len(frequency_table_ancestral))
	gibbs = map(lambda entry: entry[1], frequency_table_gibbs)
	ancestral = map(lambda entry: entry[1], frequency_table_ancestral)

	ind = np.arange(N)  # the x locations for the groups
	print ind
	width = 0.2      # the width of the bars

	fig, ax = plt.subplots()
	rects1 = ax.bar(ind, gibbs, width, color='r')
	rects2 = ax.bar(ind+width, ancestral, width, color='y')

	# add some text for labels, title and axes ticks
	ax.set_ylabel('Frequency')
	ax.set_title('Sample Occurences')
	ax.set_xticks(ind+width)

	get_bin = lambda x, n: x >= 0 and str(bin(x))[2:].zfill(n) or "-" + str(bin(x))[3:].zfill(n)
	x_labels = map(lambda entry: get_bin(entry[0], 7), frequency_table_ancestral)
	ax.set_xticklabels( x_labels, rotation="vertical")

	ax.legend( (rects1[0], rects2[0]), ('Gibbs', 'Ancestral') )

	'''def autolabel(rects):
	    # attach some text labels
		for rect in rects:
   			height = rect.get_height()
    		ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
            	ha='center', va='bottom')

	autolabel(rects1)
	autolabel(rects2)'''

	plt.show()


def calculate_conditional_p(node_to_sample, name_to_node_map):
	#This method might be a little confusing. All it is doing is calculating the probability 
	#that the node_to_sample should be sampled with value 1 given the state of all the other nodes in the network. 
	#The formula comes from page 382 of bishop, which is the obvious way to calculate the conditional distribution
	
	node_to_sample.state = 0b1 
	p_node_is_1 = 1.0 #probability of the network if the node_to_sample is set to 1
	original_state = node_to_sample.state
	for node in name_to_node_map.itervalues():
		if node.state is 0b1:
			p_node_is_1 *= node.p_up(node.parents) if node.parents is not None else node.p_up()
		else: #p_up is the probability the node is 1 given its parents, so we need to take 1.0 minus this value when the node is set to 0
			p_node_is_1 *= 1.0-node.p_up(node.parents) if node.parents is not None else 1.0-node.p_up()

	node_to_sample.state = 0b0
	p_node_is_0 = 1.0 #probability of the network if the node_to_sample is set to 0
	for name, node in name_to_node_map.iteritems(): #calculate p_node_is_1 with flipped state
		if node.state is 0b1:
			p_node_is_0 *= node.p_up(node.parents) if node.parents is not None else node.p_up()
		else: 
			p_node_is_0 *= 1.0-node.p_up(node.parents) if node.parents is not None else 1.0-node.p_up()

	return p_node_is_1/(p_node_is_1+p_node_is_0)

		
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
				p_up = calculate_conditional_p(node, name_to_node_map)
				node.state = 0b0 if r.random() > p_up else 0b1
		if sample_num > num_burnin_samples:
			b.put_sample_in_table(name_to_node_map, sample_table)

	return sample_table



def driver(num_burnin_samples, num_gibbs_samples, num_ancestral_samples, name_to_clamped_map):
	network = b.generate_network()
	ancestral_sample_table = b.build_ancestral_sample_table(network, num_ancestral_samples, name_to_clamped_map)
	gibbs_sample_table = gibbs(network.name_to_node_map, name_to_clamped_map, num_burnin_samples, num_gibbs_samples)
	return Sample_table_container(gibbs_sample_table, ancestral_sample_table)


