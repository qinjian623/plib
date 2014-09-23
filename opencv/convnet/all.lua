

dofile 'data.lua'
dofile 'model.lua'
dofile 'loss.lua'
dofile 'train.lua'

for t = 1,20,1 do
	train()
end
-- save/log current net
local filename = paths.concat(opt.save, 'model.net')
os.execute('mkdir -p ' .. sys.dirname(filename))
print('==> saving model to '..filename)
torch.save(filename, model)
