require 'torch'   -- torch
require 'image'   -- for color transforms
gfx = require 'gfx.js'  -- to visualize the dataset
require 'nn'      -- provides a normalization operator

function list_files(d)
   return io.popen(string.format("ls %s", d)):lines()
end

function load_jpg(fdir, fname)
   --print(fdir ..fname)
   return image.loadJPG(fdir .. '/' .. fname)
end


function load_jpgs_in_dir(dir, featn)
   local files = list_files(dir)
   local file_names = {}
   for fname in files do
      table.insert(file_names, fname)
   end

   local size = #file_names
   local data = torch.Tensor(size, featn, 300, 400)

   local i = 1
   for i = 1, size do
      data[i] = load_jpg(dir, file_names[i])
   end
   return data
end

function merge_tensor(list0, list1)
   local featn = (#list0)[2]
   local size0 = (#list0)[1]
   local size1 = (#list1)[1]
   local ret = torch.Tensor(size0 + size1, featn, 300, 400)
   for i = 1, size0 do
      ret[i] = list0[i]
   end
   for i = 1, size1 do
      ret[i+size0] = list1[i]
   end
   return ret
end

function merge_list(list0, list1)
   local size0 = (#list0)[1]
   local size1 = (#list1)[1]
   local ret = torch.Tensor(size0 + size1, 1)
   for i = 1, size0 do
      ret[i] = list0[i]
   end
   for i = 1, size1 do
      ret[i+size0] = list1[i]
   end
   return ret
end


function load_pos_and_neg(pos_dir, neg_dir)
   local pos = load_jpgs_in_dir(pos_dir, 3)
   local neg = load_jpgs_in_dir(neg_dir, 3)
   local posl = torch.Tensor((#pos)[1], 1)
   local negl = torch.Tensor((#neg)[1], 1)
   posl:fill(1)
   negl:fill(2)

   local all = merge_tensor(pos, neg)
   local alll = merge_list(posl, negl)
   return all, alll
end


-- all, alll = load_pos_and_neg('/home/qin/Documents/git/plib/opencv/pos', '/home/qin/Documents/git/plib/opencv/neg')
all, alll = load_pos_and_neg('/home/qin/car_rear/pos', '/home/qin/car_rear/neg')
