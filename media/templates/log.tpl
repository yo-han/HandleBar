<h1>Logging</h1>
<button class="btn btn-danger pull-right" type="button" onclick="">clear</button>
<div class="row-fluid">
  <div class="span12">
	 %for line in outLog:
	 {{line}}<br>
	 %end
  </div>
</div>
%rebase base appName=appName