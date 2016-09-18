import argparse, getpass, json

from borgapicli.plugins.app import AppPlugin
from borgapicli.plugins.auth import AuthPlugin
from borgapicli.plugins.user import UserPlugin


class ClientRunner(object):
    """
    This class is for registering all plugin commands
    """

    def setup(self):
        self.parser = argparse.ArgumentParser(prog='borgapi_cli', description='borgsphere api client tool')
        self.parser.add_argument('--version', '-v', action='version', version='borgsphere api client 1.0')

        subparsers = self.parser.add_subparsers(metavar='COMMAND')

        # authenticate first
        self.auth_plugin = AuthPlugin(self)
        self.auth_plugin._before_register(subparsers)
        self.auth_plugin.register()

        # load omega app api command line
        app_plugin = AppPlugin(self)
        app_plugin._before_register(subparsers)
        app_plugin.register()

        # load user api command line
        user_login = UserPlugin(self)
        user_login._before_register(subparsers)
        user_login.register()

    def run(self, args=None):
        self.args = self.parser.parse_args(args=args)
        data = self.args.func(self.args)
        print(data)