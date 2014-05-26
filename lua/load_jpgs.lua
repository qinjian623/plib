require 'image'
gfx = require 'gfx.js'

function list_files(d)
   return io.popen(string.format("ls %s", d)):lines()
end

function load_jpg(fdir, fname)
   -- print(fdir ..fname)
   return image.loadJPG(fdir .. fname)
end

function get_y_channel(rgb_image)
   return image.rgb2y(rgb_image)
end

function load_y_of_image_in_dir(fdir)
   local files = list_files(dir)
   local filenames = {}
   for fname in files do
      table.insert(filenames, fname)
   end

   local size = #filenames
   local data = torch.Tensor(size, 1, 360, 480)

   
   local i = 1
   for i= 1, size do
      data[i] = get_y_channel(load_jpg(dir, filenames[i]))
   end
   return data
end


function cut_pictures(pic, cut_width, cut_height, jump, std_thredhold)
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

function normalize(data)
   mean = data[{ 1, {}, {}}]:mean()
   std = data[{1, {}, {}}]:std()
   data:add(-mean)
   data:div(std)
end

