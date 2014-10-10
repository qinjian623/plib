
require 'torch'   -- torch
require 'nn'      -- provides all sorts of loss functions

-- 10-class problem
noutputs = 2
----------------------------------------------------------------------
print '==> define loss'
criterion = nn.MultiMarginCriterion()

----------------------------------------------------------------------
print '==> here is the loss function:'
print(criterion)
