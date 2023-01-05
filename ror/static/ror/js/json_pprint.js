// Django admin jQuery implementation of code found here :
// https://til.simonwillison.net/django/pretty-print-json-admin

// wrap it in jQuery function to delay processing until document is loaded
django.jQuery(function () {

  // to support regular admin and grappelli
  const targets = ['div.grp-readonly', 'div-readonly']

  django.jQuery(targets).each(function () {
    django.jQuery('div.grp-readonly').each(function () {
      var $this = django.jQuery(this)
      try {
        // must parse the text first to check if it is json
        // if it is not valid json, an error will be thrown and the field skipped
        $this.text(JSON.stringify(JSON.parse($this.text()), null, 2));
      } catch {
        return;
      }
      // modify the style of the div
      $this.css({
        "whiteSpace": "pre-wrap",
        "fontFamily": 'courier',
        "min-width": "600px",
      })
    })
  })
})