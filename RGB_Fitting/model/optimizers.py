# This code was taken directly from the original github implementation of FFHQ-UV (Bai et al. (2023)), which can be found here: https://github.com/csbhr/FFHQ-UV

import torch
from torch.optim import Optimizer


class SphericalOptimizer(Optimizer):
    '''
    Spherical Optimizer Class
    Uses the first two dimensions as batch information
    Optimizes over the surface of a sphere using the initial radius throughout
    
    Example Usage:
        opt = SphericalOptimizer([x], torch.optim.Adam, lr=0.01)
    '''

    def __init__(self, params, optimizer=torch.optim.Adam, **kwargs):
        self.opt = optimizer(params, **kwargs)
        self.params = params
        with torch.no_grad():
            self.radii = {
                param: (param.pow(2).sum(tuple(range(2, param.ndim)), keepdim=True) + 1e-9).sqrt()
                for param in params
            }

    @torch.no_grad()
    def step(self, closure=None):
        loss = self.opt.step(closure)
        for param in self.params:
            param.data.div_((param.pow(2).sum(tuple(range(2, param.ndim)), keepdim=True) + 1e-9).sqrt())
            param.mul_(self.radii[param])
        return loss