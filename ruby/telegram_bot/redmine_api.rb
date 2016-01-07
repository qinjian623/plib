require 'rubygems'
require 'active_resource'


module Redmine
  class RedmineCollection < ActiveResource::Collection
    def initialize(parsed = {})
      @elements = parsed[self.class.name.demodulize.underscore]
      @total_count = parsed['total_count']
      @offset = parsed['offset']
      @limit = parsed['limit']
    end
  end

  class Redmine < ActiveResource::Base
    self.site = 'http://192.168.1.244:3000'
    self.include_root_in_json = true
  end

  class Projects < RedmineCollection
  end

  class Project < Redmine
    self.collection_parser = Projects
  end
  class TimeEntries < RedmineCollection
  end

  class TimeEntry < Redmine
    self.collection_parser = TimeEntries
  end

  class Issues < ActiveResource::Collection
    def initialize(parsed = {})
      @elements = parsed[self.class.name.demodulize.underscore]
      @total_count = parsed['total_count']
      @offset = parsed['offset']
      @limit = parsed['limit']
    end
  end

  class Issue < ActiveResource::Base
    self.site = 'http://192.168.1.244:3000'
    self.user = ARGV[0]
    self.password = ARGV[1]
    self.collection_parser = Issues
    self.include_root_in_json = true
  end

  def self.list_issues(user, pass, id = :all)
    Issue.user = user
    Issue.password = pass
    return Issue.find(id, :params => {:assigned_to_id => 'me'})
  end

  def self.list_projects(user, name, id = :all)
    Project.user = user
    Project.password = name
    return Project.find(id)
  end

  def self.append_time(user, name, issue_id, hours, comments, activity_id)
    TimeEntry.new(
      :issues_id => issue_id,
      :hours => hours,
      :comments => comments,
      :activity_id => activity_id
    )
  end

  def self.list_activity(user, name)
    ret = {}
    TimeEntry.user = user
    TimeEntry.password = name
    res = TimeEntry.find(:all)
    res.each do|en|
      begin
        ret[en.activity.id] = en.activity.name
      rescue
      end
    end
    return ret
  end
  
  # TimeEntry.user = ARGV[0]
  # TimeEntry.password = ARGV[1]
  # res = TimeEntry.find(:all)
  # res.each do|en|
  # begin
  #   puts en.activity.name, en.activity.id
  # rescue
  #   puts "..."
  # end
  # end
end




# # exit
# te = TimeEntry.new(
#   :issue_id => 184,
#   :hours => 1.881238373,
#   :comments => "test",
#   :activity_id => 14
# )
# if te.save
#   puts te.id
# else
#   puts te.errors.full_messages
# end

# # Retrieving issues
# res = Issue.find(:all,  :params => { :assigned_to_id => "me"})
# res = Project.find(:all,  :params => { :assigned_to_id => "me"})
# res.each do | project|
#   # puts project.name, project.id
# end

# # Retrieving an issue
# # issue = Issue.find(:all, :params => { :assigned_to_id => "me"}).first
# # puts issue.subject
# # puts issue.description
# # puts issue.author.name
# # puts issue.assigned_to.name
# i = Issue.find(184)
# i.status_id = 2
# i.save
# exit
# # Creating an issue
# issue = Issue.new(
#   :subject => 'REST API test',
#   :assigned_to_id => 'me',
#   :project_id => 99,
#   :description => 'ass'
# )

# # issue.custom_field_values = {'2' => 'Fixed'}
# if issue.save
#   puts issue.id
# else
#   puts issue.errors.full_messages
# end

# exit
# # issue = Project.new(
# #   :name => "REST API test",
# #   :identifier => "ttt",
# #   :parent_id => 81
# # )
# # proj = Project.find(:one, {:name => 'REST API test'})


# # Updating an issue
# issue = Issue.find(1)
# issue.subject = 'REST API'
# issue.save

# # Deleting an issue
# issue = Issue.find(1)
# issue.destroy

