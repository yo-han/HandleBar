{% extends "base.tpl" %}

{% block body %}

<h1>Metadata</h1>
<div class="row-fluid">
  <div class="span8">
  	<form action="/metadata" method="post">
  		<input type="text" name="filename"> 
  		<input  type="submit" value="check">
  	</form>
  </div>
  <div class="span8">
  	{% if guessit %}
  	<h3>Guessit</h3>
  	<pre class="pretty-print code">{{guessit}}</pre>
  	{% end %}
  	{% if metadata %}
  	<h3>Metadata</h3>
  	<pre class="pretty-print code">{{metadata}}</pre>
  	{% end %}
  </div>
</div>

{% end %}