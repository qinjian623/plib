require 'gfx.go'
mtt = require 'data'

dir = '/home/qin/Pictures/1/'

data = mtt.load_y_of_jpg_in_dir(dir)
--gfx.image(data)
mtt.normalize(data)
--gfx.image(data)
dofile 'model.lua'
dofile 'train.lua'

for i = 1, data:size(1) do
   print (i)
   one_pic_patches = mtt.cut_one_channel_picture(data[1], 20, 20, 5, 0.1)
   train_model(model, one_pic_patches)
end
