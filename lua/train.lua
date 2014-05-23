
function train_model(module, dataset, params)
   -- get all parameters
   x,dl_dx,ddl_ddx = module:getParameters()

   -- training errors
   local err = 0
   local iter = 0

   for t = 1,params.maxiter,params.batchsize do
      --------------------------------------------------------------------
      -- progress
      -- 简单的进度调整
      iter = iter+1
      xlua.progress(iter, params.statinterval)

      --------------------------------------------------------------------
      -- create mini-batch
      -- 一个batch大小的数据集
      local example = dataset[t]
      local inputs = {}
      local targets = {}
      for i = t,t+params.batchsize-1 do
         -- load new sample
         local sample = dataset[i]
         table.insert(inputs, sample)
         table.insert(targets, sample)
      end

      --------------------------------------------------------------------
      -- define eval closure
      --
      local feval = function()
         -- reset gradient/f
         local f = 0
         dl_dx:zero()

         -- estimate f and gradients, for minibatch
         -- TODO 这块的三个函数需要查看文档
         for i = 1,#inputs do
            -- f
            -- ths loss 重构的loss
            f = f + module:updateOutput(inputs[i], targets[i])
            
            -- gradients
            module:updateGradInput(inputs[i], targets[i])
            module:accGradParameters(inputs[i], targets[i])
         end

         -- normalize
         dl_dx:div(#inputs)
         f = f/#inputs

         -- return f and df/dx
         return f,dl_dx
      end

      --------------------------------------------------------------------
      -- one SGD step
      --
      sgdconf = sgdconf or {learningRate = params.eta,
                            learningRateDecay = params.etadecay,
                            learningRates = etas,
                            momentum = params.momentum}
      _,fs = optim.sgd(feval, x, sgdconf)
      err = err + fs[1]

      -- normalize
      module:normalize()

      --------------------------------------------------------------------
      -- compute statistics / report error
      --
      if math.fmod(t , params.statinterval) == 0 then

         -- report
         print('==> iteration = ' .. t .. ', average loss = ' .. err/params.statinterval)

         -- get weights
         eweight = module.encoder.modules[1].weight
         if module.decoder.D then
            dweight = module.decoder.D.weight
         else
            dweight = module.decoder.modules[1].weight
         end

         -- reshape weights if linear matrix is used
         if params.model:find('linear') then
            dweight = dweight:transpose(1,2):unfold(2,params.inputsize,params.inputsize)
            eweight = eweight:unfold(2,params.inputsize,params.inputsize)
         end

         -- render filters
         dd = image.toDisplayTensor{input=dweight,
                                    padding=2,
                                    nrow=math.floor(math.sqrt(params.nfiltersout)),
                                    symmetric=true}
         de = image.toDisplayTensor{input=eweight,
                                    padding=2,
                                    nrow=math.floor(math.sqrt(params.nfiltersout)),
                                    symmetric=true}

         -- live display
         if params.display then
            _win1_ = gfx.image(dd, {win=_win1_, legend='Decoder filters', zoom=10})
            _win2_ = gfx.image(de, {win=_win2_, legend='Encoder filters', zoom=10})
         end

         -- save stuff
         image.save(params.rundir .. '/filters_dec_' .. t .. '.jpg', dd)
         image.save(params.rundir .. '/filters_enc_' .. t .. '.jpg', de)
         torch.save(params.rundir .. '/model_' .. t .. '.bin', module)

         -- reset counters
         err = 0; iter = 0
      end
   end
end

