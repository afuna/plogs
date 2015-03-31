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
                    sourceMapFilename: 'plogs/main/static/assets/css/<%= pkg.name %>.css.map'
                },
                src: 'plogs/main/src/less/custom-bootstrap.less',
                dest: 'plogs/main/static/assets/css/<%= pkg.name %>.css'
            }
        },

        copy: {
            vendor: {
                files: [
                    {
                        expand: true,
                        cwd: 'bower_components',
                        src: ['bootstrap/less/**', 'bootstrap/dist/js/*', 'jquery/dist/*'],
                        dest: 'plogs/main/src/vendor/'
                    }
                ]
            },
            js: {
                files: [
                    {
                        expand: true,
                        cwd: 'plogs/main/src/',
                        src: ['vendor/bootstrap/dist/js/*', 'vendor/jquery/dist/*'],
                        dest: 'plogs/main/static/assets/js'
                    },
                    {
                        expand: true,
                        src: 'plogs/main/src/js',
                        dest: 'plogs/main/static/assets/js'
                    }
                ]
            },
            fonts: {
                expand: true,
                flatten: true,
                src: 'plogs/main/src/vendor/bootstrap/dist/fonts/*',
                dest: 'plogs/main/static/assets/fonts'
            },
            staticfiles: {
                expand: true,
                cwd: 'plogs/main/static/assets/',
                src: '**',
                dest: 'staticfiles/assets/'
            }
        },

        clean: {
            dist: ['plogs/main/src/vendor', 'plogs/main/static/assets', 'staticfiles/assets']
        },

        watch: {
            less: {
                files: 'plogs/main/src/less/**/*.less',
                tasks: ['dist-css', 'dist-static']
            }
        },

    });

    grunt.loadNpmTasks('grunt-bower-task');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-contrib-watch');

    grunt.registerTask('install', ['bower:install']);
    grunt.registerTask('dist-css', ['copy:vendor', 'less:compile']);
    grunt.registerTask('dist-js', ['copy:js']);
    grunt.registerTask('dist-static', ['copy:staticfiles']);
    grunt.registerTask('dist', ['clean:dist', 'dist-css', 'copy:fonts', 'dist-js', 'dist-static']);
    grunt.registerTask('default', ['install', 'dist']);
};