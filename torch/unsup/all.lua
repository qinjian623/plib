require 'gfx.go'

mtt = require 'data'

--dir = '/home/qin/Documents/GiveQinJian/'
--dir  = '/srv/ftp/caltech-lanes/unsup/'
dir = '/home/qin/Pictures/1/'
patch_size = 25
patch_step = 25
conv_input_size = 25
kernsize = 5
nfeats = 1
nout = 32

batch_size = 1
save_interval = 3000

require 'nn'
normkernel = image.gaussian1D(3)
pool = nn.SpatialMaxPooling(2, 2)
norm = nn.SpatialSubtractiveNormalization(1, normkernel)

-- pool_data ={}
-- print (data:size())
-- print (data:size(1))
-- for i = 1, data:size(1) do
--    table.insert(pool_data, pool:forward(data[i]))
-- end
--gfx.image(data)
--mtt.normalize(data)
--gfx.image(data)

dofile '1_data.lua'
dofile 'model.lua'
dofile 'train.lua'

--shuffle(ta)
iter = 0
err = 0
-- dataset = getdata('/home/qin/Documents/git/torch-tutorials/3_unsupervised/tr-berkeley-N5K-M56x56-lcn.ascii', patch_size, 0.1)
-- dataset:conv()
-- maxiter = 40000
-- train_model(model, dataset)

file_names = mtt.ls(dir)

now_iter = 0
for fname in file_names do
   im = image.loadPNG(dir .. fname)
   lcn_im = mtt.lcn(mtt.get_y_channel(im))
   -- gfx.image(lcn_im)
   im_3d = torch.Tensor(1, lcn_im:size(1), lcn_im:size(2))
   im_3d[1]:copy(lcn_im)
   -- gfx.image(im_3d[1])
   -- pic =
   -- norm:forward(pool:forward(norm:forward(mtt.get_y_channel(image.loadPNG(dir .. fname)))))
   one_pic_patches = mtt.cut_one_channel_picture(im_3d, patch_size, patch_size, patch_step, 0.2)
   if #(one_pic_patches:size()) > 3 then
      --gfx.image(one_pic_patches, {zoom = 5})
      maxiter = (#one_pic_patches)[1]
      train_model(model, one_pic_patches)
   end
   xlua.progress(now_iter, 100000)
   if now_iter > 100000 then
      torch.save('./model_'..now_iter, model)
      break
   end
end
