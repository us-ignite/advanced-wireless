module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    sass: {
      options: {
        includePaths: ['us_ignite/assets/bower_components/foundation/scss']
      },
      dist: {
        options: {
          outputStyle: 'compressed'
        },
        files: {
          'us_ignite/assets/css/app.css': 'scss/app.scss',
          'us_ignite/assets/css/ie.css': 'scss/ie.scss'
        }
      }
    },

    pixrem: {
      options: {
        rootvalue: '16px',
        replace: true
      },
      dist: {
        src: 'us_ignite/assets/css/ie.css',
        dest: 'us_ignite/assets/css/ie.css'
      }
    },

    watch: {
      grunt: { files: ['Gruntfile.js'] },

      sass: {
        files: 'scss/**/*.scss',
        tasks: ['sass']
      }
    }
  });

  grunt.loadNpmTasks('grunt-sass');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-pixrem');

  grunt.registerTask('build', ['sass', 'pixrem']);
  grunt.registerTask('default', ['build','watch']);
}
