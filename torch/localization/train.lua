----------------------------------------------------------------------
-- This script demonstrates how to define a training procedure,
-- irrespective of the model/loss functions chosen.
--
-- It shows how to:
--   + construct mini-batches on the fly
--   + define a closure to estimate (a noisy) loss
--     function, as well as its derivatives wrt the parameters of the
--     model to be trained
--   + optimize the function, according to several optmization
--     methods: SGD, L-BFGS.
--
-- Clement Farabet
----------------------------------------------------------------------

require 'torch'   -- torch
require 'xlua'    -- xlua provides useful tools, like progress bars
require 'optim'   -- an optimization package, for online and batch methods

----------------------------------------------------------------------
-- parse command line arguments
if not opt then
   print '==> processing options'
   cmd = torch.CmdLine()
   cmd:text()
   cmd:text('SVHN Training/Optimization')
   cmd:text()
   cmd:text('Options:')
   cmd:option('-save', 'results', 'subdirectory to save/log experiments in')
   cmd:option('-visualize', false, 'visualize input data and weights during training')
   cmd:option('-plot', false, 'live plot')
   cmd:option('-optimization', 'SGD', 'optimization method: SGD | ASGD | CG | LBFGS')
   cmd:option('-learningRate', 1e-3, 'learning rate at t=0')
   cmd:option('-batchSize', 1, 'mini-batch size (1 = pure stochastic)')
   cmd:option('-weightDecay', 0, 'weight decay (SGD only)')
   cmd:option('-momentum', 0, 'momentum (SGD only)')
   cmd:option('-t0', 1, 'start averaging at t0 (ASGD only), in nb of epochs')
   cmd:option('-maxIter', 2, 'maximum nb of iterations for CG and LBFGS')
   cmd:text()
   opt = cmd:parse(arg or {})
end

----------------------------------------------------------------------
-- CUDA?
if opt.type == 'cuda' then
   model:cuda()
   criterion:cuda()
end

----------------------------------------------------------------------
print '==> defining some tools'


-- Log results to files
trainLogger = optim.Logger(paths.concat(opt.save, 'train.log'))
testLogger = optim.Logger(paths.concat(opt.save, 'test.log'))


-- TODO 内存占用问题在这里开始发生
if model then
   parameters,gradParameters = model:getParameters()
end

----------------------------------------------------------------------
print '==> configuring optimizer'

optimState = {
   learningRate = opt.learningRate,
   weightDecay = opt.weightDecay,
   momentum = opt.momentum,
   learningRateDecay = 1e-7
}
optimMethod = optim.sgd

----------------------------------------------------------------------
print '==> defining training procedure'

function train(model)
   -- epoch tracker
   epoch = epoch or 1

   -- local vars
   local time = sys.clock()


   -- do one epoch
   print('==> doing epoch on training data:')
   print("==> online epoch # " .. epoch)

   print 'before creating closure'


   -- create closure to evaluate f(X) and df/dX
   feval = function(x)
      print "into closure"
      -- get new parameters
      if x ~= parameters then
         parameters:copy(x)
      end

      --next()
      -- reset gradients
      gradParameters:zero()

      -- f is the average of all criterions
      -- evaluate function for complete mini batch

      -- estimate f
      -- criterion:forward(model:forward(all[1]), alll[1])

      local output = model:forward(img)
      print(output:size())
      print(lb:size())
      local err = criterion:forward(output, lb)
      print 'estimate df/dW'
      local df_do = criterion:backward(output, lb)
      print 'model:backward'
      model:backward(img, df_do)
      print ("f == ", err)
      return err,gradParameters
   end
   print 'waiting for optimize...'
   --next()
   -- optimize on current mini-batch
   if optimMethod == optim.asgd then
      _,_,average = optimMethod(feval, parameters, optimState)
   else
      optimMethod(feval, parameters, optimState)
   end

   -- time taken
   time = sys.clock() - time
   print("\n==> time to learn 1 sample = " .. (time*1000) .. 'ms')
   --next()
   epoch = epoch + 1
   --gfx.image(model:get(1).weight, {zoom = 20, legend ='L1'..epoch})
   --gfx.image(re:forward(model:get(6).weight[1]))
   -- gfx.image(model:get(5).weight, {zoom = 20, legend ='L2'..epoch})
end
