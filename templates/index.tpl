!!! 5
html(lang="en")
  head
    script( src="http://github.com/janl/mustache.js/raw/master/mustache.js")
    script( src="http://code.jquery.com/jquery-1.7.1.min.js")
    title= title
  body
    script
      $.getJSON('/dir/flatiron', function(data) {

        var template = "Files: <ul> {{#data.files}}<li>{{.}}</li>{{/data.files}} </ul>";
        var html = Mustache.to_html(template, data);
        document.write(html);

      });

    h1= title
    if title
      p You are amazing
    else
      p Get on it!

