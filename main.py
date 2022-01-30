import subprocess


class WiFiPassword:
    def __init__(self) -> None:
        pass

    def convertIterItem(self, item: str) -> str:
        return item.split(':')[1].strip()

    def extract_wifi_passwords(self) -> None:
        profiles_data = subprocess.check_output("netsh wlan show profiles").decode('utf-8', 'ignore').split('\n')
        profiles = [self.convertIterItem(i) for i in profiles_data if 'All User Profile' in i]

        with open('log.txt', 'w') as file:
            for profile in profiles:
                try:
                    file.write(self.getPasswordInProfile(profile))
                except subprocess.CalledProcessError:
                    pass
            file.close

    def getPasswordInProfile(self, profile: str) -> str:
        profile_info = subprocess.check_output(f"netsh wlan show profile {profile} key=clear").decode('utf-8', 'ignore').split('\n')
        password = ''.join([self.convertIterItem(i) for i in profile_info if 'Key Content' in i and self.convertIterItem(i) != []])

        if password == '':
            password = 'None'

        return f'Name: {profile}\nPassword: {password}\n\n\n'


def main() -> None:
    module = WiFiPassword()
    module.extract_wifi_passwords()


if __name__ == '__main__':
    main()