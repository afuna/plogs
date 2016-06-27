var app = angular.module('editor.directive', []);
app.directive('editor', function (editorModuleAssets, $routeParams, $timeout) {
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

            // save draft, in case of closing tab, etc
            var timeout = null;
            var cacheKey = $routeParams.username+"/"+$routeParams.project+"/"+($routeParams.log_id||"new");
            var saveDraft = function() {
                localStorage[cacheKey] = codemirror.getValue();
            };

            var debounceSaveDraft = function() {
                controller.$setViewValue(codemirror.getValue());

                if (timeout) {
                    $timeout.cancel(timeout);
                }
                timeout = $timeout(saveDraft, 500);
            };

            var restoreDraft = function () {
                var cachedText = localStorage[cacheKey];
                if (cachedText) {
                    codemirror.setValue(cachedText);
                    return true;
                }
                return false;
            };

            // update the ng-model value with editor's current contents
            codemirror.on('change', debounceSaveDraft);

            // restore any saved draft
            restoreDraft();

            // TODO: these two events are weird; feels like a better fit for a service
            // set the editor's initial value (if someone does a $broadcast)
            scope.$on('editor.init', function(e, value) {
                var restored = restoreDraft();
                if (!restored) {
                    codemirror.setValue(value);
                }
            });

            scope.$on('editor.insertImage', function(e, image) {
                codemirror.replaceSelection('![' + image.alt + '](' +  image.url +' "' + image.caption +'")\n');
            });

            // clear the cached values when we're done with the editor
            scope.$on('editor.saved', function() {
                delete localStorage[cacheKey];
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

            function fixImageOrientation(images, formData) {
                var deferreds = [];
                for (var i = 0; i < images.length; i++) {
                    var deferred = new $.Deferred();
                    deferreds.push(deferred);

                    var image = images[i];
                    loadImage.parseMetaData(
                        image,
                        function(deferred, image) {
                            return function(data) {
                                // get orientation from exif, or assume normal
                                var orientation = data.exif ? data.exif.get('Orientation') : 1;
                                loadImage(image,
                                    function(canvas) {
                                        canvas.toBlob(function(blob) {
                                            formData.append('images', blob, image.name);
                                            deferred.resolve();
                                        },
                                        image.type
                                        );
                                    },
                                    { orientation: orientation, canvas: true });
                            }
                        }(deferred, image)
                    );
                }
                return deferreds;
            }

            function s3_upload(e){
                var formData = new FormData();
                var fixedImagesDeferreds = fixImageOrientation(e.target.files || e.originalEvent.dataTransfer.files, formData);
                $.when.apply($, fixedImagesDeferreds).then(function() {
                    // after fixing all images, we upload them all to s3
                    var s3upload = new S3Upload({
                        files: formData.getAll('images'),
                        s3_sign_put_url: '/people/' + $routeParams.username + '/build/photo_upload_url/',
                        project: $routeParams.project,
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
                });
            }

            $("#image_upload").change(s3_upload);
            $("body")
                .on("drop", s3_upload)
                .on("drop dragover dragleave", function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    $(codemirror.display.wrapper).toggleClass("droppable", e.type == "dragover");
                });
        }
    };
});
