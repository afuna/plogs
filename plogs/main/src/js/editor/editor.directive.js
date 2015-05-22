var app = angular.module('editor.directive', []);
app.directive('editor', function (editorModuleAssets, $routeParams) {
    return {
        restrict: 'E',
        require: 'ngModel',
        templateUrl: editorModuleAssets('partials/editor.tmpl.html'),
        controllerAs: 'editor',
        link: function(scope, element, attrs, controller) {
            var textarea = element.find('textarea').get(0);
            var codemirror = CodeMirror.fromTextArea(textarea, {
                mode: 'markdown',
                lineWrapping: true,
                dragDrop: false,
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

            // set the editor's initial value (if someone does a $broadcast)
            scope.$on('editor.init', function(e, value) {
                codemirror.setValue(value);
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

            element.find("button").click(function(e) {
                e.preventDefault();
                insertions[$(this).data("type") || "el"]($(this));
                codemirror.focus();
            });

            function upload_placeholder_text(filename) {
                return "![Uploading " + filename + "]()\n";
            }

            function s3_upload(e){
                var s3upload = new S3Upload({
                    files: e.target.files || e.originalEvent.dataTransfer.files,
                    s3_sign_put_url: '/people/' + $routeParams.username + '/build/photo_upload_url/',
                    project_id: $routeParams.project_id,
                    log_id: $routeParams.log_id,
                    onProgress: function(percent, message, filename) {
                    },
                    onStart: function(filename) {
                        codemirror.replaceSelection(upload_placeholder_text(filename));
                    },
                    onFinishS3Put: function(imageData, filename) {
                        var placeholder_text = upload_placeholder_text(filename);
                        var index = codemirror.getValue().indexOf(placeholder_text);

                        var pos_start = codemirror.posFromIndex(index);
                        var pos_end = codemirror.posFromIndex(index + placeholder_text.length);

                        codemirror.replaceRange('![' + filename + '](' +  imageData.url +' "caption")\n',
                                                pos_start, pos_end);

                        var onUpload = scope.$eval(attrs.onUpload);
                        scope.$apply(onUpload(imageData));
                    }
                });
            }

            $("#image_upload").change(s3_upload);
            $(codemirror.display.scroller)
                .on("drop", s3_upload)
                .on("drop dragover dragleave", function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    $(codemirror.display.wrapper).toggleClass("droppable", e.type == "dragover");
                });
        }
    };
});
