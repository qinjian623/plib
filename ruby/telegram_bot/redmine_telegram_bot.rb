require 'erb'
require 'telegram_bot'
require './redmine_api'

def new_user (username, mail, password)
  @contex[username] = {}
  @contex[username][:mail] = mail
  @contex[username][:password] = password
end

def command_register(message)
  username = message.from.id
  mo = message.text.split(/\s/)
  if mo
    mail = mo[1]
    password = mo[2]
    new_user username, mail, password
    return "User registered."
  else
    return "Wrong command format."
  end
end

def command_greet(message)
  return "Hello, #{message.from.first_name}!"
end


@output_template = "#<%= issue.id %> *<%= issue.subject %>* <% if not issue.description.empty? %> _<%= issue.description%>_ <% end %>"

def command_issues(message)
  id = message.from.id
  rm_username = @contex[id][:mail]
  rm_passowrd = @contex[id][:password]
  issues = Redmine.list_issues(rm_username, rm_passowrd)
  return (issues.map do |issue|
    render = ERB.new(@output_template)
    render.result(binding)
          end).join("\n")
end

@projects_template = "#<%= project.id %> *<%= project.name %>* "
def command_projects(message)
  id = message.from.id
  rm_username = @contex[id][:mail]
  rm_passowrd = @contex[id][:password]
  projects = Redmine.list_projects(rm_username, rm_passowrd)
  return (projects.map do |project|
            render = ERB.new(@projects_template)
            render.result(binding)
          end).join("\n")
end

def command_use_project(message)
  id = message.from.id
  rm_username = @contex[id][:mail]
  rm_passowrd = @contex[id][:password]
  project_id = message.text.split(/\s/)[1].to_i
  project = Redmine.list_projects(rm_username, rm_passowrd, project_id)
  @contex[id][:current_project_] = project.id
  return "Current project: " + project.name
end

def command_use_issue(message)
  id = message.from.id
  rm_username = @contex[id][:mail]
  rm_passowrd = @contex[id][:password]
  issue_id = message.text.split(/\s/)[1].to_i
  issue = Redmine.list_issues(rm_username, rm_passowrd, issue_id)
  @contex[id][:current_issue_] = issue.id
  return "Current issue: " + issue.subject
end

def command_current_project(message)
  id = message.from.id
  rm_username = @contex[id][:mail]
  rm_passowrd = @contex[id][:password]
  if @contex[id].key?:current_project_
    project_id = @contex[id][:current_project_]
    project = Redmine.list_projects(rm_username, rm_passowrd, project_id)
    return "Current project: " + project.name
  else
    return "Current project is not set yet."
  end
end

def command_current_issue(message)
  id = message.from.id
  rm_username = @contex[id][:mail]
  rm_passowrd = @contex[id][:password]
  if @contex[id].key?:current_issue_
    issue_id = @contex[id][:current_issue_]
    issue = Redmine.list_issues(rm_username, rm_passowrd, issue_id)
    return "Current issue: " + issue.subject
  else
    return "Current issue is not set yet."
  end
end

def command_start(message)
  username = message.from.id
  @contex[username] = {}
  @contex[username][:latest_chat_it] = message['chat']['id']
  return "User storage space created."
end

def command_log_on(message)
  user = message.from.id
  if @contex[user].key? :log_begin
    return "It's logging now from " + @contex[user][:log_begin]
  else
    @contex[user][:log_begin] = Time.now
  end
end

def command_log_off(message)
  user = message.from.id
  if @contex[user].key? :log_begin
    @contex[user][:log_time] = Time.now - @contex[user][:log_begin]
    @contex[user].delete :log_begin
    return "Log off: " + @contex[user][:log_time]/3600.to_s + " hours"
  else
    @contex[user][:log_begin] = Time.now
  end
end

def command_add_log(message)
  id = message.from.id
  rm_username = @contex[id][:mail]
  rm_passowrd = @contex[id][:password]
  if not @contex[id].key? :current_issue_
    return "Current issue is not set yet."
  end
  current_issue = @contex[id][:current_issue_]
  segs = message.text.split(/\s/)
  if segs.length > 2
    return "Command format error"
  end
  comments = ""
  if segs.length == 2
    comments = segs.last
  end

  user = id
  if @contex[user].key? :log_time
    if @contex[user].key? :current_activity
      Redmine.append_time(rm_username, rm_passowrd,
                  current_issue, @contex[user][:log_time], comments,
                  @contex[user][:current_activity])
    else
      return "Please set activity with command user_activity \n" +
             command_list_activity(message)
    end
  else
    return "No log time now. Log on then log off to get the log time."
  end
end

def command_list_activity(message)
  id = message.from.id
  rm_username = @contex[id][:mail]
  rm_passowrd = @contex[id][:password]
  h = Redmine.list_activity(rm_username, rm_passowrd)
  return (h.map do |key, value|
    "#" + key.to_s + " *" + value + "* "
  end).join("\n")
end

def command_use_activity(message)
  id = message.from.id
  rm_username = @contex[id][:mail]
  rm_passowrd = @contex[id][:password]
  activity_id = message.text.split(/\s/)[1].to_i
  h = Redmine.list_activity(rm_username, rm_passowrd)
  if h.key? activity_id
    @contex[id][:current_activity] = activity_id
  else
    return "Activity ID not found."
  end
end



def dispatch(command, message)
  begin
    command_func = ('command_' + command).to_sym
    if private_methods.include? command_func
      return send 'command_'+command, message
    else
      return "Command not found."
    end
  rescue Exception => e
    puts e.message  
    puts e.backtrace.inspect
    return e.message
  end
end

@contex = {
  :Q => [],
  :last_update_id => -1
}

def load_contex()
  if File.exists? 'contex.db'
    puts "Reading db..."
    @contex = Marshal.load(File.read('contex.db'))
    # puts @contex if debug
  end
end

def save_contex()
  File.write('contex.db', Marshal.dump(@contex))
end

bot = TelegramBot.new(token:  ARGV[0])
bot.get_updates(fail_silently: true) do |message|
  load_contex
  puts "@#{message.from.username}: #{message.text}"
  command = (/\/(\w*)/ .match message.text)[1]
  message.reply do |reply|
    reply.text = dispatch(command, message)
    puts "sending #{reply.text.inspect} to @#{message.from.username}"
    response = reply.send_with(bot)
    puts response.text
  end
  save_contex
end
