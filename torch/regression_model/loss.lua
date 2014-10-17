
require 'torch'   -- torch
require 'nn'      -- provides all sorts of loss functions

-- 10-class problem
noutputs = l1_out
----------------------------------------------------------------------
print '==> define loss'

-- model:add(nn.LogSoftMax())
criterion = nn.MSECriterion()
-- criterion = nn.ClassNLLCriterion()

-- criterion = nn.MultiMarginCriterion()

----------------------------------------------------------------------
print '==> here is the loss function:'
print(criterion)
