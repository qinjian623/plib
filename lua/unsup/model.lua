require 'nn'
require 'unsup'

-- input dimensions
nfeats = 1
nout = 32
width = 20
height = 20
filtsize = 5

local conntable = nn.tables.full(nfeats, nout)
local decodertable = conntable:clone()
decodertable[{ {},1 }] = conntable[{ {},2 }]
decodertable[{ {},2 }] = conntable[{ {},1 }]

encoder = nn.Sequential()
encoder:add(nn.SpatialConvolutionMap(conntable,filtsize, filtsize, 1, 1))
encoder:add(nn.Tanh())
encoder:add(nn.Diag(nout))

decoder = unsup.SpatialConvFistaL1(decodertable, filtsize, filtsize, width, height,1)
model = unsup.PSD(encoder, decoder, 1)
