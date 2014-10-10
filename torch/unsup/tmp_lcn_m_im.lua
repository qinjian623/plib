require 'gfx.go'
require 'nn'
mtt = require 'mtt'

function first_n(n, l)
   local ret = {}
   for i=1,n do
      table.insert(ret, l[i])
   end
   return ret
end

i = image.loadPNG '/tmp/road1.png'
i = (image.scale(i, 1920/4, 1080/4))
--image.display(i)
i = mtt.get_y_channel(i)
--image.display(i)
ni = mtt.lcn(i)
--image.display(ni)

label = image.loadJPG '/tmp/label1.jpg'
label = image.scale(label, 1920/4, 1080/4)
label = mtt.get_y_channel(label)


i_patches = mtt.cut_one_channel_picture(ni, 20, 20, 5)
l_patches = mtt.cut_one_channel_picture(label, 20, 20, 5)


poss = {}
negs = {}
for i=1,l_patches:size(1) do
   if l_patches[i][1]:sum() < 350 then
      table.insert(poss, i_patches[i][1])
   else
      table.insert(negs, i_patches[i][1])
   end
end
negs = first_n(#poss, negs)

posl = torch.Tensor((#poss), 1)
negl = torch.Tensor((#negs), 1)
all = mtt.merge_list(poss, negs)
alll = mtt.merge_list(posl, negl)

--print (#mtt.cut_one_channel_picture(label, 30, 30, 20))

--gfx.image(mtt.cut_one_channel_picture(ni, 30, 30, 10), {zoom = 5})
--gfx.image(mtt.cut_one_channel_picture(label, 30, 30, 10), {zoom = 5})
--image.save('/tmp/r.jpg',ni)
-- ni = mtt.lcn(model:forward(image.rgb2y(i)))
-- image.display(ni)

------------------------------------
-- ny = torch.Tensor(3, 296, 396) --
-- ny:fill(0)                     --
-- ny[1] = image.rgb2y(ni)        --
--                                --
-- y =  torch.Tensor(3, 300, 400) --
-- y:fill(0)                      --
-- y[1] = image.rgb2y(i)          --
------------------------------------



