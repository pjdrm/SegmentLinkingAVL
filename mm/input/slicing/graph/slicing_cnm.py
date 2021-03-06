'''
Provides the interface for the specific Clauset-Newman-Moore (CNM) algorithm
to be used for word community detection.

To use this algorithm, in the .yaml configuration write the name of this module.
(slicing: type: slicing_cnm)

@author: Mota
'''
import os
import snap
import mm.input.slicing.graph.slicing_graph_based as slicing_graph_based

class SlicingCNM(slicing_graph_based.SlicingGraphBased):
    def __init__(self, slicer_configs):
        super(SlicingCNM, self).__init__(slicer_configs)
        self.g = self.createGraph()
        self.debugDir = 'resources/slicing_results/cnm/'
        self.debugFile = self.debugDir + "cnm.txt"
        self.desc = "cnm " + self.desc
        
    def cnm(self):
        CmtyV = snap.TCnComV()
        snap.CommunityCNM(self.g, CmtyV)
        community_list = []
        for C in CmtyV:
            cluster_k = []
            for Node in C:
                token = self.token_to_word[Node]
                cluster_k += [token]
            cluster_d = {'cluster_tokens': cluster_k, 'k': self.k}
            community_list += [cluster_d]
        return community_list
    
    def run(self):
        communities = self.cnm()
        if not os.path.exists(self.debugDir):
            os.makedirs(self.debugDir)
        self.print_communities(communities, self.debugFile)
        return communities
        
def construct(config):
    return SlicingCNM(config)
