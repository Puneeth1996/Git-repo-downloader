require 'mechanize'

class BlogGrabber

  def initialize
    @mechanize = Mechanize.new
    @page = @mechanize.get('http://jyaasa.com/blogs/')
    @node = @page.search(".blog-list a")
    @this_months_link = []
  end

  def patrika_contents
    @node.each do |link|
      link_contents = Mechanize::Page::Link.new(link, @mechanize, @page)
      clicked_link = link_contents.click
      post_date_str = clicked_link.search(".blog-layout .right-sidebar h3").first.text
      @this_months_link.push(get_link_and_content(clicked_link, link)) if is_this_months_post?(post_date_str)
    end
    @this_months_link
  end

  def get_link_and_content(clicked_link, link)
    header =  clicked_link.search(".blog-layout .right-sidebar h2").first.text
    content = clicked_link.search(".blog-layout .right-sidebar p").first.text[0..125] + ".."
    link = link.attributes["href"].value = "http://jyaasa.com" + link.attributes["href"].value
    [header, link, content]
  end

  def is_this_months_post?(date_str)
    post_month = Date.parse(date_str).month
    post_month == Date.today.month - 1 ? true : false
  end
end
