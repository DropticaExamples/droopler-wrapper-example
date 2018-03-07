# import classes to override
from docker_console.web.engines.drupal8.builder import Builder
from docker_console.utils.console import message as msg, run as run_cmd

class BuilderLocal:

    def npm_install(self):
        print("INSTALL NPM PACKAGES (Node.js)")
        run_cmd("docker run --rm -v %s:/var/www/html -w /var/www/html/profiles/contrib/droopler/themes/custom/droopler_theme droptica/gulptheme npm install" % self.config.WEB['APP_ROOT'])
        run_cmd("docker run --rm -v %s:/var/www/html -w /var/www/html/themes/custom/droopler_subtheme droptica/gulptheme npm install" % self.config.WEB['APP_ROOT'])

    def gulp_watch(self):
        print("GULP WATCH SUBTHEME")
        run_cmd("docker run --rm -e VIRTUAL_HOST=styleguide.%s -it -v %s:/var/www/html -w /var/www/html/themes/custom/droopler_subtheme droptica/gulptheme gulp watch" % (self.config.DRUPAL['default']['SITE_URI'], self.config.WEB['APP_ROOT']))

    def gulp_watch_base(self):
        print("GULP WATCH BASE THEME")
        run_cmd("docker run --rm -e VIRTUAL_HOST=styleguide.%s -it -v %s:/var/www/html -w /var/www/html/profiles/contrib/droopler/themes/custom/droopler_theme droptica/gulptheme gulp watch" % (self.config.DRUPAL['default']['SITE_URI'], self.config.WEB['APP_ROOT']))

    def gulp_dist(self):
        print("GULP DIST (dumping prod assets)")
        run_cmd("docker run --rm -v %s:/var/www/html -w /var/www/html/profiles/contrib/droopler/themes/custom/droopler_theme droptica/gulptheme gulp dist" % self.config.WEB['APP_ROOT'])
        run_cmd("docker run --rm -v %s:/var/www/html -w /var/www/html/themes/custom/droopler_subtheme droptica/gulptheme gulp dist" % self.config.WEB['APP_ROOT'])

    def gulp_compile(self):
        print("GULP COMPILE (dumping dev assets)")
        run_cmd("docker run --rm -v %s:/var/www/html -w /var/www/html/profiles/contrib/droopler/themes/custom/droopler_theme droptica/gulptheme gulp compile" % self.config.WEB['APP_ROOT'])
        run_cmd("docker run --rm -v %s:/var/www/html -w /var/www/html/themes/custom/droopler_subtheme droptica/gulptheme gulp compile" % self.config.WEB['APP_ROOT'])

    def gulp_clean(self):
        print("GULP CLEAN")
        run_cmd("docker run --rm -v %s:/var/www/html -w /var/www/html/profiles/contrib/droopler/themes/custom/droopler_theme droptica/gulptheme gulp clean" % self.config.WEB['APP_ROOT'])
        run_cmd("docker run --rm -v %s:/var/www/html -w /var/www/html/themes/custom/droopler_subtheme droptica/gulptheme gulp clean" % self.config.WEB['APP_ROOT'])

    def gulp_debug(self):
        print("GULP DEBUG")
        run_cmd("docker run --rm -v %s:/var/www/html -w /var/www/html/profiles/contrib/droopler/themes/custom/droopler_theme droptica/gulptheme gulp debug" % self.config.WEB['APP_ROOT'])
        run_cmd("docker run --rm -v %s:/var/www/html -w /var/www/html/themes/custom/droopler_subtheme droptica/gulptheme gulp debug" % self.config.WEB['APP_ROOT'])

    def install_profile(self):
        print("INSTALL PROFILE")
        self.drush.run("site-install droopler --db-url='mysql://user:pass@mysql/db' --site-name=droopler -y")


Builder.__bases__ += (BuilderLocal,)

# replace/add new commands
commands_overrides = {
    'composer-install' : [ 'docker.docker_run("composer install -vvv -d ./app/")' ],
    'composer-update' : [ 'docker.docker_run("composer update -vvv -d ./app/")' ],
    'composer-outdated' : [ 'docker.docker_run("composer outdated -d ./app/")' ],
    'composer-scaffold' : [ 'docker.docker_run("composer drupal-scaffold -d ./app/")' ],
    'gulp-watch' : [ 'gulp_watch' ],
    'gulp-watch-base' : [ 'gulp_watch_base' ],
    'gulp-clean' : [ 'gulp_clean' ],
    'gulp-compile' : [ 'gulp_compile' ],
    'gulp-dist' : [ 'gulp_dist' ],
    'gulp-debug' : [ 'gulp_debug' ],
    'npm-install' : [ 'npm_install' ],
    'build-profile': [
        'confirm_action',
        'docker.docker_run("composer clear-cache -vvv -d ./app/")',
        'docker.docker_run("composer self-update -vvv")',
        'docker.docker_run("composer install -vvv -d ./app/")',
        'docker.docker_run("composer drupal-scaffold -d ./app/")',
        'docker.docker_run("composer install -vvv -d ./app/")',
        'npm_install',
        'gulp_compile',
        'docker.docker_run("docker-console build-profile-in-docker")',
        'docker.chown',
        'docker.setfacl',
        'chmod_files',
        'chmod_private_files'
    ],
    'build-profile-in-docker': [
        'drupal_settings.copy_settings("drupal8", True)',
        'install_profile',
        'drush.cr',
        'drush.updb',
        'drush.change_password',
        'drush.uli'
    ],
    'build': [
        'confirm_action',
        'docker.docker_run("composer clear-cache -vvv -d ./app/")',
        'docker.docker_run("composer self-update -vvv")',
        'docker.docker_run("composer install -vvv -d ./app/")',
        'docker.docker_run("composer drupal-scaffold -d ./app/")',
        'docker.docker_run("composer install -vvv -d ./app/")',
        'npm_install',
        'gulp_compile',
        'docker.docker_run("docker-console build-in-docker")',
        'docker.chown',
        'docker.setfacl',
        'chmod_files',
        'chmod_private_files'
    ],
    'build-in-docker': [
        'drupal_settings.copy_settings("drupal8", True)',
        'database.drop_db',
        'database.create_db',
        'database.import_db',
        'drush.cr',
        'drush.updb',
        'drush.change_password',
        'drush.uli'
    ],
    'prepare': [
        'confirm_action',
        'docker.docker_run("composer clear-cache -vvv -d ./app/")',
        'docker.docker_run("composer self-update -vvv")',
        'docker.docker_run("composer install -vvv -d ./app/")',
        'docker.docker_run("composer drupal-scaffold -d ./app/")',
        'docker.docker_run("composer install -vvv -d ./app/")',
        'npm_install',
        'gulp_compile',
        'docker.chown',
        'docker.setfacl',
        'chmod_files',
        'chmod_private_files'
    ],
}
