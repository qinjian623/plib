mtt = require 'mtt'

function first_n(n, l)
   local ret = {}
   for i=1,n do
      table.insert(ret, l[i])
   end
   return ret
end

function load_train_patches(pic_file, label_file, scale, patch_width, patch_height, step, label_thredhold)
   i = image.loadJPG(pic_file)
   label = image.loadJPG(label_file)
   width = i:size(2)
   height = i:size(3)
   i = image.scale(i, height/scale, width/scale)
   i = mtt.get_y_channel(i)
   i = mtt.lcn(i)


   label = image.scale(label, height/scale, width/scale)
   label = mtt.get_y_channel(label)
   label = mtt.lcn(label)


   i_patches = mtt.cut_one_channel_picture(i, patch_width, patch_height, step)
   l_patches = mtt.cut_one_channel_picture(label, patch_width, patch_height, step)

   --gfx.image(label[1])
   --gfx.image(i[1])
   poss = {}
   negs = {}

   l_ = {}
   f_ = {}
   for i=1,l_patches:size(1) do
      if l_patches[i][1]:std() >  label_thredhold then
         table.insert(poss, mtt.lcn(i_patches[i]))
         table.insert(l_, mtt.lcn(l_patches[i]))
      elseif l_patches[i][1]:std() < 0.01 then
         table.insert(negs, mtt.lcn(i_patches[i]))
         table.insert(f_, mtt.lcn(l_patches[i]))
      end
   end

   local append_round = math.floor((#negs)/(#poss)) - 10
   print ('negs size:', #negs)
   print ('poss size:', #poss)
   print (append_round)
   local old_number = #poss
   for j=1, 3 do
      for i=1, old_number do
         table.insert(poss, poss[i])
      end
   end
   print 'shuffle now...'
   negs = first_n(#poss, mtt.shuffle(negs))

   posl = torch.Tensor((#poss), 1)
   posl:fill(1)
   negl = torch.Tensor((#negs), 1)
   negl:fill(2)

   print 'merge now...'
   -- gfx.image(mtt.tensor_list_to_tensor(l_),{zoom=10})
   -- gfx.image(mtt.tensor_list_to_tensor(first_n(#poss,f_)),{zoom=10})
   -- gfx.image(poss,{zoom=10})
   -- gfx.image(negs,{zoom=10, legend='asdfasdf'})

   all = mtt.merge_pic_tensor(mtt.tensor_list_to_tensor(poss), mtt.tensor_list_to_tensor(negs), patch_width-4, patch_height-4)
   alll = mtt.merge_list(posl, negl)
   return all, alll
end





