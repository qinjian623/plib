require 'torch'   -- torch
require 'image'   -- for image transforms
require 'gfx.js'  -- to visualize the dataset
require 'nn'      -- provides all sorts of trainable modules/layers

print '==> define parameters'

-- 10-class problem
noutputs = 2

-- input dimensions

width = scale_width - 4
height = scale_height - 4

ninputs = nfeats*width*height

-- hidden units, filter sizes (for ConvNet only):
nstates = {64,64,128}
filtsize = 5
poolsize = 2
normkernel = image.gaussian1D(7)

----------------------------------------------------------------------
print '==> construct model'


-- a typical convolutional network, with locally-normalized hidden
-- units, and L2-pooling

-- Note: the architecture of this convnet is loosely based on Pierre Sermanet's
-- work on this dataset (http://arxiv.org/abs/1204.3968). In particular
-- the use of LP-pooling (with P=2) has a very positive impact on
-- generalization. Normalization is not done exactly as proposed in
-- the paper, and low-level (first layer) features are not fed to
-- the classifier.

model = nn.Sequential()

-- stage 1 : filter bank -> squashing -> Max pooling -> normalization
model:add(nn.SpatialConvolutionMap(nn.tables.random(nfeats, nstates[1], nfeats), filtsize, filtsize))
-- model:add(nn.SpatialConvolutionMM(nfeats, nstates[1], filtsize, filtsize))
model:add(nn.Tanh())
model:add(nn.SpatialMaxPooling(poolsize,poolsize))
model:add(nn.SpatialSubtractiveNormalization(nstates[1], normkernel))
-- stage 2 : filter bank -> squashing -> Max pooling -> normalization
model:add(nn.SpatialConvolutionMap(nn.tables.random(nstates[1], nstates[2], 3), filtsize, filtsize))
model:add(nn.Tanh())
model:add(nn.SpatialMaxPooling(poolsize,poolsize))
model:add(nn.SpatialSubtractiveNormalization(nstates[2], normkernel))

-- stage 3 : standard 2-layer neural network
model:add(nn.Reshape(nstates[2]*9))--*148*198))--72*97))
model:add(nn.Linear(nstates[2]*9, nstates[3]))
model:add(nn.Tanh())
model:add(nn.Linear(nstates[3], noutputs))

----------------------------------------------------------------------
print '==> here is the model:'
print(model)

----------------------------------------------------------------------
-- Visualization is quite easy, using gfx.image().

if false then--opt.visualize then
   if true then --opt.model == 'convnet' then
      print '==> visualizing ConvNet filters'
      model:get(1)
      gfx.image(model:get(1).weight, {zoom=2, legend='L1'})
      gfx.image(model:get(5).weight, {zoom=2, legend='L2'})
   end
end
