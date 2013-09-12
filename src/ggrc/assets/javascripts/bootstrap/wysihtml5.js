!function($) {

  "use strict"; // jshint ;_;
	
	var createLink = wysihtml5.commands.createLink
		, old_exec = createLink.exec;
	createLink.exec = function(composer, command, value) {
		if (typeof(value) === "object")
			value.href = value.href.indexOf('//') > -1 ? value.href : 'http://' + value.href;
		else
			value = value.indexOf('//') > -1 ? value : 'http://' + value;
		return old_exec.call(this, composer, command, value);
	}

}(window.jQuery);
