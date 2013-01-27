{% extends "base.tpl" %}

{% block body %}

<button class="btn btn-success pull-right" type="button" onclick="document.location='/retry'">retry</button>
<h1>Failed files</h1>
<div class="row-fluid">
  <div class="span12">
	 {%for file in entries %}
		 {%if file != ".DS_Store" %}
		 {{file}}<br>
		 {% end %}
	 {% end %}
  </div>
</div>

{% end %}