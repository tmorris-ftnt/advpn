function addhub() {
    if (+$("#numberofhubs").val() > 3) {
        alert("ADVPN Wizard only support a maximum of 4 hubs");
    } else {
        $("#numberofhubs").val(+$("#numberofhubs").val() + 1);
        $("#hubstitle").html("Hubs (" + $("#numberofhubs").val() + "/4)");
        if (+$("#numberofhubs").val() > 3) {
            $("#addhubbutton").attr("disabled", "disabled");
            $("#addhubbutton").attr("class", "medium disabled");
            $("#addhubbutton").html("Max Reached");
        } else {
            $("#addhubbutton").removeAttr("disabled");
            $("#addhubbutton").attr("class", "medium green");
            $("#addhubbutton").html("<i class=\"fa fa-plus\"></i> Add Hub");
        }
        if (+$("#numberofhubs").val() > 1) {
            $("#removehubbutton").removeAttr("disabled");
            $("#removehubbutton").attr("class", "medium green");
}

        var newhubnum = $("#numberofhubs").val();
        $("#hubcontainer").append("<div id=\"hub" + newhubnum + "\" class=\"sitebox\">" +
            "<label for=\"hub" + newhubnum + "-hubname\">Hub Name</label><input class=\"valportname\" id=\"hub" + newhubnum + "-hubname\" name=\"hub" + newhubnum + "-hubname\"=type=\"text\" placeholder=\"i.e. Hub" + newhubnum + "\"/><label for=\"hub1platform\"" +
            "<label for=\"hub" + newhubnum + "-hubsubnets\">Hub Subnet(s) (Comma seperated)</label><input class=\"valsubnetlist\" id=\"hub" + newhubnum + "-hubsubnets\" name=\"hub" + newhubnum + "-hubsubnets\"=type=\"text\" placeholder=\"i.e. 192.168.1.0/24,192.168.101.0/24\"/>" +
            "<div id=\"hub" + newhubnum + "vpncontainer\"> </div>" +
            "<button type=\"button\" class=\"small green\" id=\"addhub" + newhubnum + "intfbutton\" onclick=\"addhubintf(" + newhubnum + ")\"><i class=\"fa fa-plus\"></i> Add Interface</button>" +
            "<button type=\"button\" class=\"small disabled\" id=\"removehub" + newhubnum + "intfbuttonbutton\" disabled=\"disabled\" onclick=\"removehubintf(" + newhubnum + ")\"><i class=\"fa fa-minus\"></i> Remove Interface</button>" +
            "<input type=\"hidden\" name=\"hub" + newhubnum + "numofinterfaces\" id=\"hub" + newhubnum + "numofinterfaces\" value=0>" +
            "</div>");
        addhubintf(newhubnum)
    }
}

function removehub() {
    var lasthubnum = $("#numberofhubs").val();
    $("#hub" + lasthubnum).remove();
    $("#numberofhubs").val(+$("#numberofhubs").val() - 1);
    $("#hubstitle").html("Hubs (" + $("#numberofhubs").val() + "/4)");

    if (+$("#numberofhubs").val() < 2) {
        $("#removehubbutton").attr("disabled", "disabled");
        $("#removehubbutton").attr("class", "medium disabled");
    }
    if (+$("#numberofhubs").val() < 4) {
        $("#addhubbutton").removeAttr("disabled");
        $("#addhubbutton").attr("class", "medium green");
        $("#addhubbutton").html("<i class=\"fa fa-plus\"></i> Add Hub");

    }
}

