require 'nn'
require 'unsup'


local conntable = nn.tables.full(nfeats, nout)
local decodertable = conntable:clone()
decodertable[{ {},1 }] = conntable[{ {},2 }]
decodertable[{ {},2 }] = conntable[{ {},1 }]

encoder = nn.Sequential()
encoder:add(nn.SpatialConvolutionMap(conntable,kernsize, kernsize, 1, 1))
encoder:add(nn.Tanh())
encoder:add(nn.Diag(nout))

decoder = unsup.SpatialConvFistaL1(decodertable, kernsize, kernsize, patch_size, patch_size, 1)
model = unsup.PSD(encoder, decoder, 1)
