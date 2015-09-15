require 'socket'
require 'digest/md5'

code_book = "/home/qin/weka.log"
addr = 'localhost'
port = 2001
code_book_str = File.read(code_book)
md5sum = Digest::MD5.hexdigest(code_book_str)

s = TCPSocket.new addr, port
puts md5sum
s.puts md5sum

prng = Random.new
offset = prng.rand(1..(code_book_str.length-10))
length = 10
key = code_book_str[offset, length]

msg = "kkkkkkkkkk"
puts key
encode_str = msg.bytes.zip(key.bytes).map{|z|
  z[0]^z[1]
}
s.puts msg
s.puts offset.to_s + "," + length.to_s
s.write encode_str.map{|b| b.chr}.join
#s.write 0

s.close


