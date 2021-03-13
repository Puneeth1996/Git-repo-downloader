require "blog_grabber"
require "knowledge_ninja"
require "announcement"
require "liquid"

class EmailTemplate
  def initialize
    @template_content = File.open("./patrika_template.html.liquid")
    @newsletter_contents = [] 
    [BlogGrabber, KnowledgeNinja, Announcement].each {|klass| @newsletter_contents += klass.new.patrika_contents}
  end

  def get_email_contents(month, email)
    content = Liquid::Template.parse(@template_content.read).render('email'=>email, 'month'=>month, 'posts'=>@newsletter_contents)
  end
end