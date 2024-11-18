import numpy as np
import GA

class Brain():
    def __init__(self,genome):
        self.genome = genome
        self.inputs = np.zeros((7))
        self.outputs = np.array([1,0], dtype=int)
        self.hidden_layer_weights = np.zeros((7, 7))
        self.output_layer_weights = np.zeros((7, 2))
        self.hidden_layer_bias = self.genome.hidden_layer_bias
        self.output_layer_bias = self.genome.output_layer_bias
        self._init_weights()
        #print(self.hidden_layer_weights)
        #print()
        #print(self.output_layer_weights)
    
    def _init_weights(self):
        for gen in self.genome.genes:
            if gen.source_hidden_layer:
                self.output_layer_weights[gen.source, gen.target] = gen.weight
            else:
                self.hidden_layer_weights[gen.source, gen.target] = gen.weight

    def update_weights(self):

        self.hidden_layer_weights.fill(0)
        self.output_layer_weights.fill(0)
        

        self.hidden_layer_bias = self.genome.hidden_layer_bias
        self.output_layer_bias = self.genome.output_layer_bias
        
        self._init_weights()

    
    def feed_forward(self,inputs):
        self.inputs[:] = inputs
        hidden_outputs = np.dot(self.hidden_layer_weights, self.inputs) + self.hidden_layer_bias
        hidden_outputs = self.ReLU(hidden_outputs)

        self.outputs = np.dot(self.output_layer_weights.T, hidden_outputs) + self.output_layer_bias
        self.outputs = self.ReLU(self.outputs)

    def ReLU(self, x):
        return np.maximum(0, x)

