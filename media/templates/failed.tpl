<h1>Failed files</h1>
<button class="btn btn-success pull-right" type="button" onclick="document.location='/retry'">retry</button>
<div class="row-fluid">
  <div class="span12">
	 %for file in failedFiles:
		 %if file != ".DS_Store":
		 {{file}}<br>
		 %end
	 %end
  </div>
</div>
%rebase base appName=appName