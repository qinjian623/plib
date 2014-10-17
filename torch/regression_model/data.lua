mtt = require 'mtt'

function first_n(n, l)
   local ret = {}
   for i=1,n do
      table.insert(ret, l[i])
   end
   return ret
end


function load_one_pic(pic_file, label_file, scale, patch_width, patch_height, step, label_thredhold)
   local i = image.loadJPG(pic_file)--mtt.cut_one_picture(image.loadJPG(pic_file), 719, 640, 640)[1]
   local label = image.loadJPG(label_file)--mtt.cut_one_picture(image.loadJPG(label_file), 719, 640, 640)[1]
   local width = i:size(2)
   local height = i:size(3)

   i = image.scale(i, height/scale, width/scale)
   i = mtt.get_y_channel(i)
   i = mtt.lcn(i)
   label = image.scale(label, height/scale, width/scale)
   label = mtt.get_y_channel(label)
   label = mtt.lcn(label)


   local nw =  label:size(2)/4
   local nh = label:size(3)/4
   label=image.scale(label[1], nh, nw)
   return i, label
end

function load_train_data(pic_dir, label_dir, scale, patch_width, patch_height, step, label_thredhold)
   local all = {}
   local alll= {}
   for file_name in mtt.ls(label_dir) do
      local pic_file = pic_dir .. '/' .. file_name
      local label_file = label_dir .. '/' .. file_name
      x, y = load_one_pic(pic_file, label_file, scale, patch_width, patch_height, step, label_thredhold)
      table.insert(all, x)
      table.insert(alll, y)
   end
   return all, alll
end






