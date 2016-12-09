/*
 *  CRM 100credit
 */

function bootstrapAlert(content, type){
    return '<div class="alert alert-'+(type || "danger")+' alert-dismissable" role="alert">'+content+'</div>' +
           '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>';
}

function emailCheck(string){
    var pattern = /^([\.a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+/;
    return pattern.test(string);
}

function getChecked(name){
    var arr = [];
    $('input[name="'+name+'"]:checked').each(function(){
        arr.push($(this).val());
    });
    return arr.join(',');
}

function getCheckedArray(name){
    var arr = [];
    $('input[name="'+name+'"]:checked').each(function(){
        arr.push($(this).val());
    });
    return arr;
}

// 返回上一页并刷新
function backpage(){
    location.href = document.referrer;
}

function backtopage(){
    history.go(-1);
}

// 打开新页面
function openNewWindow(url){
    window.open(url);
}

// 筛选器效果
function filterEffect(){
    $(this).addClass("selected").siblings().removeClass("selected");
}

function checkSelectVal(jq){
    if (jq.children("option").length > 1){
        return !(jq.val() === "0");
    } else {
        return true;
    }
}

function loading(flag){
    var oLoading = $('#loading');
    if (oLoading){
        if(flag){
            oLoading.css('display', 'block');
        }else{
            oLoading.css('display', 'none');
        }
    }
}

/*
 *  客户方面的操作
 */

function checkCustomerForm(){
    var type = $('#type');
    if (!(checkSelectVal(type))) {
        type.parent().addClass("has-error");
        alert("请选择客户类型！");
        return false;
    }
    var category1 = $('#category1');
    if (!(checkSelectVal(category1))) {
        category1.parent().addClass("has-error");
        alert("请选择客户客户一级类目！");
        return false;
    }
    var category2 = $('#category2');
    if (!(checkSelectVal(category2))) {
        category2.parent().addClass("has-error");
        alert("请选择客户客户二级类目！");
        return false;
    }
    var category3 = $('#category3');
    if (!(checkSelectVal(category3))) {
        category3.parent().addClass("has-error");
        alert("请选择客户客户三级类目！");
        return false;
    }
    var zone = $("#zone");
    if (zone.is("select")){
        if (zone.val() === "0") {
            zone.parent().addClass("has-error");
            alert("请选择大区！");
            return false;
        }
    }
    var province = $("#province");
    if (!(checkSelectVal(province))) {
        province.parent().addClass("has-error");
        alert("请选择省份！");
        return false;
    }
    return true;
}

function getCustomerData(){
    return {
        name: $("#name").val(),
        short_name: $("#short-name").val(),
        type: $("#type").val(),
        priority: $("#priority").val(),
        category1: $('#category1').val(),
        category2: $('#category2').val(),
        category3: $('#category3').val(),
        zone: $("#zone").val(),
        registered_capital: $("#registered-capital").val(),
        shareholder: $("#shareholder").val(),
        product_desc: $("#product-desc").val(),
        province: $("#province").val(),
        city: $("#city").val(),
        address: $("#address").val(),
        notes: $("#notes").val(),
        businessmans_id: getCheckedArray("businessman")
    };
}

function checkCustomerData(args){
    if (!args['name']){
        $("#name").parent().addClass("has-error");
        alert('客户名称为必填项');
        return false;
    } else if (!args['short_name']){
        $("#short-name").parent().addClass("has-error");
        alert('简称为必填项');
        return false;
    } else if (!$.trim(args['registered_capital'])){
        $("#registered-capital").parent().addClass("has-error");
        alert('注册资本为必填项');
        return false;
    } else if (!args['shareholder']){
        $("#short-name").parent().addClass("has-error");
        alert('股东为必填项');
        return false;
    } else if (!args['product_desc']){
        $("#product-desc").parent().addClass("has-error");
        alert('客户业务或产品描述为必填项');
        return false;
    } else if (!args['city']){
        $("#city").parent().addClass("has-error");
        alert('城市为必填项');
        return false;
    } else if (!$.isNumeric(args['registered_capital'])){
        $("#registered-capital").parent().addClass("has-error");
        alert('注册资本不是一个有效的数字');
        return false;
    } else {
        return true;
    }
}

function customerAdd(){
    $("form").find("div.has-error").removeClass("has-error");
    var args = getCustomerData();
    if (checkCustomerData(args)){
        if (checkCustomerForm()){
            var url = '/crm/ajax/customer/add/';
            $.post(url, JSON.stringify(args), function(result){
                if (result['msg']=='0') {
                    backpage();
                } else {
                    alert(result['msg']);
                }
            });
        }
    }
}

function customerEdit(customerId){
    $("form").find("div.has-error").removeClass("has-error");
    var args = getCustomerData();
    args['id'] = customerId;
    if (checkCustomerData(args)){
        if (checkCustomerForm()){
            var url = '/crm/ajax/customer/edit/';
            $.post(url, JSON.stringify(args), function(result){
                if (result['msg'] == '0'){
                    backpage();
                } else {
                    alert(result['msg']);
                }
            });
        }
    }
}

function customerView(customerId){
    var url = '/crm/ajax/customer/view/';
    var tbody = $("#table-view").children("tbody");
    tbody.empty();
    $.getJSON(url, {'customer_id': customerId}, function(ret){
        if (ret['msg']==0) {
            var data = ret['data'];
            for (var i=0; i<data.length; i++) {
                tbody.append('<tr class="default"><th scope="row">'+data[i].name+'</th><td>'+data[i].value+'</td></tr>');
            }
        } else {
            alert(ret['msg']);
        }
    });
}

function confirmDelCustomer(customerId, customerName){
    var modal = $('#confirm-modal');
    modal.modal('show');
    modal.find('.modal-body').html("<p>确认要删除<strong>"+customerName+"</strong>吗？");
    modal.find('.modal-footer button').val(customerId);
}

function customerDel(self){
    var customerId = $(self).val();
    var modal = $('#confirm-modal');
    var url = '/crm/ajax/customer/del/';
    $.getJSON(url, {'customer_id': customerId}, function(ret){
        if (ret['msg']==0) {
            modal.modal('hide');
            location.reload();
        } else {
            alert(ret['msg']);
        }
    });
}

// 删除表格table-contact的一行
function table_del(self){
    var lineNum = $(self).val();
    $("#table-contact tr:eq("+lineNum+")").remove();
    table_line_each();
}

// 重新排列表格的行号和button上的行号索引
function table_line_each(){
    $("#table-contact tr:gt(0)").each(function(i){
        $(this).children("th").html(i+1);
        $(this).find("button").attr("value", i+1);
    });
}

function GetTableData(tableId){
    var tableData = [];
    $(tableId+" tr:gt(0)").each(function(trindex, tritem){
        tableData[trindex] = [];
        $(tritem).find("td").each(function(tdindex, tditem){
            tableData[trindex][tdindex] = $(tditem).text();
        });
    });
    return tableData;
}

/*
 * 联系人方面的操作
 */

function checkContact(contact) {
    if (!(contact.name && contact.mobile)) {
        alert("名字和手机不能为空！");
        return false;
    }
    if (!emailCheck(contact.mail)) {
        alert("请正确填写email地址！");
        return false;
    }
    return true;
}

function showContactViewModal(contactId){
    var modal = $('#contact-info-modal');
    modal.modal('show');
    var url = '/crm/ajax/contact/view/';
    $.getJSON(url, {'contact_id': contactId}, function(ret){
        if (ret['msg']==0){
            $('#table_view tr:eq(0) td:eq(0)').html(ret['name']);
            $('#table_view tr:eq(1) td:eq(0)').html(ret['pos']);
            $('#table_view tr:eq(2) td:eq(0)').html(ret['phone']);
            $('#table_view tr:eq(3) td:eq(0)').html(ret['mobile']);
            $('#table_view tr:eq(4) td:eq(0)').html(ret['mail']);
        } else {
            alert(ret['msg']);
        }
    });
}

function show_contact_add_modal(){
    var modal = $('#contact-add-modal');
    modal.modal('show');
    modal.find(".modal-body input[name='contact-name']").val('');
    modal.find(".modal-body input[name='contact-pos']").val('');
    modal.find(".modal-body input[name='contact-tel']").val('');
    modal.find(".modal-body input[name='contact-mobile']").val('');
    modal.find(".modal-body input[name='contact-mail']").val('');
}

function ajaxContactCreate(projectId){
    var modal = $('#contact-add-modal');
    var data = {
        project_id: projectId,
        name: modal.find(".modal-body input[name='contact-name']").val(),
        pos: modal.find(".modal-body input[name='contact-pos']").val(),
        tel: modal.find(".modal-body input[name='contact-tel']").val(),
        mobile: modal.find(".modal-body input[name='contact-mobile']").val(),
        mail: modal.find(".modal-body input[name='contact-mail']").val()
    };
    if (checkContact(data)) {
        var url = '/crm/ajax/contact/add/';
        $.getJSON(url, data, function(ret){
            if (ret['msg']==0){
                modal.modal('hide');
                var oContact = $('#contact');
                oContact.get(0).options.add(new Option(ret['contact_name'], ret['contact_id']));
                oContact.val(ret['contact_id']);
            } else {
                alert(ret['msg']);
            }
        });
    }
}

function contact_add(){
    var modal = $('#contact-add-modal');
    var name = modal.find(".modal-body input[name='contact-name']").val();
    var pos = modal.find(".modal-body input[name='contact-pos']").val();
    var tel = modal.find(".modal-body input[name='contact-tel']").val();
    var mobile = modal.find(".modal-body input[name='contact-mobile']").val();
    var mail = modal.find(".modal-body input[name='contact-mail']").val();
    if (!(name && mobile)) {
        alert("名字和手机不能为空！");
        return false;
    }
    if (!emailCheck(mail)) {
        alert("请正确填写email地址！");
        return false;
    }
    var table = $('#table-contact');
    var tbody = table.children("tbody");
    var row_count = tbody.children('tr').length;
    tbody.append("<tr>"+
                    "<th scope='row'>"+row_count+"</th>"+
                    "<td>"+name+"</td>"+
                    "<td>"+pos+"</td>"+
                    "<td>"+tel+"</td>"+
                    "<td>"+mobile+"</td>"+
                    "<td>"+mail+"</td>"+
                    "<td><button type='button' class='btn btn-sm btn-success' value="+row_count+" onclick='table_del(this)'>删除</button></td>"+
                "</tr>");
    modal.modal('hide');
}

function ajaxContactAdd(projectId){
    var modal = $('#contact-add-modal');
    var data = {
        project_id: projectId,
        name: modal.find(".modal-body input[name='contact-name']").val(),
        pos: modal.find(".modal-body input[name='contact-pos']").val(),
        tel: modal.find(".modal-body input[name='contact-tel']").val(),
        mobile: modal.find(".modal-body input[name='contact-mobile']").val(),
        mail: modal.find(".modal-body input[name='contact-mail']").val()
    };
    if (checkContact(data)) {
        var url = '/crm/ajax/contact/add/';
        $.getJSON(url, data, function(ret){
            if (ret['msg']=='0') {
                modal.modal('hide');
                location.reload();
            } else {
                alert(ret['msg']);
            }
        });
    }
}

function show_contact_edit(self){
    var contact_id_linenum = $(self).val();
    var modal = $('#contact-edit-modal');
    modal.modal('show');

    var id_linenum = contact_id_linenum.split(',');
    var contact_id = id_linenum[0];
    var linenum = id_linenum[1];

    var table_data = GetTableData('#table-contact');
    var contact_this_info = table_data[linenum-1];

    modal.find(".modal-body input[name='contact-name']").val(contact_this_info[0]);
    modal.find(".modal-body input[name='contact-pos']").val(contact_this_info[1]);
    modal.find(".modal-body input[name='contact-tel']").val(contact_this_info[2]);
    modal.find(".modal-body input[name='contact-mobile']").val(contact_this_info[3]);
    modal.find(".modal-body input[name='contact-mail']").val(contact_this_info[4]);
    modal.find(".modal-footer button").val(contact_id);
}

function contact_edit(self){
    var contact_id = $(self).val();
    var modal = $('#contact-edit-modal');
    var data = {
        contact_id:contact_id,
        name: modal.find(".modal-body input[name='contact-name']").val(),
        pos: modal.find(".modal-body input[name='contact-pos']").val(),
        tel: modal.find(".modal-body input[name='contact-tel']").val(),
        mobile: modal.find(".modal-body input[name='contact-mobile']").val(),
        mail: modal.find(".modal-body input[name='contact-mail']").val()
    };
    if (checkContact(data)) {
        var url = '/crm/ajax/contact/edit/';
        $.getJSON(url, data, function(ret){
            if (ret['msg']==0){
                modal.modal('hide');
                location.reload();
            } else {
                alert(ret['msg']);
            }
        });
    }
}

function show_contact_del(self){
    var contact_id_name = $(self).val();
    var modal = $('#confirm-modal');
    modal.modal('show');

    var id_name = contact_id_name.split(',');
    var contact_id = id_name[0];
    var contact_name = id_name[1];

    modal.find(".modal-title strong").html("删除联系人");
    modal.find(".modal-body").html("<h5>确认要删除<strong>"+contact_name+"</strong>吗？</h5>");
    modal.find(".modal-footer button[class='btn btn-success']").attr("onclick", "contact_del(this)");
    modal.find(".modal-footer button[class='btn btn-success']").attr("value", contact_id);
}

function contact_del(self){
    var modal = $('#confirm-modal');
    var contact_id = $(self).val();
    var url = '/crm/ajax/contact/del/';
    $.getJSON(url, {'contact_id': contact_id}, function(ret){
        if (ret['msg']==0){
            modal.modal('hide');
            location.reload();
        } else {
            var contactName = modal.find(".modal-body strong").html();
            modal.find(".modal-body").html(
                "<h5>无法删除<strong>"+contactName+"</strong></h5>" +
                "<p style='color:red;'>"+ret['msg']+"</p>"
            );
        }
    });
}

/*
 * 项目方面的操作
 */

function ajax_project_add(){
    var project_name = $("input[name='project-name']").val();
    if (!project_name) {
        alert('项目名称不能为空！');
        return;
    }
    var customer_id = $("select[name='customer-name']").val();
    var products_id = getChecked('product');
    if (!products_id){
        alert('至少选择一个产品!');
        return;
    }
    var priority = $("select[name='priority']").val();
    var notes = $("textarea[name='notes']").val();

    if (customer_id){
        if (project_name) {
            // 读取表格table-contact中的联系人信息
            var contacts = GetTableData("#table-contact");
            var datas = {
                project_name:project_name,
                customer_id:customer_id,
                products_id:products_id,
                priority:priority,
                notes:notes,
                contacts:contacts
            };
            $.ajax({
                type: "POST",
                url: "/crm/ajax/project/add/",
                contentType: "application/json; charset=utf-8",
                data: JSON.stringify(datas),
                dataType: "json",
                success: function(ret){
                    if (ret['msg']=='0'){
                        backpage();
                    } else {
                        alert(ret['msg']);
                    }
                },
                error: function(){
                    alert("添加项目失败！");
                }
            });
        } else {
            alert("请填写项目名称！");
        }
    } else {
        alert("您还没有跟进任何客户,无法添加项目！");
        backpage();
    }
}

function ajax_project_edit(projectId){
    var project_form = $("#project-edit-form");
    var project_name = project_form.find("input[name='project-name']").val();
    if (!project_name) {
        alert('项目名称不能为空！');
        return;
    }
    var customer_id = project_form.find("select[name='customer-name']").val();
    var products_id = getChecked('product');
    if (!products_id){
        alert('至少选择一个产品!');
        return;
    }
    var priority = project_form.find("select[name='priority']").val();
    var businessmans_id = getChecked("businessman");
    var notes = project_form.find("textarea[name='notes']").val();
    var args = {
        project_id: projectId,
        project_name: project_name,
        customer_id: customer_id,
        priority: priority,
        products_id: products_id,
        notes: notes,
        businessmans_id: businessmans_id
    };
    var url = '/crm/ajax/project/edit/';
    $.getJSON(url, args, function(ret){
        if (ret['msg']=='0'){
            location.href = "/crm/projects/0/0/0/0/";
        } else {
            alert(ret['msg']);
        }
    });
}

function show_project_del(project_id, project_name){
    var modal = $('#confirm-modal');
    modal.modal('show');
    modal.find('.modal-title strong').html("删除项目");
    modal.find('.modal-body').html("<h4>确认要删除<strong>"+project_name+"</strong>吗？</h4>");
    modal.find('.modal-footer button').val(project_id);
}

function project_del(self){
    var modal = $('#confirm-modal');
    var project_id = $(self).val();
    var url = '/crm/ajax/project/del/';
    $.getJSON(url, {'project_id':project_id}, function(ret){
        if (ret['msg']=='0'){
            modal.modal('hide');
            location.reload();
        } else {
            alert(ret['msg']);
        }
    });
}

/*
 *  进度方面的操作
 */

function show_update_progress(self){
    var modal = $('#update-progress-modal');
    modal.modal('show');
    var project_id_name_state = $(self).val();
    var strs = project_id_name_state.split(",");
    var project_id = strs[0];
    var project_name = strs[1];
    var project_progress = strs[2];
    if(project_progress!=undefined){
        if (project_progress==0){project_progress=1}
        modal.find(".modal-body select[name='progress']").val(project_progress);
    }
    modal.find('.modal-title strong').html(project_name+"进度更新");
    modal.find('.modal-footer button').val(project_id);
}

function update_progress(self){
    var project_id = $(self).val();
    var modal = $('#update-progress-modal');
    var body = modal.find(".modal-body");
    var progress = body.find("select[name='progress']").val();
    var description = body.find("textarea[name='description']").val();
    var plan = body.find("textarea[name='plan']").val();
    var updatetime = body.find("input[name='datetime']").val();
    if (description) {
        var args = {
            project_id:project_id,
            progress:progress,
            description:description,
            plan:plan,
            updatetime:updatetime
        };
        var url = '/crm/ajax/progress/add/';
        $.post(url, JSON.stringify(args), function(ret){
            if (ret['msg']=='0'){
                modal.modal('hide');
                location.reload();
            } else {
                alert(ret['msg']);
            }
        }, "json");
    } else {
        alert("请简单填写项目进展！");
    }
}

function show_progress_add(self){
    var modal = $('#progress-modal');
    modal.modal('show');
    var project_id_progress = $(self).val();
    var strs = project_id_progress.split(",");
    var project_id = strs[0];
    var project_progress = strs[1];
    if (project_progress==0){project_progress=1}
    modal.find(".modal-title strong").html("添加项目进度");
    modal.find(".modal-body select[name='progress']").val(project_progress);
    modal.find(".modal-body textarea[name='description']").val('');
    modal.find(".modal-body textarea[name='plan']").val('');
    modal.find(".modal-body input[name='datetime']").val('');
    modal.find(".modal-footer button").val(project_id);
    modal.find(".modal-footer button[class='btn btn-success']").attr("onclick", "progress_add(this)");
}

function show_progress_edit(self){
    var modal = $('#progress-modal');
    modal.modal('show');
    var progress_id_linenum = $(self).val();
    var strs = progress_id_linenum.split(",");
    var progress_id = strs[0];
    var progress_linenum = strs[1];
    var table_data = GetTableData("#table-progress");
    var progress_this_info = table_data[progress_linenum-1];
    modal.find(".modal-title strong").html("编辑进度");
    var choice = {'准备':1,'接洽':2,'测试/试用':3,'谈判':4,'上线':5,'售后':6};
    modal.find(".modal-body select[name='progress']").val(choice[progress_this_info[1]]);
    modal.find(".modal-body textarea[name='description']").val(progress_this_info[2]);
    modal.find(".modal-body textarea[name='plan']").val(progress_this_info[3]);
    modal.find(".modal-body input[name='datetime']").val(progress_this_info[0]);
    modal.find(".modal-footer button").val(progress_id);
    modal.find(".modal-footer button[class='btn btn-success']").attr("onclick", "progress_edit(this)");
}

function progress_edit(self){
    var progress_id = $(self).val();
    var modal = $('#progress-modal');
    var body = modal.find(".modal-body");
    var progress = body.find("select[name='progress']").val();
    var description = body.find("textarea[name='description']").val();
    var plan = body.find("textarea[name='plan']").val();
    var updatetime = body.find("input[name='datetime']").val();
    if (description) {
        var args = {
            progress_id:progress_id,
            progress:progress,
            description:description,
            plan:plan,
            updatetime:updatetime
        };
        var url = '/crm/ajax/progress/edit/';
        $.post(url, JSON.stringify(args), function(ret){
            if (ret['msg']=='0'){
                modal.modal('hide');
                location.reload();
            } else {
                alert(ret['msg']);
            }
        }, "json");
    } else {
        alert("请简单填写项目进展！");
    }
}

function show_progress_del(self){
    var progress_id = $(self).val();
    var modal = $('#confirm-modal');
    modal.modal('show');
    modal.find(".modal-title strong").html("删除进度");
    modal.find(".modal-body").html("<h5>确认要删除这条进度信息吗？</h5>");
    modal.find(".modal-footer button[class='btn btn-success']").attr("onclick", "progress_del(this)");
    modal.find(".modal-footer button[class='btn btn-success']").attr("value", progress_id);
}

/*
 * 标记方面的操作
 */

function show_mark_modal(progressId, mark){
    var modal = $('#mark-modal');
    modal.modal('show');
    modal.find(".modal-body textarea[name=content]").val(mark);
    modal.find(".modal-footer button[class='btn btn-success']").attr("value", progressId);
}

function mark_edit(self){
    var progress_id = $(self).val();
    var modal = $('#mark-modal');
    var content = modal.find(".modal-body textarea[name=content]").val();
    if (content){
        var args = {
            progress_id: progress_id,
            content: content
        };
        var url = '/crm/ajax/mark/edit/';
        $.post(url, JSON.stringify(args), function(ret){
            if (ret['msg']=='0'){
                modal.modal('hide');
                location.reload();
            } else {
                alert(ret['msg']);
            }
        }, "json");
    } else {
        alert("请填写标注内容！");
    }
}

/*
 *  测试申请
 */

function getTestApplyData(){
    var analyser_id = $('#analyser').val();
    var amount_data = $('#amount-data').val();
    var goal = $('#goal').val();
    var fields = $('#fields').val();
    var notes = $('#notes').val();
    var contact_id = $('#contact').val();
    var test_result = getCheckedArray('test-result');
    var overdue_state = getCheckedArray('overdue-state');
    return {
        analyser_id: analyser_id,
        amount_data: amount_data,
        goal: goal,
        fields: fields,
        notes: notes,
        test_result_id: test_result,
        overdue_state: !(overdue_state.length==0),
        contact_id: contact_id
    };
}

function checkTestApplyData(data){
    if (!data.contact_id) {
        alert("缺少联系人");
        return false;
    } else if (data.amount_data === "") {
        alert("请填写测试数据量");
        return false;
    } else if (data.goal === "") {
        alert("请填写本次测试目标");
        return false;
    } else if (data.fields === "") {
        alert("请填写客户提供的测试字段");
        return false;
    } else if (data.test_result_id.length==0) {
        alert("请选择测试结果要求");
        return false;
    }
    return true;
}

function testApplyAdd(projectId){
    loading(true);
    var data = getTestApplyData();
    if (checkTestApplyData(data)){
        data.project_id = projectId;
        var url = '/crm/test-apply/add/';
        $.post(url, JSON.stringify(data), function(ret){
            if (ret['msg']==0){
                backpage();
            } else {
                loading(false);
                alert(ret['msg']);
            }
        }, "json");
    } else {
        loading(false);
    }
}

function testApplyEdit(testApplyId){
    loading(true);
    var data = getTestApplyData();
    if (checkTestApplyData(data)){
        data.test_apply_id = testApplyId;
        var url = '/crm/test-apply/edit/';
        $.post(url, JSON.stringify(data), function(ret){
            if (ret['msg']==0){
                backpage();
            } else {
                loading(false);
                alert(ret['msg']);
            }
        }, "json");
    } else {
        loading(false);
    }
}

function showTestApplyProgressAddModal(url, refuse, progress){
    var modal = $('#update-progress-modal');
    var progress_dom = $('#progress_dom');
    if (refuse) {
        // 退回
        progress_dom.hide();
        $('#progress').val(4);
        modal.find(".modal-title strong").html("理由或建议");
    } else {
        progress_dom.show();
        $('#progress').val(progress);
        modal.find(".modal-title strong").html("更新进度");
    }
    modal.find(".modal-footer button[class='btn btn-success']").attr("onclick", "testApplyProgressAdd(\""+url+"\")");
    modal.modal('show');
}

function testApplyProgressAdd(url){
    var modal = $('#update-progress-modal');
    var progress = $('#progress').val();
    var description = $('#description').val();
    if(!description){
        alert("请简单填写描述信息");
        return false;
    }
    $.getJSON(url, {'progress': progress, 'description': description}, function(ret){
        if (ret['msg']==0){
            modal.modal('hide');
            location.href = '/crm/test-apply/list/'+progress+'/0/0/';
        } else {
            alert(ret['msg']);
        }
    });
}

function showDeleteConfirmModal(testApplyId){
    var modal = $('#confirm-modal');
    modal.modal('show');
    modal.find(".modal-title strong").html("删除测试申请");
    modal.find(".modal-body").html("<h5>确认要删除这个申请吗？</h5>");
    modal.find(".modal-footer button[class='btn btn-success']").attr("value", testApplyId);
}

function testApplyDel(self){
    var modal = $('#confirm-modal');
    var testApplyId = $(self).val();
    var url = '/crm/test-apply/del/';
    $.getJSON(url, {'test_apply_id':testApplyId}, function(result){
        if (result['msg']=='0'){
            modal.modal('hide');
            location.href = '/crm/test-apply/list/4/0/0/';
        } else {
            alert(result['msg']);
        }
    });
}

/*
 * 实施申请
 */

function showSelectProductModel(projectId){
    var modal = $('#select-product-modal');
    modal.find(".modal-footer button[class='btn btn-success']").attr("value", projectId);
    var selectProduct = modal.find(".modal-body select[name='product']").get(0);
    selectProduct.options.length = 0;  // 清除原来的选项
    var url = '/crm/ajax/get-project-products/';
    $.getJSON(url, {'projectid':projectId}, function(result){
        if(result['msg']==0){
            var products = result['products'];
            for(var idx in products){
                selectProduct.options.add(new Option(products[idx].name, products[idx].id));
            }
            modal.modal('show');
        }else{
            alert(result['msg']);
        }
    });
}

function locateImpApply(self){
    var projectId = $(self).val();
    var modal = $('#select-product-modal');
    modal.modal('hide');
    var productId = modal.find(".modal-body select[name='product']").val();
    location.href = '/crm/imp-apply/add/'+projectId+'/'+productId+'/';
}

function showImpApplyProgressAddModal(url, progress){
    var modal = $('#update-progress-modal');
    modal.find(".modal-footer button[class='btn btn-success']").attr("onclick", "impApplyProgressAdd(\""+url+"\"\,"+progress+")");
    modal.modal('show');
}

function impApplyProgressAdd(url, progress){
    var modal = $('#update-progress-modal');
    var description = $('#description').val();
    $.getJSON(url, {'progress': progress, 'description': description}, function(result){
        if(result['msg']==0){
            modal.modal('hide');
            var p = 1;
            if(progress==40){
                p = 5;
            }else if(progress==45){
                p = 6;
            }else if(progress==50){
                p = 7;
            }else if(progress==13){
                p = 8;
            }
            location.href = '/crm/imp-apply/list/'+p+'/0/0/';
        }else{
            alert(result['msg']);
        }
    });
}

function showImpApplyDelModal(impApplyId){
    var modal = $('#confirm-modal');
    modal.modal('show');
    modal.find(".modal-title strong").html("删除交付申请");
    modal.find(".modal-body").html("<h5>确认要删除这个交付申请吗？</h5>");
    modal.find(".modal-footer button[class='btn btn-success']").attr("value", impApplyId);
}

function impApplyDel(self){
    var modal = $('#confirm-modal');
    var impApplyId = $(self).val();
    var url = '/crm/imp-apply/del/';
    $.getJSON(url, {'imp_apply_id': impApplyId}, function(result){
        if(result['msg']==0){
            modal.modal('hide');
            location.href = '/crm/imp-apply/list/5/0/0/';
        }else{
            alert(result['msg']);
        }
    });
}

function impApplyFreeDateStartEdit(impApplyId){
    var modal = $('#update-free-date-start-modal');
    var url = "/crm/imp-apply/free-date-start/edit/" + impApplyId;
    var date = $('#free-date-start-model').val();
    $.getJSON(url, {'date': date}, function(ret){
        if(ret['msg']==0){
            modal.modal('hide');
            $('#free-date-start-td').text(date);
        }else{
            alert(ret['msg']);
        }
    });
}
