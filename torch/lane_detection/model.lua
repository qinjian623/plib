require 'nn'
l1_in = (p_size-4)*(p_size-4)/4

nstates = {9,16,32}
ifeat = 1
filtsize = 5
poolsize = 2
normkernel = image.gaussian1D(7)

model = nn.Sequential()
model:add(nn.SpatialConvolutionMap(nn.tables.random(ifeat, nstates[1], ifeat), filtsize, filtsize))
-- model:add(nn.SpatialConvolutionMM(nfeats, nstates[1], filtsize, filtsize))
model:add(nn.ReLU())
model:add(nn.SpatialLPPooling(nstates[1],5,poolsize,poolsize,poolsize,poolsize))
-- model:add(nn.SpatialMaxPooling(poolsize,poolsize))
-- model:add(nn.SpatialSubtractiveNormalization(nstates[1], normkernel))
-- stage 2 : filter bank -> squashing -> Max pooling -> normalization
-- model:add(nn.SpatialConvolutionMap(nn.tables.random(nstates[1], nstates[2], 3), filtsize, filtsize))
-- model:add(nn.Tanh())
-- model:add(nn.SpatialMaxPooling(poolsize,poolsize))
-- model:add(nn.SpatialSubtractiveNormalization(nstates[2], normkernel))

-- stage 3 : standard 2-layer neural network

model:add(nn.Reshape(nstates[1]*l1_in))--25;*148*198))--72*97))
model:add(nn.Linear(nstates[1]*l1_in, nstates[3]))
model:add(nn.Tanh())
model:add(nn.Linear(nstates[3], 2))


-- model:add(nn.Reshape(l1_in*3))
-- model:add(nn.Linear(l1_in*3, 200))
-- model:add(nn.Tanh())
-- model:add(nn.Linear(200, 32))
-- model:add(nn.Tanh())
-- model:add(nn.Linear(32, 2))
print (model)
