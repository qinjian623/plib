-- This module is a part of mapbar torch codebase, contains tools to
-- load jpg, cut picture into patches and so on.
-- MTT is short for mapbar_torch_tools
require 'image'

local MTT={}

-- private
local function lcn(im, gs)
   local gfh = image.gaussian{width=gs,height=1,normalize=true}
   local gfv = image.gaussian{width=1,height=gs,normalize=true}
   local gf = image.gaussian{width=gs,height=gs,normalize=true}
   local mn = im:mean()
   local std = im:std()

   if data_verbose then
      print('im',mn,std,im:min(),im:max())
   end
   -- 平均值与方差
   im:add(-mn)
   im:div(std)
   if data_verbose then
      print('im',im:min(),im:max(),im:mean(), im:std())
   end

   local imsq = torch.Tensor()
   local lmnsqh = torch.Tensor()
   local lmnsq = torch.Tensor()
   imsq:resizeAs(im):copy(im):cmul(im)
   if data_verbose then
      print('imsq',imsq:min(),imsq:max())
   end

   -- gfh横向的高斯
   lmnh = torch.conv2(im,gfh)
   -- gfh纵向的高斯
   lmn = torch.conv2(lmnh,gfv)
   if data_verbose then
      print('lmn',lmn:min(),lmn:max())
   end
   --local lmn = torch.conv2(im,gf)
   torch.conv2(lmnsqh,imsq,gfh)
   torch.conv2(lmnsq,lmnsqh,gfv)
   if data_verbose then
      print('lmnsq',lmnsq:min(),lmnsq:max())
   end
   local lvar = torch.Tensor()
   lvar:resizeAs(lmn):copy(lmn):cmul(lmn)
   lvar:mul(-1)
   lvar:add(lmnsq)
   if data_verbose then
      print('2',lvar:min(),lvar:max())
   end
   lvar:apply(function (x) if x<0 then return 0 else return x end end)
   if data_verbose then
      print('2',lvar:min(),lvar:max())
   end
   local lstd = lvar
   lstd:sqrt()
   lstd:apply(function (x) if x<1 then return 1 else return x end end)
   if data_verbose then
      print('lstd',lstd:min(),lstd:max())
   end
   local shift = (gs+1)/2
   local nim = im:narrow(1,shift,im:size(1)-(gs-1)):narrow(2,shift,im:size(2)-(gs-1))
   nim:add(-1,lmn)
   nim:cdiv(lstd)
   if data_verbose then
      print('nim',nim:min(),nim:max())
   end
   return nim
end


-- functions

-- 从指定的文件路径中载入JPG文件，返回一个Tensor
function MTT.load_jpg(fname)
   return image.loadJPG(fname)
end

-- 获得rgb图片的y通道
function MTT.get_y_channel(rgb_image)
   return image.rgb2y(rgb_image)
end

-- 用于list的map函数，返回一个处理后的list
function MTT.map(func, list)
   local ret = {}
   for k, v in pairs(list) do
      table.insert(ret, func(v))
   end
   return ret
end

-- 用于生成器的map函数，返回一个处理后的list
function MTT.map_generator(func, gen)
   local ret={}
   for item in gen do
      table.insert(ret, func(item))
   end
   return ret
end

-- ls命令的包装，返回的是一个生成器
function MTT.ls(d)
   return io.popen(string.format("ls %s", d)):lines()
end

-- cat命令的包装，返回的是一个生成器
function MTT.cat(d)
   return io.popen(string.format("cat %s", d)):lines()
end


-- 载入文件夹中所有的jpg图片
function MTT.load_jpg_in_dir(dir)
   function cat_dir(fname)
      return dir..fname
   end
   dir = dir .. '/'
   local images = MTT.map(load_jpg, MTT.map_generator(cat_dir, MTT.ls(dir)))
   return images
end

-- 文件夹中所有图片的y通道
function MTT.load_y_of_jpg_in_dir(dir)
   local images = MTT.load_jpg_in_dir(dir)
   local y_images=MTT.map(get_y_channel, images)
   return MTT.tensor_list_to_tensor(y_images)
end


-- LCN的实现, 高斯核默认大小为5
-- TODO 等待实现对多图层的支持，目前只是生成第一图层的LCN，故API不会稳
-- 定
function MTT.lcn(im, gs)
   gs = gs or 5
   local channels_count = im:size()[1]
   local new_width = im:size()[2]-gs+1
   local new_height = im:size()[3]-gs+1
   local ret = torch.Tensor(channels_count, new_width, new_height)
   for i =1, channels_count do
      ni = lcn(im[i], gs)
      ret[i] = ni
   end
   return ret
end


-- 将Tensor列表转换为一个维度加1的Tensor
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

-- 将图片以指定宽度和高度、步长切割，返回其中方差大于指定阈值的，阈值
-- 默认为0.2
-- TODO 待增加多图层的操作
function MTT.cut_one_channel_picture(pic, cut_width, cut_height, jump, std_thredhold)
   local std_thredhold = std_thredhold or nil
   local pic_width = pic:size()[2]
   local pic_height = pic:size()[3]
   local patches = {}

   for i=1, (pic_width - cut_width), jump do
      for j=1, (pic_height - cut_height), jump do
         local patch = pic:narrow(2, i, cut_width)
         patch = patch:narrow(3, j, cut_height)
         local patch_std = patch: std()
         if (not std_thredhold) or patch_std > std_thredhold then
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

function MTT.merge_list(list0, list1)
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


-- 简单的normalize
function MTT.normalize(data)
   mean = data[{ 1, {}, {}}]:mean()
   std = data[{1, {}, {}}]:std()
   data:add(-mean)
   data:div(std)
end

-- 重新洗牌list，不要用于Tensor的洗牌会有内存问题
function MTT.shuffle(t)
   local n = #t

   while true do
      if n < 2 then
         break
      end
      -- n is now the last pertinent index
      local k = math.random(n) -- 1 <= k <= n
      -- Quick swap
      t[n], t[k] = t[k], t[n]
      n = n - 1
   end

   return t
end

-- 等待用户输入以继续
function MTT.next()
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
return MTT






