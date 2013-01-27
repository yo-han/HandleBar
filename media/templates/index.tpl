{% extends "base.tpl" %}

{% block body %}

<h1>HandleBar convert history and status</h1>
<button class="btn btn-danger pull-right" type="button" onclick="document.location='/clear?c=imsure'">clear</button>
<table class="table table-striped">
	<thead>
		<tr>
			<th>#</th>
			<th>Type</th>			
			<th>Artwork</th>
			<th>Title</th>	
			<th>Filename</th>
		</tr>
	</thead>
	<tbody>
		{% for row in entries %}
			 {{ modules.File(row) }}
		{% end %}
	</tbody>
</table>
{% end %}