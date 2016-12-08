var i = 1;
        $("#input_add").click(function() {
            $("tbody tr:first").clone().find(".data_input").each(function() {
                if ($(this).attr('class')== 'tr_clone_add btn data_input'){
                    $(this).attr({
                        'id': function(_, id) { return "remove_button" },
                        'name': function(_, name) { return "name_remove" +i },
                        'value': 'Remove'
                    }).on("click", function(){
                        var a = $(this).parent();
                        var b= a.parent();
                        i=i-1
                        $('#id_form-TOTAL_FORMS').val(i);
                        b.remove();

                        $('.product-instances tr').each(function(index, value){
                            $(this).find('.data_input').each(function(){
                                $(this).attr({
                                    'id': function (_, id) {
                                        var idData= id;
                                        var splitV= String(idData).split('-');
                                        var fData= splitV[0];
                                        var tData= splitV[2];
                                        return fData+ "-" +index + "-" + tData
                                    },
                                    'name': function (_, name) {
                                        var nameData= name;
                                        var splitV= String(nameData).split('-');
                                        var fData= splitV[0];
                                        var tData= splitV[2];
                                        return fData+ "-" +index + "-" + tData
                                    }
                                });
                            })
                        })
                    })
                }
                else{
                    $(this).attr({
                        'id': function (_, id) {
                            var idData= id;
                            var splitV= String(idData).split('-');
                            var fData= splitV[0];
                            var tData= splitV[2];
                            return fData+ "-" +i + "-" + tData
                        },
                        'name': function (_, name) {
                            var nameData= name;
                            var splitV= String(nameData).split('-');
                            var fData= splitV[0];
                            var tData= splitV[2];
                            return fData+ "-" +i + "-" + tData
                        }
                    });

                }
            }).end().appendTo("tbody");
            $('#id_form-TOTAL_FORMS').val(1+i);
            i++;

        });