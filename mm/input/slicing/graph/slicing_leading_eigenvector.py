'''
Provides the interface for the specific Newman's eigenvector algorithm
to be used for word community detection.

To use this algorithm, in the .yaml configuration write the name of this module.
(slicing: type: leading_eigenvector)

The leading_eigenvector algorithm is sensible to weighted edges. These weights
are generated by classes in the weight package. The specific
weighting scheme can be configured in "slicing: weight_calculator:"
attribute of the yaml configuration file. 

@author: Mota
'''
import mm.input.slicing.graph.slicing_graph_based as slicing_graph_based
from mm.input.slicing.graph.weight.factory import factory
from wrapper.iGraphWrapper import iGraphWrapper
import os

class SlicingLeadingEigenvector(slicing_graph_based.SlicingGraphBased):
    def __init__(self, slicer_configs):
        super(SlicingLeadingEigenvector, self).__init__(slicer_configs)
        self.igraphWrapper = iGraphWrapper(self)
        self.g = self.igraphWrapper.createGraph()
        self.weightcalc = factory(slicer_configs, self.igraphWrapper)
        self.weightcalc.calculateWeights()
        self.wc_des = slicer_configs['weight_calculator']
        
    def leading_eigenvector(self):
        vertexCluster =  self.g.community_leading_eigenvector(weights="weight")
        return self.igraphWrapper.getCommunities(vertexCluster)
    
    def run(self):
        communities = self.leading_eigenvector()
        directory = 'slicing_results/leading_eigenvector/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.print_communities(communities, directory + self.wc_des + ".txt")
        return communities
    
def construct(config):
    return SlicingLeadingEigenvector(config)  
