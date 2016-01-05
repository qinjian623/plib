require 'httpclient'
require 'json'
require 'digest'
require 'erb'
@redmine_domain = "http://192.168.1.244:3000"
@redmine_methods = {
  :issues => "http://192.168.1.244:3000/issues.json",
}

@output_template = "# <%= issue['id'] %> *<%= issue['subject'] %>* <% if not issue['description'].empty? %> _<%= issue['description']%>_ <% end %>"

def call_redmine(method, username, password, paras = {})
  client = HTTPClient.new
  client.set_auth(@redmine_domain, username, password)
  JSON.parse(client.get(@redmine_methods[:issues], paras).content)
end


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

def command_issues(message)
  id = message['from']['id']
  rm_username = @contex[id][:mail]
  rm_passowrd = @contex[id][:password]
  json = call_redmine(:issues, rm_username, rm_passowrd, {'assigned_to_id' => 'me'})
  return (json['issues'].map do |issue|
    render = ERB.new(@output_template)
    render.result(binding)
  end).join("\n")
end

def command_register(message)
  username = message['from']['id']
  mo = message['text'].split(/\s/)
  if mo
    mail = mo[1]
    password = mo[2]
    new_user username, mail, password
    return "User registered."
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
          'reply_to_message_id' => message['message_id'],
          'parse_mode' => 'Markdown'})
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
    # puts @contex if debug
  end
  process_q
  updates = call(:getUpdates,
                 {'offset' => @contex[:last_update_id] + 1})
  updates.each do | update|
    handle_update(update)
  end
  if updates.last
    @contex[:last_update_id] = updates.last['update_id']
  end
  File.write('contex.db', Marshal.dump(@contex))
  # puts @contex if debug
  sleep(10)
end


# puts Marshal.dump(ret)

