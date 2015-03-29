module.exports = function(grunt) {
    "use strict";

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        bower: {
            install: {
                options: {
                    copy: false
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
            js: {
                files: [
                    {
                        flatten: true,
                        expand: true,
                        src: ['plogs/main/src/vendor/bootstrap/dist/js/*', 'plogs/main/src/vendor/jquery/dist/*'],
                        dest: 'plogs/main/static/assets/js/vendor/'
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
        },

        clean: {
            dist: 'plogs/main/static/assets'
        },

        watch: {
            less: {
                files: 'plogs/main/src/less/**/*.less',
                tasks: 'dist-css'
            }
        },

    });

    grunt.loadNpmTasks('grunt-bower-task');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-contrib-watch');

    grunt.registerTask('install', ['bower:install']);
    grunt.registerTask('dist-css', ['less:compile']);
    grunt.registerTask('dist-js', ['copy:js']);
    grunt.registerTask('dist', ['clean:dist', 'dist-css', 'copy:fonts', 'dist-js']);
    grunt.registerTask('default', ['install', 'dist']);
};