require 'torch'   -- torch
require 'nn'      -- provides all sorts of loss functions

criterion = nn.AbsCriterion() --MSECriterion()
-- criterion.sizeAverage = false

