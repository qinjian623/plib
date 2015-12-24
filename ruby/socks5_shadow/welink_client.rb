require 'socket'

addr = ARGV[0]
port = 6806

s = TCPSocket.new addr, port
#s.puts '{"moduleName":"WeLink_SDK","version":0,"platform":"wince","command":{"method":"onHuReady","extData":{"width":800,"height":480}}}'
while true
  data = s.read 40000
  puts data
end
#s.puts "screen 320 240"
#puts s.gets
s.close

######################################################################
# byte[] bHeader = readBuffer(4);                                    #
# if (bHeader != null && bHeader.length == 4) {                      #
#      if ((bHeader[0] == 'W') && (bHeader[1] == 'L')) {             #
# 	  int iHdrLen = bHeader[3];                                  #
# 	  if (iHdrLen > 0)                                           #
# 	    readBuffer(iHdrLen);                                     #
# 	    DataInputStream dis = new DataInputStream(mIs);          #
# 	    int nLen = dis.readInt();                                #
# 	    if (nLen > 0) {                                          #
# 		 byte[] bufImg = readBuffer(nLen);                   #
# 	       }                                                     #
# 	}                                                            #
#    }                                                               #
######################################################################
