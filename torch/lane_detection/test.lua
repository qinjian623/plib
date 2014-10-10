mtt = require 'mtt'
require 'image'


function test(test_file)

   img = image.loadJPG(test_file)
   width = img:size(2)
   height = img:size(3)


   img = image.scale(img, height/scale, width/scale)
   img = mtt.get_y_channel(img)
   img = mtt.lcn(img)

   gfx.image(img[1])
   --print (#img)
   test_patches = mtt.cut_one_channel_picture(img, p_size, p_size, jump)
   --print (#test_patches)
   -- gfx.image(test_patches, {zoom=5})

   yes = {}
   hps = math.floor((img:size(2)-1-p_size)/jump)+1
   wps = math.floor((img:size(3)-1-p_size)/jump)+1
   print ('--->', hps, wps)
   for i=1, test_patches:size(1) do
      output = model:forward(mtt.lcn(test_patches[i]))
      if output[1][1] > output[1][2] then
         col = i%wps
         if col==0 then
            col = wps
         end
         row = (i-col)/wps+1
         --print ('--->'..i, row, col)
         table.insert(yes, mtt.lcn(test_patches[i]))
         img[1][(row-1)*jump + p_size/2][(col-1)*jump + p_size/2] = 10
      end
   end

   --gfx.image(yes, {zoom=5})
   gfx.image(img[1])
end
