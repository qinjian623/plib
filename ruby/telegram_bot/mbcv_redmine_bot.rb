require 'httpclient'
require 'json'
require 'digest'

def new_user (username, mail, password)
  @contex[username] = {}
  @contex[username][:mail] = mail
  @contex[username][:password] = password
end

def command_start(message)
  puts JSON.pretty_generate(message)
  username = message['from']['id']
  @contex[username] = {}
  @contex[username][:latest_chat_it] = message['chat']['id']
  return "User storage space created."
end

def command_register(message)
  username = message['from']['id']
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
  segs = message['text'].split(/\s/)
  t = Time.now
  msg = "Alarm"
  if segs.length == 3
    msg = segs[2]
    t =  t + segs[1].to_i * 60
  elsif segs.length == 2
    t = t + segs[1].to_i * 60
  else
    return "Wrong command format"
  end
  q = {
    :chat_id => message['chat']['id'],
    :text => msg,
    :message_id => message['message_id'],
    :t => t
  }
  puts JSON.pretty_generate(q)
  @contex[:Q].push(q)
  @contex[:Q].sort!{ |left,  right|
    left[:t] <=> right[:t]
  }
  return "Will reminder you at " + t.to_s
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
  :Q => [],
  :last_update_id => -1
}


def process_q()
  now = Time.now
  idx = 0
  for q in @contex[:Q]
    if q[:t] < now
      idx = idx + 1
      call(:sendMessage,
           {'chat_id' => q[:chat_id],
            'text' => q[:text],
            'reply_to_message_id' => q[:message_id]})
    end
  end
  @contex[:Q].shift(idx)
end


debug = true

while true
  if File.exists? 'contex.db'
    puts "Reading db..."
    @contex = Marshal.load(File.read('contex.db'))
    puts @contex
  end
  process_q
  updates = call(:getUpdates,
                 {'offset' => @contex[:last_update_id] + 1})
  # puts JSON.pretty_generate(updates.last)
  updates.each do | update|
    handle_update(update)
  end
  if updates.last
    @contex[:last_update_id] = updates.last['update_id']
  end
  File.write('contex.db', Marshal.dump(@contex))
  puts @contex if debug
  break
end


# puts Marshal.dump(ret)

