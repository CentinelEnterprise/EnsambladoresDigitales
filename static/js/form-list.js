$(document).ready(function(){
	$(".appframe-toolbar").find("a").each(function(){
		$(this).tooltip();
	});
	$("#eliminar-seleccionados").click(function(){
		$(this).closest('form').submit();
	});
	$(".refresh").click(function(){
		location.reload();
	});
	$(".select-all").click(function(){
		$("table tbody tr td input:checkbox").each(function(){
			console.log($(this));
			if($(this).prop('checked')) {
				$(this).prop('checked', false);
			}else{
				$(this).prop('checked', true);
			}
		});
	});
	$("#agregar_elemento").click(function(){
		$("#elementos").find(":selected").each(function(){
			if($(this).text().length != 0) {
				$("#elementos_seleccionados optgroup").append(new Option($(this).text(), $(this).attr("value")));
				$(this).remove();
			}
		});
	});	
	$("#agregar_todos").click(function(){
		$("#elementos").find("option").each(function(){
			if($(this).text().length != 0) {
				$("#elementos_seleccionados optgroup").append(new Option($(this).text(), $(this).attr("value")));
				$(this).remove();
			}
		});
	});	
	$("#quitar_elemento").click(function(){
		var opt = $("#elementos_seleccionados optgroup").find(":selected");
		if(opt.text().length != 0) {
			$("#elementos").append(new Option(opt.text(), opt.attr("value")));
			opt.remove();
		}
	});	
	$("#quitar_todos").click(function(){
		$("#elementos_seleccionados optgroup").find("option").each(function(){
			if($(this).text().length != 0) {
				$("#elementos").append(new Option($(this).text(), $(this).attr("value")));
				$(this).remove();
			}
		});
	});	
	$("form")[0].onsubmit = function() {
		$("#elementos_seleccionados optgroup").find("option").each(function(){
			if($(this).text().length != 0) {
				$(this).attr("selected","selected");
			}
		});
	}
});