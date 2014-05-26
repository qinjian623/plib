

dofile 'load_jpgs.lua'
dofile 'build_model.lua'
dofile 'train.lua'

params = {
nfiltersin   = 1,
nfiltersout  = 40,
kernelwidth  = 20,
kernelheight = 20,
width        = 40,
height       = 40,
coefficient  = 1,
batchsize    = 5,
eta          = 2e-3,
etadecay     = 1e-5,
maxiter      = 500,
statinterval = 1,
beta         = 1,
threads      = 4,
rundir = '/home/qin/nnmd_1'
}

torch.setnumthreads(params.threads)

function next()
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

dir = "/home/qin/Pictures/1/"
data = load_y_of_image_in_dir(dir)
normalize(data)
one_cuts = cut_pictures(data[2][{{}, {}, {}}], params.width, params.height, 1, 0.3)
--print(one_cuts[1]:size())

-- pic  = data[1][{1, {}, {}}]
-- cut_width = 30
-- cut_height = 30
-- jump = 10
-- std_thredhold = 0.2
-- local pic_width = pic:size()[1]
-- local pic_height = pic:size()[2]
-- local patches = {}

-- for i=1, (pic_width - cut_width), jump do
--    for j = 1, (pic_height - cut_height), jump do
--       local patch = pic:narrow(1, i, cut_width)
--       patch =  pic:narrow(2, j, cut_height)
--       local patch_std = patch: std()
--       if patch_std > std_thredhold then
--          table.insert(patches, patch)
--       end
--    end
-- end

model = build_conv_psd(params)
train_model(model, one_cuts, params)
--torch.save(params.rundir .. '/model_' .. t .. '.bin', model)

