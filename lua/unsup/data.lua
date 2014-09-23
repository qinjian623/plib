-- This module is a part of mapbar torch codebase, contains tools to
-- load jpg, cut picture into patches and so on.
-- MTT is short for mapbar_torch_tools
require 'image'

local MTT={}

-- private
local function load_jpg(fname)
   return image.loadJPG(fname)
end

local function get_y_channel(rgb_image)
   return image.rgb2y(rgb_image)
end

-- functions

-- functional programming functions
function MTT.map(func, list)
   local ret = {}
   for k, v in pairs(list) do
      table.insert(ret, func(v))
   end
   return ret
end

function MTT.map_generator(func, gen)
   local ret={}
   for item in gen do
      table.insert(ret, func(item))
   end
   return ret
end

function MTT.ls(d)
   return io.popen(string.format("ls %s", d)):lines()
end

function MTT.load_jpg_in_dir(dir)
   function cat_dir(fname)
      return dir..fname
   end
   dir = dir .. '/'
   local images = MTT.map(load_jpg, MTT.map_generator(cat_dir, MTT.ls(dir)))
   return images
end

function MTT.load_y_of_jpg_in_dir(dir)
   local images = MTT.load_jpg_in_dir(dir)
   local y_images=MTT.map(get_y_channel, images)
   return MTT.tensor_list_to_tensor(y_images)
end

function MTT.tensor_list_to_tensor(tensorlist)
   local size = #tensorlist
   local tensor_storage_size = tensorlist[1]:nDimension()
   local tensor_size = #(tensorlist[1])

   local t = {}
   table.insert(t, size)
   for i = 1, tensor_storage_size do
      table.insert(t, tensor_size[i])
   end
   local new_size=torch.LongStorage(t)
   local data = torch.Tensor(new_size)

   for i = 1, size do
      data[i] = tensorlist[i]
   end
   return data
end

function MTT.cut_one_channel_picture(pic, cut_width, cut_height, jump, std_thredhold)
   local pic_width = pic:size()[2]
   local pic_height = pic:size()[3]
   local patches = {}

   for i=1, (pic_width - cut_width), jump do
      for j=1, (pic_height - cut_height), jump do
         local patch = pic:narrow(2, i, cut_width)
         patch = patch:narrow(3, j, cut_height)
         local patch_std = patch: std()
         if patch_std > std_thredhold then
            table.insert(patches, patch)
         end
      end
   end

   local ret = torch.Tensor(#patches, 1, cut_width, cut_height)
   for i =1, #patches do
      ret[i] = patches[i]
   end
   return ret
end

function MTT.normalize(data)
   mean = data[{ 1, {}, {}}]:mean()
   std = data[{1, {}, {}}]:std()
   data:add(-mean)
   data:div(std)
end

return MTT






