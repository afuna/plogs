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

        copy: {
            vendor: {
                files: [
                    {
                        expand: true,
                        cwd: 'bower_components',
                        src: ['bootstrap/less/**', 'bootstrap/dist/js/*', 'jquery/dist/*', 'bootstrap/dist/fonts/*'],
                        dest: '<%= vendor_assets %>'
                    }
                ]
            },
            js: {
                files: [
                    {
                        expand: true,
                        cwd: '<%= vendor_assets %>',
                        src: ['bootstrap/dist/js/*', 'jquery/dist/*', 'angular/*'],
                        dest: '<%= compiled_assets %>/vendor'
                    },
                    {
                        expand: true,
                        cwd: "plogs",
                        src: '*/src/js/*',
                        dest: '<%= compiled_assets %>',
                        rename: function(dest, src) {
                            return dest + "/" + src.replace("src/", "");
                        }
                    }
                ]
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
                    livereload: true
                },
                files: ['plogs/**/src/less/**/*.less'],
                tasks: ['less:compile']
            },
            js: {
                options: {
                    livereload: true
                },
                files: 'plogs/**/src/js/**.js',
                tasks: ['copy:js']
            }
        },
        vendor_assets: "plogs/main/src/vendor",
        compiled_assets: "plogs/main/static/assets"
    });

    grunt.loadNpmTasks('grunt-bower-task');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-contrib-watch');

    grunt.registerTask('install', ['bower:install']);
    grunt.registerTask('dist-css', ['copy:vendor', 'less:compile']);
    grunt.registerTask('dist-js', ['copy:js']);
    grunt.registerTask('dist', ['clean:dist', 'dist-css', 'copy:fonts', 'dist-js']);
    grunt.registerTask('default', ['install', 'dist']);
};