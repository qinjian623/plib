require 'image'
mtt = require 'mtt'

intput_dir = '/home/qin/car_rear/raw/neg/'
output_dir = '/home/qin/car_rear/neg/'

for file_name in mtt.ls(intput_dir) do
   raw = image.loadJPG(intput_dir .. file_name)
   new = image.scale(raw, 400, 300)
   image.saveJPG(output_dir..file_name, new)
end

intput_dir = '/home/qin/car_rear/raw/pos/'
output_dir = '/home/qin/car_rear/pos/'

for file_name in mtt.ls(intput_dir) do
   raw = image.loadJPG(intput_dir .. file_name)
   new = image.scale(raw, 400, 300)
   image.saveJPG(output_dir..file_name, new)
end

