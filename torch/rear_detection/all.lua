package.path = package.path .. ';../lib/?.lua'


negs_dir = '/srv/ftp/small_imgs/' --'/root/neg'--'/srv/ftp/small_imgs/'--'/home/qin/car_rear/pos'
poss_dir = '/home/qin/car_rear/1363764871_t_o/' --'/root/pos'--'/home/qin/car_rear/1363764871_t_o/'--'/home/qin/car_rear/neg'

scale_width = 30
scale_height = 30

dofile 'data.lua'
dofile 'model.lua'
dofile 'loss.lua'
dofile 'train.lua'

mtt = require 'mtt'

require 'gfx.go'

-- gfx.image(model:get(1).weight, {zoom = 20, legend ='L1 init'})


function preprocess(im)
   return mtt.lcn(image.rgb2y(im))
   --return mtt.lcn(image.scale(im, scale_width, scale_height))
end

function test(negs_dir, poss_dir)
   negs = load_jpgs_in_dir(negs_dir, 3, 1, 1000)
   poss = load_jpgs_in_dir(poss_dir, 3, 1, 1000)
   cf = optim.ConfusionMatrix(2)
   --print 'negs\n'
   time = sys.clock()
   for i=1, negs:size(1) do
      output = model:forward(preprocess(negs[i]))
      cf:add(output, 2)
      -----------------------------------
      -- if output[1] > output[2] then --
      --    print (i)                  --
      -- end                           --
      -----------------------------------
   end

   --print 'poss\n'
   for i=1, poss:size(1) do
      output = model:forward(preprocess(poss[i]))
      cf:add(output, 1)
      -----------------------------------
      -- if output[1] < output[2] then --
      --    print (i)                  --
      -- end                           --
      -----------------------------------
   end
   time = sys.clock() - time
   time = time/(poss:size(1)+negs:size(1))
   print("\n==> time to predict 1 sample = " .. (time*1000) .. 'ms')
   print(cf)
end


for c = 1, 3 do
   for t = 0, 20 do
      local fbegin = t*1000+1
      local fend = fbegin+1000
      print (fbegin, fend)
      all, alll = load_pos_and_neg(poss_dir, negs_dir, fbegin, fend)
      lcn_all = torch.Tensor(all:size(1), 3, scale_height-4, scale_width-4)
      for i=1, all:size(1) do
         lcn_all[i] = preprocess(all[i])
      end
      all = lcn_all
      --print (#all)
      --print (#alll)
      train()
      local filename = paths.concat(opt.save, 'model.net')
      os.execute('mkdir -p ' .. sys.dirname(filename))
      print('==> saving model to '..filename)
      torch.save(filename, model)
   end
end
test(negs_dir, poss_dir)
-- save/log current net
gfx.image(model:get(1).weight, {zoom = 10, legend ='Layer 1 fini'})
