require File.join(File.dirname(__FILE__),'lib/configurations.rb')
class Deployer
  def deploy
    source = File.expand_path('./')
    server = CONFIG['server']
    remote_path = CONFIG['remote_path']
    response = `rsync -avuz --progress #{source}/ #{server}:#{remote_path}`
    puts response
  end

  def sync
    
  end
end

d = Deployer.new
d.deploy