function addhubintf(hubnum) {
    $("#hub" + hubnum + "numofinterfaces").val(+$("#hub" + hubnum + "numofinterfaces").val() + 1);
    $("#hub" + hubnum + "vpncontainer").append("<div id=\"hub" + hubnum + "-intf" + $("#hub" + hubnum + "numofinterfaces").val() + "box\">Interface #" + $("#hub" + hubnum + "numofinterfaces").val() + "<div class=\"interfacebox\">" +
    "<label for=\"hub" + hubnum + "-intf" + $("#hub" + hubnum + "numofinterfaces").val() + "intfname\">Interface Name</label><input class=\"valportname\" id=\"hub" + hubnum + "-intf" + $("#hub" + hubnum + "numofinterfaces").val() + "intfname\" name=\"hub" + hubnum + "-intf" + $("#hub" + hubnum + "numofinterfaces").val() + "intfname\" type=\"text\" placeholder=\"i.e. port1\"/>" +
    "<label for=\"hub" + hubnum + "-intf" + $("#hub" + hubnum + "numofinterfaces").val() + "underlay\">Underlay</label><select name=\"hub" + hubnum + "-intf" + $("#hub" + hubnum + "numofinterfaces").val() + "underlay\" id=\"hub" + hubnum + "-intf" + $("#hub" + hubnum + "numofinterfaces").val() + "underlay\"><option value=\"internet\">Internet</option><option value=\"private\">Private/MPLS</option></select>" +
    "<label for=\"hub" + hubnum + "-intf" + $("#hub" + hubnum + "numofinterfaces").val() + "ip\">IP Address/Hostname</label><input class=\"valipaddr\"  id=\"hub" + hubnum + "-intf" + $("#hub" + hubnum + "numofinterfaces").val() + "ip\" name=\"hub" + hubnum + "-intf" + $("#hub" + hubnum + "numofinterfaces").val() + "ip\" type=\"text\" placeholder=\"i.e. 100.64.1.1\"/>" +
    "</div></div>");

    if (+$("#hub" + hubnum + "numofinterfaces").val() > 1) {
        $("#removehub" + hubnum + "intfbuttonbutton").removeAttr("disabled");
        $("#removehub" + hubnum + "intfbuttonbutton").attr("class", "small green");
    }

}

function removehubintf(hubnum) {
    var lastintfnum = $("#hub" + hubnum + "numofinterfaces").val();
    $("#hub" + hubnum + "-intf" + lastintfnum + "box").remove();
    $("#hub" + hubnum + "numofinterfaces").val(+$("#hub" + hubnum + "numofinterfaces").val() - 1);

    if (+$("#hub" + hubnum + "numofinterfaces").val() < 2) {
        $("#removehub" + hubnum + "intfbuttonbutton").attr("disabled", "disabled");
        $("#removehub" + hubnum + "intfbuttonbutton").attr("class", "small disabled");
    }
}

//############################
//// Spokes
//############################

function addspoke() {
    if (+$("#numberofspokes").val() > 3) {
        alert("ADVPN Wizard only support a maximum of 4 spokes");
    } else {
        $("#numberofspokes").val(+$("#numberofspokes").val() + 1);
        $("#spokestitle").html("spokes (" + $("#numberofspokes").val() + "/4)");
        if (+$("#numberofspokes").val() > 3) {
            $("#addspokebutton").attr("disabled", "disabled");
            $("#addspokebutton").attr("class", "medium disabled");
            $("#addspokebutton").html("Max Reached");
        } else {
            $("#addspokebutton").removeAttr("disabled");
            $("#addspokebutton").attr("class", "medium green");
            $("#addspokebutton").html("<i class=\"fa fa-plus\"></i> Add spoke");
        }
        if (+$("#numberofspokes").val() > 1) {
            $("#removespokebutton").removeAttr("disabled");
            $("#removespokebutton").attr("class", "medium green");
}

        var newspokenum = $("#numberofspokes").val();
        $("#spokecontainer").append("<div id=\"spoke" + newspokenum + "\" class=\"sitebox\">" +
            "<label for=\"spoke" + newspokenum + "-spokename\">Spoke Name</label><input class=\"valportname\" id=\"spoke" + newspokenum + "-spokename\" name=\"spoke" + newspokenum + "-spokename\"=type=\"text\" placeholder=\"i.e. Branch" + newspokenum + "\"/>" +
            "<label for=\"spoke" + newspokenum + "-spokesubnets\">Spoke Subnet(s) (Comma seperated)</label><input class=\"valsubnetlist\" id=\"spoke" + newspokenum + "-spokesubnets\" name=\"spoke" + newspokenum + "-spokesubnets\"=type=\"text\" placeholder=\"i.e. 192.168.1.0/24,192.168.101.0/24\"/>" +
            "<div id=\"spoke" + newspokenum + "vpncontainer\"> </div>" +
            "<button type=\"button\" class=\"small green\" id=\"addspoke" + newspokenum + "intfbutton\" onclick=\"addspokeintf(" + newspokenum + ")\"><i class=\"fa fa-plus\"></i> Add Interface</button>" +
            "<button type=\"button\" class=\"small disabled\" id=\"removespoke" + newspokenum + "intfbuttonbutton\" disabled=\"disabled\" onclick=\"removespokeintf(" + newspokenum + ")\"><i class=\"fa fa-minus\"></i> Remove Interface</button>" +
            "<input type=\"hidden\" name=\"spoke" + newspokenum + "numofinterfaces\" id=\"spoke" + newspokenum + "numofinterfaces\" value=0 autocomplete=\"off\">" +
            "</div>");
        addspokeintf(newspokenum)
    }
}

