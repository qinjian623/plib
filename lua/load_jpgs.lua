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
   local data = {}
   for fname in list_files(dir) do
      table.insert(data, get_y_channel(load_jpg(dir, fname)))
   end
   return data
end
