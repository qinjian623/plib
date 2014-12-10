package.path = package.path .. ';../lib/?.lua'

-- Torch library
require 'gfx.go'
require 'image'

-- Plib
mtt = require 'mtt'

function regression_label(lcn_img, tag)
   local ret = torch.Tensor(lcn_img:size(1), lcn_img:size(2))
   for i = 1, lcn_img:size(1) do
      for j = 1, lcn_img:size(2) do
         if(lcn_img[i][j] > 0.0001) then
            ret[i][j] = math.min(2, tag)
         else
            ret[i][j] = 0
         end
      end
   end
   return ret
end

function next()
   local answer = nil
   while answer ~= '' and answer ~= 'y' and answer ~= 'Y' and neverstall ~= true do
      io.write("continue ([y]/n/!)? ")
      io.flush()
      answer=io.read()
      if answer == '!' then
         neverstall = true
      end
      if answer == 'n' then
         print('exiting...')
         os.exit()
      end
   end
   print ''
end

function merge_channels(c0_3, c1_1)
   local ret = torch.Tensor(c0_3:size(1)+c1_1:size(1), c1_1:size(2), c1_1:size(3))
   for i = 1, c0_3:size(1) do
      ret[i] = c0_3[i]
   end
   for i = 1, c1_1:size(1) do
      ret[i+c0_3:size(1)] = c1_1[i]
   end
   return ret
end

label_dir = "/home/qin/car_rear/close_test/label_2014_11_09_for_nn_filled/"
pics_dir = "/home/qin/car_rear/trainset_pic_11-3/extract/"


width = 320
height = 160
o_w = 60+4
o_h = 20+4
nfeats = 4
raw = false
view = false

dofile 'model.lua'
dofile 'loss.lua'
dofile 'train.lua'


kern = torch.Tensor(5, 5)
kern:fill(0)
kern[3][3] = 1

for i = 3, 1, -1 do
   print ('traing iter: ', i)
   for file_name in mtt.ls(label_dir) do
      -- next()
      if raw then
         img = image.scale(image.loadJPG(pics_dir .. file_name), width, height)
         lb_img = image.scale(image.loadJPG(label_dir .. file_name), o_w, o_h)[1]
      else
         -- TODO memory issue
         img = image.loadJPG(label_dir .. file_name)
         lb_img = image.scale(img, o_w -4, o_h -4)[1]
         img = mtt.lcn(
            image.scale(
               mtt.get_y_channel(image.loadJPG(pics_dir .. file_name)),
               width,
               height))
         cl_img = mtt.lcn(
            image.scale(
               image.loadJPG(pics_dir .. file_name),
               width,
               height))
         img = merge_channels(cl_img, img)
      end

      lb = regression_label(lb_img, i)
      if raw and view then
         gfx.image(all[1])
         gfx.image(alll[1], {zoom=4})
      elseif view then
         gfx.image(all[1][1])
         gfx.image(alll[1], {zoom=4})
      end

      train(model)
      gfx.image(img[1])
      gfx.image({model:forward(img)[1], lb}, {zoom = 4})
      --gfx.image(model:forward(img)[1], {zoom = 4, legend=file_name})
      --gfx.image(lb, {zoom = 4, legend=file_name .. '-lb'})
   end
end

next()
model_file_name = '/tmp/conv_model'
torch.save(model_file_name, model)
print('model saved to ' .. model_file_name)

show_num = 1
for file_name in mtt.ls(label_dir) do
   if raw then
      img = image.scale(
         image.loadJPG(pics_dir .. file_name),
         width,
         height)
   else
      img = mtt.lcn(
         image.scale(
            mtt.get_y_channel(image.loadJPG(pics_dir .. file_name)),
            width,
            height))
      local cl_img = mtt.lcn(
         image.scale(
            image.loadJPG(pics_dir .. file_name),
            width,
            height))
      img = merge_channels(cl_img, img)
   end
   o = model:forward(img)
   gfx.image(o[1], {zoom=4, legend=file_name})
   show_num  = show_num - 1
   if (show_num < 0) then
      break
   end
end
print "Training done..."
-- r = model:forward(all[1])
-- gfx.image(r, {zoom = 8})
-- gfx.image(alll[1], {zoom = 8})