function removespoke() {
    var lastspokenum = $("#numberofspokes").val();
    $("#spoke" + lastspokenum).remove();
    $("#numberofspokes").val(+$("#numberofspokes").val() - 1);
    $("#spokestitle").html("spokes (" + $("#numberofspokes").val() + "/4)");

    if (+$("#numberofspokes").val() < 2) {
        $("#removespokebutton").attr("disabled", "disabled");
        $("#removespokebutton").attr("class", "medium disabled");
    }
    if (+$("#numberofspokes").val() < 4) {
        $("#addspokebutton").removeAttr("disabled");
        $("#addspokebutton").attr("class", "medium green");
        $("#addspokebutton").html("<i class=\"fa fa-plus\"></i> Add spoke");

    }
}

function addspokeintf(spokenum) {
    $("#spoke" + spokenum + "numofinterfaces").val(+$("#spoke" + spokenum + "numofinterfaces").val() + 1);
    $("#spoke" + spokenum + "vpncontainer").append("<div id=\"spoke" + spokenum + "-intf" + $("#spoke" + spokenum + "numofinterfaces").val() + "box\">Interface #" + $("#spoke" + spokenum + "numofinterfaces").val() + "<div class=\"interfacebox\">" +
    "<label for=\"spoke" + spokenum + "-intf" + $("#spoke" + spokenum + "numofinterfaces").val() + "intfname\">Interface Name</label><input class=\"valportname\" id=\"spoke" + spokenum + "-intf" + $("#spoke" + spokenum + "numofinterfaces").val() + "intfname\" name=\"spoke" + spokenum + "-intf" + $("#spoke" + spokenum + "numofinterfaces").val() + "intfname\" type=\"text\" placeholder=\"i.e. port1\"/>" +
    "<label for=\"spoke" + spokenum + "-intf" + $("#spoke" + spokenum + "numofinterfaces").val() + "underlay\">Underlay</label><select name=\"spoke" + spokenum + "-intf" + $("#spoke" + spokenum + "numofinterfaces").val() + "underlay\" id=\"spoke" + spokenum + "-intf" + $("#spoke" + spokenum + "numofinterfaces").val() + "underlay\"><option value=\"internet\">Internet</option><option value=\"private\">Private/MPLS</option></select>" +
    "</div></div>");

    if (+$("#spoke" + spokenum + "numofinterfaces").val() > 1) {
        $("#removespoke" + spokenum + "intfbuttonbutton").removeAttr("disabled");
        $("#removespoke" + spokenum + "intfbuttonbutton").attr("class", "small green");
    }

}

function removespokeintf(spokenum) {
    var lastintfnum = $("#spoke" + spokenum + "numofinterfaces").val();
    $("#spoke" + spokenum + "-intf" + lastintfnum + "box").remove();
    $("#spoke" + spokenum + "numofinterfaces").val(+$("#spoke" + spokenum + "numofinterfaces").val() - 1);

    if (+$("#spoke" + spokenum + "numofinterfaces").val() < 2) {
        $("#removespoke" + spokenum + "intfbuttonbutton").attr("disabled", "disabled");
        $("#removespoke" + spokenum + "intfbuttonbutton").attr("class", "small disabled");
    }
}




function xportjson() {

    var jsonxport = $( "form" ).serializeArray();
    $("#exportbox").html(JSON.stringify(jsonxport, null,4));
}


// A $( document ).ready() block.
$( document ).ready(function() {
    addhub();
});