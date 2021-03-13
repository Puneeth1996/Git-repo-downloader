require 'httparty'
require File.join(File.dirname(__FILE__),'formatters','knowledge_formatter.rb')
require File.join(File.dirname(__FILE__),'configurations.rb')

class KnowledgeNinja
  attr_accessor :knowledge
  def initialize
    @token = CONFIG['slack_authorization_token']
    @base_uri = "https://slack.com/api/channels.history"
    @channel = CONFIG['slack_knowledge_sharing_channel']
    @knowledge = []
  end

  def fetch_knowledge
    today_date = Date.today.prev_month
    start_time = Date.parse "#{today_date.year}-#{today_date.month}-01"
    start_time = start_time.to_time.to_i
    slack_contents = HTTParty.get("#{@base_uri}?token=#{@token}&channel=#{@channel}&inclusive=1&pretty=1&oldest=#{start_time}").body
    json_contents = JSON.parse(slack_contents)
    @knowledge= json_contents['messages']
  end

  def filter_knowledge
    @knowledge.keep_if{|k| k['text'].include?('http')}
    @knowledge.delete_if {|k| k['subtype'] && k['subtype']=="bot_add"} 
  end

  def prepare_for_patrika
    @knowledge.collect! {|k| 
      formatter = KnowledgeFormatter.new(k)
      formatter.format
    }
  end

  def patrika_contents
    self.fetch_knowledge
    self.filter_knowledge
    self.prepare_for_patrika
  end

end 
