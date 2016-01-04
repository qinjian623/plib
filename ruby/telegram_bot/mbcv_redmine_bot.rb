require 'httpclient'
require 'json'

@key = ARGV[0]

def call(method, paras = {})
  cli = HTTPClient.new
  url = "https://api.telegram.org/bot" + @key + "/" + method.to_s
  json = JSON.parse(cli.post(url, paras).content)
  if not json["ok"]
    raise method.to_s + ": "+ json["description"]
  else
    return json['result']
  end
end

def is_command? (message)
  message.key? 'text' and message['text'].start_with? '/'
end

def get_command(message)
  return (/\/(\w*)/ .match message['text'])[1]
end

def command_register(message)
  puts "Register from" + message['from']['username']
end

def dispatch(command, message)
  if methods().include? ('command_'+command).to_sym
    send 'command_'+command, message
  else
    puts "Command: " + command + " not found."
  end
end

def handle_message(message)
  if is_command? message
    command = get_command message
    dispatch(command, message)
  end
end

def is_message?(update)
  return update.key? 'message'
end

def handle_update(update)
  if is_message? update
    handle_message update['message']
  end
end

@contex = {
  
}

updates = call(:getUpdates)
puts JSON.pretty_generate(updates.last)
updates.each do | update|
  handle_update(update)
end

@contex[:last_update_id] = updates.last['update_id']

puts @contex[:last_update_id]
# puts Marshal.dump(ret)

