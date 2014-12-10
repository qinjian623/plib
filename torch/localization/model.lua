require 'torch'   -- torch
require 'image'   -- for image transforms
require 'gfx.js'  -- to visualize the dataset
require 'nn'      -- provides all sorts of trainable modules/layers

print '==> define parameters'


-- input dimensions


-- hidden units, filter sizes (for ConvNet only):
nstates = {16,128,256}

poolsize = 2
normkernel = image.gaussian1D(5)

----------------------------------------------------------------------
print '==> construct model'

model = nn.Sequential()

-- stage 1 : filter bank -> squashing -> Max Pooling
-- model:add(nn.SpatialConvolutionMap(nn.tables.full(nfeats, nstates[1]), 21, 21))
-- model:add(nn.ReLU())
-- model:add(nn.SpatialMaxPooling(poolsize,poolsize))

model:add(nn.SpatialConvolutionMap(nn.tables.full(nfeats, nstates[1]), 11, 11))
model:add(nn.ReLU())
model:add(nn.SpatialMaxPooling(poolsize,poolsize))

-- stage 2 : filter bank -> squashing -> Max pooling
model:add(nn.SpatialConvolutionMap(nn.tables.full(nstates[1], nstates[2]), 5, 5))
model:add(nn.ReLU())
model:add(nn.SpatialMaxPooling(poolsize,poolsize))

model:add(nn.SpatialConvolutionMap(nn.tables.full(nstates[2], nstates[2]), 5, 5))
model:add(nn.ReLU())
-- model:add(nn.SpatialMaxPooling(poolsize,poolsize))

model:add(nn.SpatialConvolutionMap(nn.tables.full(nstates[2], nstates[3]), 5, 5))
model:add(nn.ReLU())

model:add(nn.SpatialConvolutionMap(nn.tables.full(nstates[3], 100), 3, 3))
model:add(nn.ReLU())

model:add(nn.SpatialConvolutionMap(nn.tables.full(100, 64), 3, 3))
model:add(nn.ReLU())

model:add(nn.SpatialConvolutionMap(nn.tables.full(64, 32), 3, 3))
model:add(nn.ReLU())

model:add(nn.SpatialConvolutionMap(nn.tables.full(32, 1), 1, 1))
model:add(nn.ReLU())

model:add(nn.Reshape(25*65))
model:add(nn.Linear(25*65, 25*65))
model:add(nn.ReLU())

-- model:add(nn.Linear(25*65, 25*25))
-- model:add(nn.ReLU())
model:add(nn.Reshape(25, 25))



-- model:add(nn.Tanh())
-- model:add(nn.SpatialSubtractiveNormalization(nstates[3], normkernel))


--model:add(nn.SpatialConvolutionMap(nn.tables.random(nstates[3], 3, 3), 1, 1))
-- model:add(nn.Tanh())
-- model:add(nn.SpatialMaxPooling(poolsize,poolsize))
-- model:add(nn.SpatialSubtractiveNormalization(3, normkernel))

-- model:add(nn.Reshape(10*28*56))--*148*198))--72*97))
-- model:add(nn.Linear(10*28*56, 124*68))
-- model:add(nn.Tanh())
-- model:add(nn.Reshape(68, 124))
----------------------------------------------------------------------
print '==> here is the model:'
print(model)

----------------------------------------------------------------------
-- Visualization is quite easy, using gfx.image().

if false then --opt.visualize then
   if true then --opt.model == 'convnet' then
      print '==> visualizing ConvNet filters'
      model:get(1)
      gfx.image(model:get(1).weight, {zoom=2, legend='L1'})
      gfx.image(model:get(5).weight, {zoom=2, legend='L2'})
   end
end
