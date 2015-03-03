module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    meta: {
      banner: '/*! <%= pkg.name %> - v<%= pkg.version %> - ' + '<%= grunt.template.today("yyyy-mm-dd") %> */',
      modern: [
        'us_ignite/assets/bower_components/jquery/dist/jquery.min.js',
        'us_ignite/assets/bower_components/fastclick/lib/fastclick.js',
        'us_ignite/assets/bower_components/foundation/js/foundation/foundation.js',
        'us_ignite/assets/bower_components/foundation/js/foundation/foundation.dropdown.js',
        'us_ignite/assets/bower_components/foundation/js/foundation/foundation.orbit.js',
        'us_ignite/assets/bower_components/foundation/js/foundation/foundation.topbar.js',
        'us_ignite/assets/js/vendor/jquery-ui-1.10.4.custom.js',
        'us_ignite/assets/globalcityteams/js/slick.min.js',
        'us_ignite/assets/js/app.js'
        ],
      basic: [
        'us_ignite/assets/bower_components/jquery-1.9.1/index.js',
        'us_ignite/assets/bower_components/foundation/js/foundation/foundation.js',
        'us_ignite/assets/bower_components/foundation/js/foundation/foundation.dropdown.js',
        'us_ignite/assets/bower_components/foundation/js/foundation/foundation.orbit.js',
        'us_ignite/assets/bower_components/foundation/js/foundation/foundation.topbar.js',
        'us_ignite/assets/js/vendor/jquery-ui-1.10.4.custom.js',
        'us_ignite/assets/globalcityteams/js/slick.min.js',
        'us_ignite/assets/js/vendor/html5shiv.js',
        'us_ignite/assets/js/vendor/nwmatcher-1.2.5-min.js',
        'us_ignite/assets/js/vendor/selectivizr-1.0.3b.js',
        'us_ignite/assets/js/vendor/respond.min.js',
        'us_ignite/assets/js/app.js'
        ],
      modern_microsite: [
        'us_ignite/assets/bower_components/jquery/dist/jquery.min.js',
        'us_ignite/assets/bower_components/fastclick/lib/fastclick.js',
        'us_ignite/assets/bower_components/foundation/js/foundation/foundation.js',
        'us_ignite/assets/bower_components/foundation/js/foundation/foundation.dropdown.js',
        'us_ignite/assets/bower_components/foundation/js/foundation/foundation.orbit.js',
        'us_ignite/assets/bower_components/foundation/js/foundation/foundation.topbar.js',
        'us_ignite/assets/js/vendor/jquery-ui-1.10.4.custom.js',
        'us_ignite/assets/js/app.js',
        'us_ignite/assets/globalcityteams/js/slick.min.js',
        'us_ignite/assets/globalcityteams/js/jquery.validate.min.js',
        'us_ignite/assets/globalcityteams/js/jquery.dataTables.min.js',
        'us_ignite/assets/globalcityteams/js/dataTables.responsive.min.js',
        'us_ignite/assets/globalcityteams/js/jquery.matchHeight-min.js',
        'us_ignite/assets/globalcityteams/js/gctc.js'
        ],
      basic_microsite: [
        'us_ignite/assets/bower_components/jquery-1.9.1/index.js',
        'us_ignite/assets/bower_components/foundation/js/foundation/foundation.js',
        'us_ignite/assets/bower_components/foundation/js/foundation/foundation.dropdown.js',
        'us_ignite/assets/bower_components/foundation/js/foundation/foundation.orbit.js',
        'us_ignite/assets/bower_components/foundation/js/foundation/foundation.topbar.js',
        'us_ignite/assets/js/vendor/jquery-ui-1.10.4.custom.js',
        'us_ignite/assets/js/vendor/html5shiv.js',
        'us_ignite/assets/js/vendor/nwmatcher-1.2.5-min.js',
        'us_ignite/assets/js/vendor/selectivizr-1.0.3b.js',
        'us_ignite/assets/js/vendor/respond.min.js',
        'us_ignite/assets/js/app.js',
        'us_ignite/assets/globalcityteams/js/slick.min.js',
        'us_ignite/assets/globalcityteams/js/jquery.validate.min.js',
        'us_ignite/assets/globalcityteams/js/jquery.dataTables.min.js',
        'us_ignite/assets/globalcityteams/js/dataTables.responsive.min.js',
        'us_ignite/assets/globalcityteams/js/jquery.matchHeight-min.js',
        'us_ignite/assets/globalcityteams/js/gctc.js'
        ]
    },

    concat: {
      options: {
        separator: '\n;\n',
        banner: '<%= meta.banner %>'
      },
      all: {
        files: {
          'us_ignite/assets/js/lib/modern.js': ['<%= meta.modern %>'],
          'us_ignite/assets/js/lib/basic.js': ['<%= meta.basic %>'],
          'us_ignite/assets/js/lib/modern_microsite.js': ['<%= meta.modern_microsite %>'],
          'us_ignite/assets/js/lib/basic_microsite.js': ['<%= meta.basic_microsite %>']
        }
      }
    },

    uglify: {
      options: {
        mangle: {
          except: []
        }
      },
      all: {
        files: {
          'us_ignite/assets/js/lib/modern.js': 'us_ignite/assets/js/lib/modern.js',
          'us_ignite/assets/js/lib/basic.js': 'us_ignite/assets/js/lib/basic.js',
          'us_ignite/assets/js/lib/modern_microsite.js': 'us_ignite/assets/js/lib/modern_microsite.js',
          'us_ignite/assets/js/lib/basic_microsite.js': 'us_ignite/assets/js/lib/basic_microsite.js'
        }
      }
    },

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

  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-uglify');

  grunt.registerTask('build', ['sass', 'pixrem']);
  grunt.registerTask('buildjs', ['concat', 'uglify']);
  grunt.registerTask('default', ['build','buildjs', 'watch']);
}
