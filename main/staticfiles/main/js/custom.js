function displayNotification(from, align, text) {
    type = ['', 'info', 'danger', 'success', 'warning', 'rose', 'primary'];

    color = Math.floor((Math.random() * 6) + 1);

    $.notify({
      icon: "gavel",
      message: text

    }, {
      type: type[color],
      timer: 30000,
      placement: {
        from: from,
        align: align
      }
    });
  }
