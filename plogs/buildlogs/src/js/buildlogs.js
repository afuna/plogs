(function($){
    "use strict";

    function zeropad(number, pad_len) {
        return ("0".repeat(pad_len) + number).slice(-1 * pad_len);
    }

    function init() {
        var today = new Date();
        $("#id_date").val([today.getFullYear(),
                           zeropad(today.getMonth() + 1, 2),
                           zeropad(today.getDate(), 2)]
                        .join('-'));
    }

    init();

})(jQuery);