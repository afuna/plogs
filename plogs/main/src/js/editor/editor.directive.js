var app = angular.module('editor.directive', []);
app.directive('editor', function (editorModuleAssets) {
    return {
        restrict: 'E',
        require: 'ngModel',
        scope: {},
        templateUrl: editorModuleAssets('partials/editor.tmpl.html'),
        link: function(scope, element, attrs, controller) {
            var textarea = element.find('textarea').get(0)
            var codemirror = CodeMirror.fromTextArea(textarea, {
                mode: 'markdown',
                lineWrapping: true,
                extraKeys: {
                    "Enter": "newlineAndIndentContinueMarkdownList",
                    "Tab": false
                }
            });

            // style the markdown editor to look like a textarea
            codemirror.display.wrapper.classList.add("form-control");

            // update the ng-model value with editor's current contents
            codemirror.on('change', function() {
                controller.$setViewValue(codemirror.getValue());
            });


            // based on markdownify
            var insertions = {
                el: function(btn) {
                    codemirror.replaceSelection(btn.data('prefix') + codemirror.getSelection());
                    if (btn.data('suffix')) {
                        codemirror.replaceSelection(btn.data('prefix'), 'start');
                    }
                },
                link: function() {
                    var link = window.prompt('Enter a url').trim();
                    if (link !== null && link.length > 0) {
                        var selection = codemirror.getSelection();
                        selection = selection.length === 0 ? link : selection;
                        codemirror.replaceSelection('[' + selection + '](' + link + ')')
                    }
                },
                image: function() {
                }
            };

            element.find("button").click(function() {
                insertions[$(this).data("type") || "el"]($(this));
                codemirror.focus();
            });
        }
    };
});
