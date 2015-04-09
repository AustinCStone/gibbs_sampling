To run, use the python console. 
1.) At terminal, go to the directory for the files. 
2.) Type "python"
3.) Type "import gibbs"
4.) Type "tables = gibbs.driver(<num_burnin_samples>, <num_gibbs_samples>, <num_ancestral_samples>, <clamp_value_map>)" For instance, a call of 
tables = gibbs.driver(100, 1000, 1000, {0:0,4:1}) will generate 1000 ancestral samples, 1000 gibbs samples (with 100 iterations of burnin) and pull these samples from the conditional distribution where x1 is 0 and x5 is 1 (in the map 0:0 corresponds to set x1 to 0). An empty map, {} can also be entered in to sample from the full joint. The function returns these samples in a table object. 
5.) If you called your table object "tables," run tables.compare_pdfs() to generate a series of graphs comparing the sample frequencies for each method. 