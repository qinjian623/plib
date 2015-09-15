require 'digest/md5'
require 'socket'
code_book = "../server.rb"
port = 2001

code_book_str = File.read(code_book)
md5sum = Digest::MD5.hexdigest(code_book_str)

server = TCPServer.new port
i = 0
loop do
  puts "listening..."
  c = server.accept
  c_md5sum = c.gets

  if (c_md5sum.strip == md5sum)
  else
    c.close
    next
  end
  c_id_str = c.gets

  pos = c.gets.split(',').map{|s| s.to_i}
  s = pos[0]
  l = pos[1]
  key = code_book_str[s, l]

  encode_str = c_id_str.strip.bytes.zip(key.bytes).map{|z|
    z[0]^z[1]
  }
  c_encode = c.read 10
  if c_encode.length != 10
    puts 'error'
    return
  end
  if (c_encode.bytes.to_a <=> encode_str) != 0
    puts key
    puts c_encode
    puts encode_str
  else
    puts "SUCC"
  end
  c.puts "SUCC"
  c.close
  puts i
  i = i+1
end
