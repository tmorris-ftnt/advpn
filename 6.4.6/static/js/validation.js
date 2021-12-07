// Wait for the DOM to be ready

jQuery.validator.addMethod('validvpnrange', function(value) {
    var split = value.split(/\.|\//);
    if (split.length != 5)
        return false;

    if(split[4] != 17 && split[4] != 14)
      return false;

    if (split[0].length==0 || isNaN(split[0]) || split[0]<0 || split[0]>255)
      return false;

    if (split[4] == 17) {
      if (split[1].length==0 || isNaN(split[1]) || split[1]<0 || split[1]>255)
        return false;
      if (split[2] != 0 && split[2] != 128)
        return false;
    }

    if (split[4] == 14) {
      if (split[1].length==0 || isNaN(split[1]) || split[1]<0 || split[1]>255 || split[1] % 8 > 0)
        return false;
      if (split[2] != 0)
        return false;
    }

    if (split[3] != 0)
      return false;

    return true;
}, ' Invalid IP Address');

jQuery.validator.addMethod('validIP', function(value) {
    var split = value.split('.');
    if (split.length != 4)
        return false;

    for (var i=0; i<split.length; i++) {
        var s = split[i];
        if (s.length==0 || isNaN(s) || s<0 || s>255)
            return false;
    }
    return true;
}, ' Invalid IP Address');

jQuery.validator.addMethod('validsubnetlist', function(value) {
    var split = value.split(",");
    for (var i = 0; i < split.length; i++) {

      var s = split[i].split("/");

      if (s.length != 2)
        return false;

      if (s[1] > 32 || s[1] < 0 || s[1].length == 0 || isNaN(s[1]))
        return false;
      var ip = s[0].split(".");

      if (ip.length != 4)
        return false;
      for (var i2 = 0; i2 < ip.length; i2++) {
        var a = ip[i2];
        if (a.length == 0 || isNaN(a) || a < 0 || a > 255)
          return false;
      }
    }
    return true;
}, ' Invalid Subnet List');

jQuery.validator.addClassRules({
  valipaddr: {
    required: true,
    validIP: true
  },
  valportname: {
    required: true,
    minlength: 1,
    maxlength: 15
  },
  valsubnetlist: {
    required: true,
    validsubnetlist: true

  }
});




$(function() {
  // Initialize form validation on the registration form.
  // It has the name attribute "registration"
  $("form[name='vpnform']").validate({
    // Specify validation rules
    rules: {
      // The key name on the left side is the name attribute
      // of an input field. Validation rules are defined
      // on the right side
      bgpas: {
      required: true,
      range: [0, 4294967295]
    },
      vpnaddressrange: {
        required: true,
        validvpnrange: true
      },
      password: {
        required: true,
        minlength: 5
      }
    },
    // Specify validation error messages
    messages: {
      bgpas: "Please enter your a valid BGP AS number",
      vpnaddressrange: "Please enter a valid /17 or /14 ip address range (format: 10.200.128.0/17)",
      lastname: "Please enter your lastname",
      password: {
        required: "Please provide a password",
        minlength: "Your password must be at least 5 characters long"
      },
      email: "Please enter a valid email address"
    },
    // Make sure the form is submitted to the destination defined
    // in the "action" attribute of the form when valid
    submitHandler: function(form) {
      form.submit();
    }
  });
});
