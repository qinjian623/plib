package.path = package.path .. ';../lib/?.lua'
scale = 2
gs = 1

p_size = 30
jump = 5
thredhold = 0.2

dofile 'data.lua'
print '----------------- MODEL ------------------'
dofile 'model.lua'
print '----------------- LOSS  ------------------'
dofile 'loss.lua'

dofile 'train.lua'

mtt = require 'mtt'

require 'gfx.go'

print '----------------- DATA  ------------------'
-- all, alll = load_train_patches('/home/qin/car_rear/realroadImage/1951.jpg',
--                                '/home/qin/car_rear/realroadImage/label1951.jpg',
--                                scale, p_size, p_size, jump, thredhold)
all, alll = load_train_data('/home/qin/car_rear/realroadImage/',
                            '/home/qin/car_rear/label_rectangle/',
                            scale, p_size, p_size, jump, thredhold)
print (alll[1]:size())
print '----------------- TRAIN ------------------'
for t = 1,75,1 do
	train()
        gfx.image(model:get(1).weight, {zoom=10})
        if confusion.totalValid > 0.99999 then
           break
        end
        confusion:zero()
end
torch.save('/tmp/model', model)
dofile 'test.lua'
test_dir = '/home/qin/car_rear/realroadImage/'
for i=1,9 do
   test(test_dir .. i ..'000.jpg')
end
-- test_file = '/home/qin/car_rear/realroadImage/2491.jpg'--1951.jpg'--1303.jpg'--
-- test(test_file)
-- test_file = '/home/qin/car_rear/realroadImage/1303.jpg'--2491.jpg'--1951.jpg'--
-- test(test_file)
-- test_file = '/home/qin/car_rear/realroadImage/1951.jpg'--1303.jpg'--2491.jpg'--
-- test(test_file)
