require 'httpclient'
require 'json'

cli = HTTPClient.new
test_res = cli.get_content("https://api.telegram.org/bot"+ARGV[0]+"/getMe")
get_me_json = JSON.parse(test_res)
if get_me_json['ok']
  puts "Connection OK."
end

def call(method, paras)
  
end
