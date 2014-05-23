

dofile 'load_jpgs.lua'
dofile 'build_model.lua'
dofile 'train.lua'

params = {
nfiltersin   = 1,
nfiltersout  = 32,
kernelwidth  = 20,
kernelheight = 20,
width        = 480,
height       = 360,
coefficient  = 1,
batchsize    = 1,
eta          = 2e-3,
etadecay     = 1e-5,
maxiter      = 1000,
statinterval = 50,
beta         = 1,
threads      = 4
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
model = build_conv_psd(params)
train_model(model, data, params)

