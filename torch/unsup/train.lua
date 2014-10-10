-- 训练过程，输入为模型和数据集
function train_model(model, dataset)
   -- get all parameters
   x,dl_dx,ddl_ddx = model:getParameters()

   -- training errors
   --local err = 0
   --local iter = 0

   for t = 1, maxiter , batch_size do
      --------------------------------------------------------------------
      -- progress
      -- 简单的进度调整
      iter = iter + batch_size
      now_iter = now_iter + 1
      -- xlua.progress(iter, save_interval)

      --------------------------------------------------------------------
      -- create mini-batch
      inputs = {}
      targets = {}
      for i = t,t+batch_size-1 do
         -- load new sample
         sample = dataset[i]
         input = sample:clone()
         target = sample:clone()
         table.insert(inputs, input)
         table.insert(targets, target)
      end

      feval = function()
         -- reset gradient/f
         local f = 0
         dl_dx:zero()

         -- estimate f and gradients, for minibatch
         -- TODO 这块的三个函数需要查看文档
         for i = 1,#inputs do
            -- f
            -- ths loss 重构的loss
            f = f + model:updateOutput(inputs[i], targets[i])
            --gfx.image(inputs)
            --gfx.image(targets)
            --next()
            -- gradients
            model:updateGradInput(inputs[i], targets[i])
            model:accGradParameters(inputs[i], targets[i])
         end

         -- normalize
         dl_dx:div(#inputs)
         f = f/#inputs
         -- print (dl_dx[1]..'\n')
         -- return f and df/dx
         return f,dl_dx
      end

      --------------------------------------------------------------------
      -- one SGD step
      --
      sgdconf = sgdconf or {learningRate = 2e-3,
                            learningRateDecay = 1e-5,
                            learningRates = etas,
                            momentum = 0}
      _,fs = optim.sgd(feval, x, sgdconf)
      err = err + fs[1]

      -- normalize
      model:normalize()

      --------------------------------------------------------------------
      -- compute statistics / report error
      --
      if iter >= save_interval then
         -- report
         print('==> iteration = ' .. t .. ', average loss = ' .. err/iter)

         -- get weights
         eweight = model.encoder.modules[1].weight
         if model.decoder.D then
            dweight = model.decoder.D.weight
         else
            dweight = model.decoder.modules[1].weight
         end

         -- render filters
         dd = image.toDisplayTensor{input=dweight,
                                    padding=2,
                                    nrow=math.floor(math.sqrt(16)),
                                    symmetric=true}
         de = image.toDisplayTensor{input=eweight,
                                    padding=2,
                                    nrow=math.floor(math.sqrt(16)),
                                    symmetric=true}

         -- live display
         if true then
            gfx.image(dd, {zoom = 10, legend ='decoder'})
            gfx.image(de, {zoom = 10, legend ='encoder'})
            -- _win1_ = gfx.image(dd, {win=_win1_, legend='Decoder filters', zoom=10})
            -- _win2_ = gfx.image(de, {win=_win2_, legend='Encoder filters', zoom=10})
         end

         -- save stuff
         -- image.save('.' .. '/filters_dec_' .. t .. '.jpg', dd)
         -- image.save('.' .. '/filters_enc_' .. t .. '.jpg', de)
         -- torch.save(params.rundir .. '/model_' .. t .. '.bin', module)
         -- reset counters
         err = 0; iter = 0
      end
   end
end

