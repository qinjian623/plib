require 'httpclient'
require 'json'
require 'digest'

def new_user (username, mail, password)
  @contex[username] = {}
  @contex[username][:mail] = mail
  @contex[username][:password] = password
end

def command_register(message)
  username = message['from']['username']
  mo = /\/(\w*) *(\w*@\w*\.com)\s*(\w*)/.match(message['text'])
  if mo
    mail = mo[2]
    password = Digest::SHA256.digest mo[3]
    if not @contex.key? username
      new_user username, mail, password
      return "New user added."
    else
      if  @contex[username][:password] == password
        @contex[username][:mail] = mail
        return "User mail reset done."
      else
        return "Wrong password."
      end
    end
  else
    return "Wrong command format."
  end
end

def command_reminder(message)
  
end

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


def dispatch(command, message)
  begin
    response = send 'command_'+command, message
    call(:sendMessage,
         {'chat_id' => message['chat']['id'],
          'text' => response,
          'reply_to_message_id' => message['message_id']})
  rescue NoMethodError
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

