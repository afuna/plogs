(function() {

  window.S3Upload = (function() {

    S3Upload.prototype.project = '';

    S3Upload.prototype.log_id = '';

    S3Upload.prototype.s3_sign_put_url = '/signS3put';

    S3Upload.prototype.files = [];

    S3Upload.prototype.onStart = function(filename) {
      return console.log('base.onStart()', filename)
    };

    S3Upload.prototype.onFinishS3Put = function(imageData, filename) {
      return console.log('base.onFinishS3Put()', imageData, filename);
    };

    S3Upload.prototype.onProgress = function(percent, status, filename) {
      return console.log('base.onProgress()', percent, status, filename);
    };

    S3Upload.prototype.onError = function(status) {
      return console.log('base.onError()', status);
    };

    function S3Upload(options) {
      if (options == null) options = {};
      for (option in options) {
        this[option] = options[option];
      }
      this.handleFileSelect(this.files);
    }

    S3Upload.prototype.handleFileSelect = function(files) {
      var f, output, _i, _len, _results;
      output = [];
      _results = [];
      for (_i = 0, _len = files.length; _i < _len; _i++) {
        f = files[_i];
        this.onProgress(0, 'Upload started.', f.name);
        this.onStart(f.name);
        _results.push(this.uploadFile(f));
      }
      return _results;
    };


    S3Upload.prototype.createCORSRequest = function(method, url) {
      var xhr;
      xhr = new XMLHttpRequest();
      if (xhr.withCredentials != null) {
        xhr.open(method, url, true);
      } else if (typeof XDomainRequest !== "undefined") {
        xhr = new XDomainRequest();
        xhr.open(method, url);
      } else {
        xhr = null;
      }
      return xhr;
    };

    S3Upload.prototype.executeOnSignedUrl = function(file, callback) {
      var this_s3upload, xhr, log_id;
      this_s3upload = this;
      xhr = new XMLHttpRequest();
      log_id = this.log_id || "";
      xhr.open('GET', this.s3_sign_put_url + '?s3_object_type=' + file.type + '&project=' + this.project + '&log_id=' + log_id, true);
      xhr.overrideMimeType('text/plain; charset=x-user-defined');
      xhr.onreadystatechange = function(e) {
        var result;
        if (this.readyState === 4 && this.status === 200) {
          try {
            result = JSON.parse(this.responseText);
          } catch (error) {
            this_s3upload.onError('Signing server returned some ugly/empty JSON: "' + this.responseText + '"');
            return false;
          }
          return callback(result.signed_request, result.image);
        } else if (this.readyState === 4 && this.status !== 200) {
          return this_s3upload.onError('Could not contact request signing server. Status = ' + this.status);
        }
      };
      return xhr.send();
    };

    S3Upload.prototype.uploadToS3 = function(file, url, imageData) {
      var this_s3upload, xhr;
      this_s3upload = this;
      xhr = this.createCORSRequest('PUT', url);
      if (!xhr) {
        this.onError('CORS not supported');
      } else {
        xhr.onload = function() {
          if (xhr.status === 200) {
            this_s3upload.onProgress(100, 'Upload completed.', file.name);
            return this_s3upload.onFinishS3Put(imageData, file.name);
          } else {
            return this_s3upload.onError('Upload error: ' + xhr.status);
          }
        };
        xhr.onerror = function() {
          return this_s3upload.onFinishS3Put(imageData, file.name);
          return this_s3upload.onError('XHR error.');
        };
        xhr.upload.onprogress = function(e) {
          var percentLoaded;
          if (e.lengthComputable) {
            percentLoaded = Math.round((e.loaded / e.total) * 100);
            return this_s3upload.onProgress(percentLoaded, percentLoaded === 100 ? 'Finalizing.' : 'Uploading.', file.name);
          }
        };
      }
      xhr.setRequestHeader('Content-Type', file.type);
      xhr.setRequestHeader('x-amz-acl', 'public-read')
      return xhr.send(file);
    };

    S3Upload.prototype.uploadFile = function(file) {
      var this_s3upload;
      this_s3upload = this;
      return this.executeOnSignedUrl(file, function(signedURL, imageData) {
        return this_s3upload.uploadToS3(file, signedURL, imageData);
      });
    };

    return S3Upload;

  })();

}).call(this);
