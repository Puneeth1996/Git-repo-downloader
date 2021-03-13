require 'httparty'
require File.join(File.dirname(__FILE__),'configurations.rb')

class Announcement
  attr_accessor :key, :secret, :token, :list_id

  def initialize
    @key = CONFIG['trello_key']
    @secret = CONFIG['trello_secret']
    @token = CONFIG['trello_token']
    @list_id = CONFIG['trello_list']
  end

  def patrika_contents
    begin
      list = HTTParty.get("https://api.trello.com/1/lists/#{@list_id}?fields=name&cards=open&key=#{@key}&token=#{@token}")
      cards = list['cards']
      result = Array.new
      cards.each do |card|
        if Date.parse( card['dateLastActivity']).month == (Time.now.month.to_i - 1)
          result << prepare_result(card)
        end
      end
    rescue Exception => e
    end
    return result
  end

  private
  def prepare_result(card)
    name = card['name']
    desc = card['desc']
    return [name, "", desc]
  end

  # Method to move published card from ready to publish to published list. This is not working now.
  def move_card(card)
    id = card['id']
    HTTParty.put("https://api.trello.com/1/cards/#{id}/55fe79ff6286c04f8ee97091&key=#{@key}&token=#{@token}")
  end
end

