mtt = require 'mtt'
require 'image'


function test(test_file)
   -- TODO 
   img = image.loadJPG(test_file)-- img = mtt.cut_one_picture(image.loadJPG(test_file), 719, 640, 640)[1]
   width = img:size(2)
   height = img:size(3)

   --local i = mtt.cut_one_picture(image.loadJPG(pic_file), 719, 640, 640)[1]
   img = image.scale(img, height/scale, width/scale)
   img = mtt.get_y_channel(img)
   img = mtt.lcn(img)

   --gfx.image(img[1])
   --print (#img)
   test_patches = mtt.cut_one_picture(img, p_size, p_size, jump)
   --print (#test_patches)
   -- gfx.image(test_patches, {zoom=5})

   yes = {}
   hps = math.floor((img:size(2)-1-p_size)/jump)+1
   wps = math.floor((img:size(3)-1-p_size)/jump)+1
   print ('--->', hps, wps)

   img = image.loadJPG(test_file)
   -- TODO
   img = image.loadJPG(test_file)-- mtt.cut_one_picture(image.loadJPG(test_file), 719, 640, 640)[1]
   img = image.scale(img, height/scale, width/scale)
   -- img = mtt.get_y_channel(img)
   img = mtt.lcn(img)
   for i=1, test_patches:size(1) do
      output = model:forward(test_patches[i])
      if output[1] > output[2] then
         col = i%wps
         if col==0 then
            col = wps
         end
         row = (i-col)/wps+1
         --print ('--->'..i, row, col)
         --if row < (hps*0.3) then

      --else
            table.insert(yes, test_patches[i])--mtt.lcn(test_patches[i]))
            img[1][(row-1)*jump + p_size/2][(col-1)*jump + p_size/2] = 10
--         end
      end
   end

   --gfx.image(yes, {zoom=5})
   gfx.image(img[1], {legend= test_file})
end
