package.path = package.path .. ';../lib/?.lua'

scale_width = 100
scale_height = 75


dofile 'data.lua'
dofile 'model.lua'
dofile 'loss.lua'
dofile 'train.lua'

mtt = require 'mtt'

require 'gfx.go'

gfx.image(model:get(1).weight, {zoom = 20, legend ='L1 init'})


function preprocess(im)
   return mtt.lcn(image.scale(im, scale_width, scale_height))
end

function test()
   negs = load_jpgs_in_dir('/home/qin/car_rear/test/neg', 3)
   poss = load_jpgs_in_dir('/home/qin/car_rear/test/pos', 3)
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


lcn_all = torch.Tensor(all:size(1), 3, scale_height-4, scale_width-4)
for i=1, all:size(1) do
   lcn_all[i] = preprocess(all[i])
end
all = lcn_all

print (#all)
print (#alll)
for t = 1,25,1 do
	train()
        test()
end
-- save/log current net
local filename = paths.concat(opt.save, 'model.net')
os.execute('mkdir -p ' .. sys.dirname(filename))
print('==> saving model to '..filename)
torch.save(filename, model)


gfx.image(model:get(1).weight, {zoom = 20, legend ='L1 fini'})
