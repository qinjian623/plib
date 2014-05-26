require 'nn'
require 'unsup'

function build_conv_psd(params)
   -- params:
   conntable = nn.tables.full(params.nfiltersin, params.nfiltersout)
   kw, kh = params.kernelwidth, params.kernelheight
   iw, ih = params.width, params.height

   -- connection table:
   local decodertable = conntable:clone()
   decodertable[{ {},1 }] = conntable[{ {},2 }]
   decodertable[{ {},2 }] = conntable[{ {},1 }]
   local outputFeatures = conntable[{ {},2 }]:max()

   -- encoder:
   encoder = nn.Sequential()
   encoder:add(nn.SpatialConvolutionMap(conntable, kw, kh))
   encoder:add(nn.Tanh())
   encoder:add(nn.Diag(outputFeatures))

   -- decoder is L1 solution:
   decoder = unsup.SpatialConvFistaL1(decodertable, kw, kh, iw, ih, params.coefficient)
   --nn.Sequential()
   --decoder:add(nn.Linear(params.nfiltersout * params.kernelwidth * params.kernelheight, params.width * params.height))

   -- PSD autoencoder
   module = unsup.PSD(encoder, decoder, params.beta)

   -- verbose
   print('==> constructed convolutional predictive sparse decomposition (PSD) auto-encoder')
   return module
end

