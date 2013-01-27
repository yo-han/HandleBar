
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{{ escape(handler.settings["page_title"]) }}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <!-- Le styles -->
    <link href="{{ static_url("css/bootstrap.css") }}" rel="stylesheet">
    <style>
      body {
        padding-top: 60px; /* 60px to make the container go all the way to the bottom of the topbar */
      }
    </style>
    <link href="{{ static_url("css/bootstrap-responsive.css") }}" rel="stylesheet">

    <!-- HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->

    <!-- Fav and touch icons -->
    <link rel="apple-touch-icon-precomposed" sizes="144x144" href="/media/ico/apple-touch-icon-144-precomposed.png">
    <link rel="apple-touch-icon-precomposed" sizes="114x114" href="/media/ico/apple-touch-icon-114-precomposed.png">
      <link rel="apple-touch-icon-precomposed" sizes="72x72" href="/media/ico/apple-touch-icon-72-precomposed.png">
                    <link rel="apple-touch-icon-precomposed" href="/media/ico/apple-touch-icon-57-precomposed.png">
                                   <link rel="shortcut icon" href="/media/ico/favicon.png">
  </head>

  <body>

    <div class="navbar navbar-inverse navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container">
          <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </a>
          <a class="brand" href="#">{{ escape(handler.settings["page_title"]) }}</a>
          <div class="nav-collapse collapse">
            <ul class="nav">
              <li {% if tabActive == 'home' %}class="active"{% end %}><a href="/">Home</a></li>
              <li {% if tabActive == 'log' %}class="active"{% end %}><a href="/log">Logging</a></li>
              <li {% if tabActive == 'failed' %}class="active"{% end %}><a href="/failed">Failed</a></li>
            </ul>
          </div><!--/.nav-collapse -->
          <div class="nav-collapse collapse pull-right">
            <ul class="nav">
              <li id="hb-status"><a>-</a></li>
            </ul>
          </div><!--/.nav-collapse -->
        </div>
      </div>
    </div>

    <div class="container">
	   
	   {% block body %}{% end %}

    </div> <!-- /container -->

    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="{{ static_url("js/jquery.js") }}"></script>
    <script src="{{ static_url("js/bootstrap.min.js") }}"></script>
    <script type="text/javascript">
       
       function getProgress() {
       		$.get('/progress', function(r) {
            	
            	if(r != 'none')
            		$('#hb-status a').html(r);
            	else
            		$('#hb-status a').html('nothing is converting');
             });
       }
          	
       $(function(){
	       getProgress();
	       //setInterval('getProgress()',1000);
       });        	
       </script>
  </body>
</html>