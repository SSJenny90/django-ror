if (!$) {
  $ = django.jQuery;
} // for use in the django admin site without specifying another jquery version

$(function () {

  const $select = $('.select2');

  $select.select2({
    minimumInputLength: 1,
    ajax: {
      url: 'https://api.ror.org/organizations',
      delay: 1000,
      data: function (params) {
        return {
          "query": params.term
        };
      },
      processResults: function (data) {
        return {
          results: $.map(data.items, function (item) {
            return {
              ...item,
              ...{
                text: item['name'],
              }
            }
          })
        };
      },
      templateSelection: function (data, container) {
        // Add custom attributes to the <option> tag for the selected option
        // $(data.element).val(JSON.stringify(data));
        $(data.element).attr('data-established', data.established)
        return data.text;
      }
    }
  });

  $select.on('change', function () {
    $("#id_info").val(JSON.stringify($(this).select2('data')[0]))
  })

})