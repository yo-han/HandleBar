<h1>HandleBar convert history and status</h1>
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
		%for row in list:
		<tr>
			<td style="width:20px;">{{row['fileId']}}</td>
			<td style="width:20px;">{{row['type']}}</td>
			<td style="width:70px;">
				%if row['image']:
				<img src="/media/images/{{row['image']}}" style="height:50px;">
				%end
			</td>	
			<td>
				{{row['title']}}
				%if row['type'] == "episode":
				- {{row['episodeName']}}<br>
				<span class="muted">Season {{row['season']}} Episode{{row['episode']}}</span>
				%else: 
				<a href="http://www.imdb.com/title/{{row['imdbId']}}/" target="_blank"><img src="/media/img/imdb.png"></a>
				%end				
			</td>
			<td>
				{{row['name']}}
			</td>			
			<td></td>
		</tr>	
		%end
	</tbody>
</table>

%rebase base appName=appName