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
                    sourceMapFilename: 'main/static/assets/css/<%= pkg.name %>.css.map'
                },
                src: 'main/src/less/custom-bootstrap.less',
                dest: 'main/static/assets/css/<%= pkg.name %>.css'
            }
        },

        copy: {
            js: {
                files: [
                    {
                        flatten: true,
                        expand: true,
                        src: ['main/src/vendor/bootstrap/dist/js/*', 'main/src/vendor/jquery/dist/*'],
                        dest: 'main/static/assets/js/vendor/'
                    },
                    {
                        expand: true,
                        src: 'main/src/js',
                        dest: 'main/static/assets/js'
                    }
                ]
            }
        },

        clean: {
            dist: 'main/static/assets'
        }
    });

    grunt.loadNpmTasks('grunt-bower-task');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-clean');

    grunt.registerTask('install', ['bower:install']);
    grunt.registerTask('dist-css', ['less:compile']);
    grunt.registerTask('dist-js', ['copy:js']);
    grunt.registerTask('dist', ['clean:dist', 'dist-css', 'dist-js']);
    grunt.registerTask('default', ['install', 'dist']);
};