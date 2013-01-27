<tr>
	<td style="width:20px;">{{entry['fileId']}}</td>
	<td style="width:20px;">{{entry['type']}}</td>
	<td style="width:70px;">
		{%if entry['image'] %}
		<img src="{{ static_url("images") }}/{{entry['image']}}" style="height:50px;">
		{% end %}
	</td>	
	<td>
		{{entry['title']}}
		{% if entry['type'] == "episode" %}
		- {{entry['episodeName']}}<br>
		<span class="muted">Season {{entry['season']}} Episode{{entry['episode']}}</span>
		{% else %} 
		<a href="http://www.imdb.com/title/{{entry['imdbId']}}/" target="_blank"><img src="{{ static_url("img") }}/imdb.png"></a>
		{% end %}				
	</td>
	<td>
		{{entry['name']}}
	</td>			
	<td></td>
</tr>	