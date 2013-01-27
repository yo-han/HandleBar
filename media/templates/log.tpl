{% extends "base.tpl" %}

{% block body %}

<button class="btn pull-right" type="button" onclick="document.location='/log?filter=off'">show debug</button>
<h1>Logging</h1>
<div class="row-fluid">
  <div class="span12">
	 {% for line in log %}
	 {{line}}<br>
	 {% end %}
  </div>
</div>

{% end %}