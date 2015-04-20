module.exports = function(grunt) {
    "use strict";

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        bower: {
            install: {
                options: {
                    copy: false // doesn't copy nested, so let's copy manually
                }
            }
        },

        less: {
            compile: {
                options: {
                    strictMath: true,
                    sourceMap: true,
                    outputSourceFiles: true,
                    sourceMapURL: '<%= pkg.name %>.css.map',
                    sourceMapFilename: '<%= compiled_assets %>/css/<%= pkg.name %>.css.map'
                },
                src: ['plogs/*/src/less/*.less', '!plogs/main/src/**', 'plogs/main/src/less/custom-bootstrap.less'],
                dest: '<%= compiled_assets %>/css/<%= pkg.name %>.css'
            }
        },

        concat: {
            options: {
                banner: ";(function(){\n 'use strict';",
                footer: "})();"
            },
            modules: {
                expand: true,
                files: {
                    '<%= compiled_assets %>/main/js/auth.module.js': 'plogs/main/src/js/auth/*',
                    '<%= compiled_assets %>/buildlogs/js/index.module.js': 'plogs/buildlogs/src/js/index/*',
                    '<%= compiled_assets %>/buildlogs/js/buildlogs.module.js': 'plogs/buildlogs/src/js/buildlogs/*'
                }
            }
        },

        copy: {
            vendor: {
                files: [
                    {
                        expand: true,
                        cwd: 'bower_components',
                        src: ['bootstrap/less/**', 'bootstrap/dist/js/*', 'jquery/dist/*', 'bootstrap/dist/fonts/*', 'angular*/angular*.js'],
                        dest: '<%= vendor_assets %>'
                    }
                ]
            },
            vendorjs: {
                expand: true,
                cwd: '<%= vendor_assets %>',
                src: ['bootstrap/dist/js/*', 'jquery/dist/*', 'angular*/angular*.js'],
                dest: '<%= compiled_assets %>/vendor'
            },
            appjs: {
                expand: true,
                cwd: "plogs",
                src: ['*/src/js/*', '*/src/js/*/partials/*', '*/src/views/**'],
                dest: '<%= compiled_assets %>',
                rename: function(dest, src) {
                    return dest + "/" + src.replace("src/", "");
                }
            },
            fonts: {
                expand: true,
                flatten: true,
                src: '<%= vendor_assets %>/bootstrap/dist/fonts/*',
                dest: '<%= compiled_assets%>/fonts'
            }
        },

        clean: {
            dist: ['<%= vendor_assets %>', '<%= compiled_assets %>']
        },

        watch: {
            less: {
                options: {
                    livereload: true,
                    spawn: false
                },
                files: ['plogs/**/src/less/**/*.less'],
                tasks: ['less:compile']
            },
            js: {
                options: {
                    livereload: true,
                    spawn: false
                },
                files: [
                    'plogs/**/src/js/*.js',
                    'plogs/**/src/js/**/**.js',
                    'plogs/**/src/js/**/*.tmpl.html',
                    'plogs/**/src/views/*.html',
                    'plogs/**/src/views/**/*.html'
                    ],
                tasks: ['concat:modules', 'copy:appjs']
            }
        },
        vendor_assets: "plogs/main/src/vendor",
        compiled_assets: "plogs/main/static/assets"
    });

    // on watch events only copy the changed file
    grunt.event.on('watch', function (action, filepath, target) {
        if (target === "js") {
            grunt.config('copy.appjs.src', filepath.replace('plogs/', ''));
        }
    });

    grunt.loadNpmTasks('grunt-bower-task');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-concat');

    grunt.registerTask('install', ['bower:install']);
    grunt.registerTask('dist-css', ['copy:vendor', 'less:compile']);
    grunt.registerTask('dist-js', ['copy:vendorjs', 'concat:modules', 'copy:appjs']);
    grunt.registerTask('dist', ['clean:dist', 'dist-css', 'copy:fonts', 'dist-js']);
    grunt.registerTask('default', ['install', 'dist']);
};