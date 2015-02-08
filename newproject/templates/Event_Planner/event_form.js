	<script type="text/javascript" src="{{ STATIC_URL }}jquery.form.js"></script>
	<script>
	var dialog_instance;

	function setup_accordion_headers() {
		var elems = $('input[name$="-title"]');
		var arr = new Array()
		elems.each(function(i){
			arr[i] = $(this).val()
		});
		$('h3').each(function(i) {
			$(this).find('.segment-header').text(arr[i]);
		});
	}	
	function segment_modified(event) {
		seg = $(this).closest('.sortables');
		seg.find('.segment-modified').text("*");
		setup_accordion_headers();
	}	
	function setup_accordion() {
		$( "#accordion h3" ).click(function( event ) {
			if ( stop ) {
				event.stopImmediatePropagation();
				event.preventDefault();
				stop = false;
			}
		});	
		$( "#accordion" ).accordion({
			autoHeight:false,
			forcePlaceholderSize:true,
			forceHelperSize:true,
			navigation:true,
			collapsible:true,
			header: "> div > h3"
		})
			.sortable({
				axis: "y",
				handle: "h3",
				stop: function(event, ui) {
					setTimeout('$("body").css("sortables","ui-accordion-header")', 2000);
					stop = true;
					var data = [];
					$('input[name$="order"]').each(function(i) {
						$(this).val(i+1);
					});
					$('div[id^="sortable_"]').each(function(i) {
						data[i] = $(this).attr("id");
					});
					
					var jqxhr = $.post("{% url 'event_order_update_view' event.id %}", JSON.stringify({'array': data}) , function(data) {
						$("#ajax").text("order saved.").show().delay(5000).fadeOut();
						//alert(data);
					}).error(function() { alert("error") });
					if (($.browser.msie) && ($.browser.version >=6.0))
						$('#accordion *').focus().blur();
					},
				cancel: "div[id^='sortable']:has(div.ui-accordion-content-active)"
		});
		
		////// hide form fields that are handled automatically via javascript
		$('input[name$="order"]').hide();
		$('label[for$="order"]').hide();
		$('select[name$="-song"]').hide();
		$('label[for$="-song"]').hide();
		$('select[name$="-event"]').hide();
		$('label[for$="-event"]').hide();
		
		////// set up accordion header names
		setup_accordion_headers();
		$('#accordion').find(":input").change(segment_modified);
	}
	
	function reset_accordion() {
		$('#accordion').accordion('destroy').sortable('destroy');
		setup_accordion();
	}

	function setup_activity_dialog_autocomplete() {


		$('#id_participant_name').autocomplete({
			minLength: 0,
			source: "{% url 'json_participant_list_view' %}"
		});
		$('#id_role_name').autocomplete({
			minLength: 0,
			source: "{% url 'json_role_list_view' %}"
		});
	}	
	var activity_button;
	var delete_button;
	function setup_activity_delete_button() {
		$( '.activity_delete_link' ).button('destroy').button({
				icons: {
					primary: "ui-icon-trash"
				},
				text:false
			}).click(function(event) {
			delete_button = $(this);

			$( "#dialog-confirm" ).dialog({
				resizable: false,
				height:219,
				width: 350,
				modal: true,
				autoOpen: false,
				buttons: {
					"Delete": function() {
						delete_button.closest('li').addClass('mark_for_delete');
						var jqxhr = $.post(delete_button.attr('ajax_url'), [{}] , function() {
							$("#ajax").text("item deleted.").show().delay(5000).fadeOut();
						
							$(".mark_for_delete").remove();
						})
						.error(function() { 
							alert("error");
							$('.mark_for_delete').removeClass('mark_for_delete');
					 	});
			
						$( this ).dialog( "close" );
					},
					Cancel: function() {
						$( this ).dialog( "close" );
					}
				}
			});

			$('#dialog-confirm').dialog("open");
			event.stopImmediatePropagation();
			event.preventDefault();
			return false;
		});
	}


	function setup_segment_links() {
		$( '.segment_button' ).button('destroy').button();
		$( '.segment_form').submit(function(e) {
			e.preventDefault(); // <-- important
			e.stopImmediatePropagation();
			this_url = $(this).attr('ajax_url');
			$(this).ajaxSubmit({
		   	 //target: '#id_song_list',
		   	 context: $(this).closest('.sortables'),
		
	  	  		 success: function(){
	  	  		 	$(this).find('.segment-modified').text("");
	  	  	 	},
	       	url: this_url,
	       	dataType: 'json'
			});
		});		
		$( '.delete_link' ).button('destroy').button().click(function(event) {
			delete_button = $(this);

			$( "#dialog-confirm" ).dialog({
				resizable: false,
				height:219,
				width: 350,
				modal: true,
				autoOpen: false,
				buttons: {
					"Delete": function() {
						delete_button.closest('div.sortables').addClass('mark_for_delete');
						var jqxhr = $.post(delete_button.attr('ajax_url'), [{}] , function() {
							$("#ajax").text("item deleted.").show().delay(5000).fadeOut();
						
							$(".mark_for_delete").remove();
							reset_accordion()
						})
						.error(function() { 
							alert("error");
							$('.mark_for_delete').removeClass('mark_for_delete');
					 	});
			
						$( this ).dialog( "close" );
					},
					Cancel: function() {
						$( this ).dialog( "close" );
					}
				}
			});

			$('#dialog-confirm').dialog("open");
			event.stopImmediatePropagation();
			event.preventDefault();
			return false;
		});
		setup_activity_delete_button();
		$('.edit_link').hide();


		//setup activity dialog			
		$( "#dialog-add-activity" ).dialog("destroy").dialog({
			resizable: true,
			width: 640,
			modal: true,
			autoOpen: false,
			buttons: {

				"Add Activity": function() {
					$('#activity_form').ajaxSubmit({
						success: function(data) {
							if (data.data)
							{
								$('#dialog-add-activity-form').html(data.data);
								setup_activity_dialog_autocomplete();
							}
							else
								activity_button.closest(".segment-activity-buttons").siblings(".activity_div").html(data.activities);
								setup_activity_delete_button();
								$('#dialog-add-activity').dialog("close");
						},
						url: activity_button.attr("ajax_url")	
					});
				},
				Cancel: function() {
					$( this ).dialog( "close" );
				}

			}
		});	
		
		$('.add_activity_link').button().click(function(event) {
			activity_button=$(this);
			$.get(activity_button.attr('ajax_url'), function(data) {
				$('#dialog-add-activity-form').html(data.data);
				setup_activity_dialog_autocomplete();
			});
			$('#dialog-add-activity').dialog("open");
			event.stopImmediatePropagation();
			event.preventDefault();
			return false;
		});
		
		
		
		$('button[id^="edit_song_seg_"]').button().click(function(event) {
			
			$.get('{% url 'song_list_view' %}?xhr&options=A&page_size=5', build_dialog);
			dialog_instance=$(this).attr("instance");
			event.stopImmediatePropagation();
			event.preventDefault();
			return false;
		});	
		
	}	
	function add_segment_callback(data) {
		//alert(data.html);
		//$('#accordion').accordion('destroy').sortable('destroy');
		$('#accordion').append(data.html);
		reset_accordion();
		setup_segment_links();
	}
	
	function build_dialog(data) {
		var song_list = JSON.parse(data.songs_json);
		var newhtml="<table>";
		$.each(song_list, function(index, song) {
			newhtml+="<tr><th>"
					+"<a target=\"_blank\" href=\"" + song.extras.get_absolute_url + "\">"
					+song.fields.title+"</a></th>"
					+"<td>";
			$.each(song.fields.composers, function(j, composer) {
				if (j>0) newhtml+="<br/>";
				newhtml+=composer.extras.__unicode__;
			});
			newhtml+="</td>"
					 +"<td><button class=\"song_select\" song=\"" + song.pk + "\">select</button></td>"
					 +"</tr>";
		});
		newhtml+="</table>";
		newhtml+="<div class=\"pagination\">"
			+"<span class=\"step-links\">";
		page = data.page;
	
		if (page.has_previous){
			newhtml+="<a class=\"song_dialog\" id=\"id_prev\" href=\""
					 + data.search_url
					 +"?page_size="
					 +page.page_size
					 +"&page="
					 +page.previous_page_number;
			if (data.search)
				newhtml+="&search="
					 +data.search;
			if (data.option)
				newhtml+="&options="
					 +data.option;								 
			newhtml+="\">previous</a>";
		}
		newhtml+="<span class=\"current\">"
				+"Page "
				+ page.number 
				+" of "
				+ page.num_pages
				+".</span>";
		if (page.has_next){
			newhtml+="<a class=\"song_dialog\" id=\"id_next\" href=\""
					 + data.search_url
					 +"?page_size="
					 +page.page_size
					 +"&page="
					 +page.next_page_number;
			if (data.search)
				newhtml+="&search="
					 +data.search;
			if (data.option)
				newhtml+="&options="
					 +data.option;							 
			newhtml+="\">next</a>";
		}
		$('#songs').html(newhtml);	
		$('.song_dialog').click(function() {
			$.get($(this).attr("href"), build_dialog);
			return false;
		});		
		if(! $("#edit_song_dialog").dialog("isOpen"))							
		$("#edit_song_dialog").dialog("open");
		$(".song_select").button().click(function() {
				//alert($(this).attr("song"));
				song_id = $(this).attr("song");
				select_name = "segment-"+dialog_instance+"-song";
				//alert(select_name);
				//alert($('select[name="'+select_name+'"]').val());//find('option[value="'+song_id+'"]').select());
				$('select[name="'+select_name+'"]').val(song_id).change();
				//alert($('select[name="'+select_name+'"]').val());
				//val($(this).attr("song"));
				//alert($(this).parent().siblings('th').html());
				//segment-{{ f.instance.id }}-song-url
				select_name = "segment-"+dialog_instance+"-song-url";
				$('#'+select_name).html($(this).parent().siblings('th').html());
				$("#edit_song_dialog").dialog("close");
		});

	}
	
	$(function() {
		$("#edit_song_dialog").dialog({
			modal:true,
			autoOpen:false,
			width: 640
		});
	
		

		
		var stop = false;
	
		setup_accordion();
		$("#id_date_0").datepicker();

	});


	var wait = false;
	var queued_submit = false;
	function autosubmit(eventObject) {
		var TIMEOUT = 2000;
		
		var options = {
		    success: build_dialog,
		    url: '{% url 'song_list_view' %}?xhr&page_size=5',
		    dataType: 'json'
		}
		if (!wait) {
			wait=true;
			$( '#search_form' ).ajaxSubmit(options);
			window.setTimeout(function() {
				wait = false;
				if (queued_submit) {
					queued_submit=false;
					$( '#search_form' ).ajaxSubmit(options);		
				}
			}, TIMEOUT);
		}
		else 
			queued_submit=true;
	}
	
	
	$( document ).ready( function() {
		$('#accordion').sortable("option", "cancel", "div[id^='sortable']:has(div.ui-accordion-content-active)");
		var options = {
		    //target: '#id_song_list',
	  	  	 success: build_dialog,
	       url: '{% url 'song_list_view' %}?xhr&page_size=5',
	       dataType: 'json'
		}
	
		$( '#search_form' ).bind('submit', function(e) {
			e.preventDefault(); // <-- important
			$(this).ajaxSubmit(options);
		});

		$( '#id_search' ).keyup(autosubmit);
		$( '#id_options' ).change(autosubmit);
		{% if event %}
		$( '#add_segment' ).click(function() {
			$.get('{% url 'segment_create_view' event.id %}', add_segment_callback)
			.error(function(data) { alert("error"); 
					 });
			return false;
		});
		$( '#add_songsegment' ).click(function() {
			$.get('{% url 'songsegment_create_view' event.id %}', add_segment_callback)
			.error(function(data) { alert("error"); 
					 });
			return false;
		});
		{% endif %}
		setup_segment_links()
		$("#ajax").ajaxError(function(event, request, settings){
  			$(this).append("<li>Error requesting page " + settings.url + "</li>");
  			$(this).append(request.responseXML);
		});
	});
	
	$(document).ajaxSend(function(event, xhr, settings) {
	    function getCookie(name) {
	        var cookieValue = null;
	        if (document.cookie && document.cookie != '') {
	            var cookies = document.cookie.split(';');
	            for (var i = 0; i < cookies.length; i++) {
	                var cookie = jQuery.trim(cookies[i]);
	                // Does this cookie string begin with the name we want?
	                if (cookie.substring(0, name.length + 1) == (name + '=')) {
	                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                    break;
	                }
	            }
	        }
	        return cookieValue;
	    }
	    function sameOrigin(url) {
	        // url could be relative or scheme relative or absolute
	        var host = document.location.host; // host + port
	        var protocol = document.location.protocol;
	        var sr_origin = '//' + host;
	        var origin = protocol + sr_origin;
	        // Allow absolute or scheme relative URLs to same origin
	        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
	            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
	            // or any other URL that isn't scheme relative or absolute i.e relative.
	            !(/^(\/\/|http:|https:).*/.test(url));
	    }
	    function safeMethod(method) {
	        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	    }
	
	    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
	        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
	    }
	});
	</script>

