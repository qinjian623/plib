package.path = package.path .. ';../lib/?.lua'
scale = 2
p_size = 15
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
all, alll = load_train_patches('/home/qin/car_rear/realroadImage/1951.jpg',
                               '/home/qin/car_rear/realroadImage/label1951.jpg',
                               scale, p_size, p_size, jump, thredhold)

-- print (#alll)
print '----------------- TRAIN ------------------'
for t = 1,75,1 do
	train()
        if confusion.totalValid > 0.99999 then
           break
        end
        confusion:zero()
end

dofile 'test.lua'
test_file = '/home/qin/car_rear/realroadImage/2491.jpg'--1951.jpg'--1303.jpg'--
test(test_file)
test_file = '/home/qin/car_rear/realroadImage/1303.jpg'--2491.jpg'--1951.jpg'--
test(test_file)
test_file = '/home/qin/car_rear/realroadImage/1951.jpg'--1303.jpg'--2491.jpg'--
test(test_file)
