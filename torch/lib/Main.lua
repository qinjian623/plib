mtt = require 'mtt'
require 'gfx.go'

file = '/home/qin/car_rear/realroadImage/1053.jpg'

gfx.image(mtt.cut_one_picture(mtt.lcn(image.loadJPG(file)), 100, 100, 100))
